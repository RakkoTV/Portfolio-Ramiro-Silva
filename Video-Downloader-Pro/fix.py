import os
import time
import logging
import traceback
import yt_dlp
from utils import CustomExceptions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('downloader.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('DownloadFixer')


class RetryDownloader:
    """Class to handle YouTube downloads with retry logic and better error handling"""
    
    def __init__(self, max_retries=5, initial_backoff=1, backoff_factor=2, max_backoff=60):
        """Initialize the RetryDownloader with retry parameters
        
        Args:
            max_retries (int): Maximum number of retry attempts
            initial_backoff (int): Initial backoff time in seconds
            backoff_factor (int): Factor to multiply backoff time on each retry
            max_backoff (int): Maximum backoff time in seconds
        """
        self.max_retries = max_retries
        self.initial_backoff = initial_backoff
        self.backoff_factor = backoff_factor
        self.max_backoff = max_backoff
        self.failed_downloads = []
    
    def download_with_retry(self, url, ydl_opts, progress_callback=None):
        """Download a video with retry logic and exponential backoff
        
        Args:
            url (str): YouTube video URL
            ydl_opts (dict): Options for yt-dlp
            progress_callback (function, optional): Callback for progress updates
            
        Returns:
            dict: Information about the downloaded video
            
        Raises:
            CustomExceptions.DownloadError: If download fails after all retries
        """
        # Add progress hooks if provided
        if progress_callback and 'progress_hooks' not in ydl_opts:
            ydl_opts['progress_hooks'] = [progress_callback]
        
        # Ensure socket timeout is set
        if 'socket_timeout' not in ydl_opts:
            ydl_opts['socket_timeout'] = 30
        
        # Ensure retries is set
        if 'retries' not in ydl_opts:
            ydl_opts['retries'] = 3
        
        # Track retry attempts
        attempt = 0
        backoff_time = self.initial_backoff
        last_error = None
        
        while attempt <= self.max_retries:
            try:
                logger.info(f"Attempt {attempt+1}/{self.max_retries+1} to download {url}")
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    return info
                    
            except Exception as e:
                last_error = e
                error_message = str(e)
                
                # Check if it's a timeout error
                if "Read timed out" in error_message or "timed out" in error_message.lower():
                    logger.warning(f"Network timeout on attempt {attempt+1} for {url}: {error_message}")
                    
                    # If we have more retries left, wait and try again
                    if attempt < self.max_retries:
                        logger.info(f"Retrying in {backoff_time} seconds...")
                        time.sleep(backoff_time)
                        
                        # Increase backoff time for next attempt (exponential backoff)
                        backoff_time = min(backoff_time * self.backoff_factor, self.max_backoff)
                        attempt += 1
                        continue
                    else:
                        # We've exhausted all retries
                        error_type = "Network timeout"
                        break
                else:
                    # For non-timeout errors, we might want different handling
                    if "HTTP Error 429" in error_message:
                        error_type = "Rate limited"
                        # For rate limiting, use longer backoff
                        if attempt < self.max_retries:
                            backoff_time = min(backoff_time * 3, 120)  # Longer backoff for rate limits
                            logger.warning(f"Rate limited. Retrying in {backoff_time} seconds...")
                            time.sleep(backoff_time)
                            attempt += 1
                            continue
                    elif "This video is unavailable" in error_message:
                        error_type = "Video unavailable"
                        # No point retrying unavailable videos
                        break
                    else:
                        error_type = "Download error"
                        # For other errors, retry with standard backoff
                        if attempt < self.max_retries:
                            logger.info(f"Retrying in {backoff_time} seconds...")
                            time.sleep(backoff_time)
                            backoff_time = min(backoff_time * self.backoff_factor, self.max_backoff)
                            attempt += 1
                            continue
                        break
            
            # If we get here, download was successful
            return
        
        # If we get here, all retries failed
        error_details = f"{error_type}: {str(last_error)}"
        logger.error(f"Failed to download {url} after {self.max_retries+1} attempts: {error_details}")
        
        # Add to failed downloads list
        self.failed_downloads.append({
            'url': url,
            'error_type': error_type,
            'error_message': str(last_error)
        })
        
        raise CustomExceptions.DownloadError(f"Failed to download after {self.max_retries+1} attempts: {error_details}")
    
    def download_playlist_with_retry(self, playlist_url, ydl_opts, download_path, progress_callback=None):
        """Download a playlist with retry logic for each video
        
        Args:
            playlist_url (str): YouTube playlist URL
            ydl_opts (dict): Options for yt-dlp
            download_path (str): Path to save downloaded videos
            progress_callback (function, optional): Callback for progress updates
            
        Returns:
            dict: Summary of download results
        """
        # First, extract playlist info
        extract_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'ignoreerrors': True,
            'no_color': True,
            'http_headers': ydl_opts.get('http_headers', {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            })
        }
        
        try:
            with yt_dlp.YoutubeDL(extract_opts) as ydl:
                playlist_info = ydl.extract_info(playlist_url, download=False)
                
                if not playlist_info or 'entries' not in playlist_info:
                    raise CustomExceptions.ValidationError("No se pudieron obtener los videos de la lista")
                
                videos = [v for v in playlist_info['entries'] if v is not None]
                if not videos:
                    raise CustomExceptions.ValidationError("No se encontraron videos válidos en la lista")
                
                # Create directory for playlist
                playlist_title = playlist_info.get('title', 'Playlist')
                playlist_dir = os.path.join(download_path, self._sanitize_filename(playlist_title))
                if not os.path.exists(playlist_dir):
                    os.makedirs(playlist_dir)
                
                # Configure download options
                download_opts = ydl_opts.copy()
                download_opts.update({
                    'outtmpl': os.path.join(playlist_dir, '%(title)s.%(ext)s'),
                })
                
                if progress_callback:
                    download_opts['progress_hooks'] = [progress_callback]
                
                # Download each video with retry
                successful_downloads = 0
                total_videos = len(videos)
                
                for i, video in enumerate(videos, 1):
                    if not video:
                        continue
                    
                    try:
                        video_url = f"https://www.youtube.com/watch?v={video['id']}"
                        self.download_with_retry(video_url, download_opts)
                        successful_downloads += 1
                    except Exception as e:
                        # Already logged in download_with_retry
                        pass
                
                # Return summary
                return {
                    'total': total_videos,
                    'successful': successful_downloads,
                    'failed': len(self.failed_downloads),
                    'failed_details': self.failed_downloads,
                    'download_path': playlist_dir
                }
                
        except Exception as e:
            logger.error(f"Error processing playlist: {str(e)}\n{traceback.format_exc()}")
            raise CustomExceptions.DownloadError(f"Error processing playlist: {str(e)}")
    
    def get_failed_downloads_report(self):
        """Generate a report of failed downloads
        
        Returns:
            str: Formatted report of failed downloads
        """
        if not self.failed_downloads:
            return "No failed downloads."
        
        report = "Los siguientes videos no se pudieron descargar:\n"
        for item in self.failed_downloads:
            report += f"- {item['url']}: ERROR: {item['error_type']}\n  {item['error_message']}\n"
        
        return report
    
    def _sanitize_filename(self, filename):
        """Sanitize filename to be safe for filesystem
        
        Args:
            filename (str): Original filename
            
        Returns:
            str: Sanitized filename
        """
        # Replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename


def main():
    """Example usage of RetryDownloader"""
    # Example usage
    downloader = RetryDownloader(max_retries=3)
    
    # Example options
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 30,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    }
    
    # Example URL that failed previously
    url = "https://www.youtube.com/watch?v=sHp5kGuJspk"
    
    try:
        # Try to download with retry logic
        downloader.download_with_retry(url, ydl_opts)
        print(f"Successfully downloaded {url}")
    except CustomExceptions.DownloadError as e:
        print(f"Failed to download: {e}")
        print("\nFailed downloads report:")
        print(downloader.get_failed_downloads_report())


if __name__ == "__main__":
    main()
