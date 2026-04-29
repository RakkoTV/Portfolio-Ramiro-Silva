import os
import time
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

# Configure logging
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
file_handler = logging.FileHandler('downloader.log', encoding='utf-8')
file_handler.setFormatter(logging.Formatter(log_format))

error_handler = logging.FileHandler('error_download.txt', encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(log_format))

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(log_format))

logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[file_handler, error_handler, console_handler]
)

logger = logging.getLogger('YouTubeDownloader')

class CustomExceptions:
    class DownloadError(Exception):
        pass

    class ValidationError(Exception):
        pass

def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f'Error in {func.__name__}: {str(e)}')
            raise
    return wrapper

class DownloadManager:
    def __init__(self, max_workers=3):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.downloads = {}
        self.lock = threading.Lock()

    def add_download(self, url, ydl_opts):
        with self.lock:
            future = self.executor.submit(self._download, url, ydl_opts)
            self.downloads[url] = {
                'future': future,
                'status': 'downloading',
                'progress': 0
            }
            return future

    def _download(self, url, ydl_opts):
        try:
            import yt_dlp
            def progress_hook(d):
                if d['status'] == 'downloading':
                    with self.lock:
                        if url in self.downloads:
                            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                            downloaded = d.get('downloaded_bytes', 0)
                            if total > 0:
                                progress = (downloaded / total) * 100
                                self.downloads[url]['progress'] = progress
                                logger.info(f'Descarga en progreso para {url}: {progress:.1f}% completado')
                            speed = d.get('speed', 0)
                            eta = d.get('eta', 0)
                            self.downloads[url]['speed'] = speed
                            self.downloads[url]['eta'] = eta
                            if speed and eta:
                                logger.info(f'Velocidad: {speed/1024/1024:.1f} MB/s, Tiempo restante: {eta} segundos')
                elif d['status'] == 'finished':
                    with self.lock:
                        if url in self.downloads:
                            self.downloads[url]['progress'] = 100
                            logger.info(f'Descarga completada para {url}')

            # Configurar para no descargar, solo extraer información
            ydl_opts['progress_hooks'] = [progress_hook]
            ydl_opts['extract_info'] = True
            ydl_opts['noplaylist'] = True
            ydl_opts['format'] = 'best'
            
            # Asegurarse de que no se descargue el archivo
            if 'outtmpl' in ydl_opts:
                del ydl_opts['outtmpl']
                
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                with self.lock:
                    if url in self.downloads:
                        self.downloads[url]['status'] = 'completed'
                        self.downloads[url]['info'] = info
                return info
        except Exception as e:
            error_msg = str(e)
            error_details = {
                'error_type': type(e).__name__,
                'error_message': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            logger.error(f'Error downloading {url}:\nTipo: {error_details["error_type"]}\nMensaje: {error_details["error_message"]}\nHora: {error_details["timestamp"]}')
            with self.lock:
                if url in self.downloads:
                    self.downloads[url]['status'] = 'error'
                    self.downloads[url]['error'] = error_details
            raise CustomExceptions.DownloadError(error_msg)

    def get_download_status(self, url):
        with self.lock:
            return self.downloads.get(url, {'status': 'not_found'})

    def cancel_download(self, url):
        with self.lock:
            if url in self.downloads:
                future = self.downloads[url]['future']
                future.cancel()
                self.downloads[url]['status'] = 'cancelled'
                return True
            return False