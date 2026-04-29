from flask import Flask, render_template, request, jsonify, Response
from utils import DownloadManager, CustomExceptions, handle_exceptions, logger
import yt_dlp
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import cloudscraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Importación condicional de moviepy
try:
    from moviepy.editor import VideoFileClip
except ImportError:
    logger.warning('MoviePy no está disponible. Algunas funcionalidades podrían estar limitadas.')
    VideoFileClip = None

app = Flask(__name__)

# Inicializar el administrador de descargas
download_manager = DownloadManager(max_workers=3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download_video():
    try:
        url = request.json.get('url')
        if not url:
            return jsonify({'error': 'URL no proporcionada'}), 400

        # Validar formato de URL
        if not url.startswith(('http://', 'https://')):
            return jsonify({'error': 'URL inválida. Debe comenzar con http:// o https://'}), 400

        # Configurar opciones mejoradas para obtener la URL directa del video
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Mejorar selección de formato
            'quiet': True,
            'no_warnings': True,
            'extract_info': True,
            'cookiesfrombrowser': ('chrome',),
            'ignoreerrors': False,  # Cambiar a False para capturar todos los errores
            'extract_flat': False,
            'noplaylist': True,
            'skip_download': True,
            'socket_timeout': 30,  # Aumentado para evitar timeouts prematuros
            'retries': 5,  # Aumentado número de reintentos
            'verbose': True,  # Activar modo verboso para mejor diagnóstico
            'force-ipv4': True,  # Forzar IPv4 para mejor compatibilidad
            'geo-bypass': True  # Intentar evitar restricciones geográficas
        }

        try:
            # Obtener la URL directa del video con manejo mejorado de formatos
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    logger.error(f'No se pudo extraer información del video: {url}')
                    return jsonify({'error': 'No se pudo obtener información del video'}), 400

                # Intentar obtener la URL del video de diferentes maneras
                video_url = None
                formats = info.get('formats', [])
                
                # Primero intentar obtener la URL directa
                video_url = info.get('url')
                
                # Si no hay URL directa, buscar en los formatos disponibles
                if not video_url and formats:
                    # Filtrar formatos de video MP4
                    mp4_formats = [f for f in formats if f.get('ext') == 'mp4']
                    if mp4_formats:
                        # Ordenar por calidad y seleccionar el mejor
                        best_format = max(mp4_formats, key=lambda f: f.get('filesize', 0) if f.get('filesize') else f.get('tbr', 0))
                        video_url = best_format['url']
                    else:
                        # Si no hay MP4, usar el mejor formato disponible
                        video_url = formats[-1]['url']

                if not video_url:
                    logger.error(f'No se encontró URL de video válida para: {url}')
                    return jsonify({'error': 'No se pudo obtener la URL del video'}), 400

                response_data = {
                    'video_url': video_url,
                    'title': info.get('title', ''),
                    'ext': info.get('ext', ''),
                    'duration': info.get('duration'),
                    'thumbnail': info.get('thumbnail'),
                    'format': info.get('format')
                }
                
                logger.info(f'Video encontrado exitosamente: {info.get("title")}')
                return jsonify(response_data)

        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            logger.error(f'Error de descarga de yt-dlp: {error_msg}')
            # Mejorar mensajes de error para el usuario
            if 'Video unavailable' in error_msg:
                return jsonify({'error': 'El video no está disponible o es privado'}), 400
            elif 'This video is only available for registered users' in error_msg:
                return jsonify({'error': 'Este video requiere inicio de sesión'}), 403
            elif 'Sign in to confirm your age' in error_msg:
                return jsonify({'error': 'Este video tiene restricción de edad'}), 403
            else:
                return jsonify({'error': f'Error al procesar el video: {error_msg}'}), 400

    except Exception as e:
        logger.error(f'Error inesperado al procesar video: {str(e)}')
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/download/status')
def get_download_status():
    try:
        url = request.args.get('url')
        if not url:
            return jsonify({'error': 'URL no proporcionada'}), 400

        status = download_manager.get_download_status(url)
        return jsonify(status)

    except Exception as e:
        logger.error(f'Error al obtener estado de descarga: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_video():
    try:
        query = request.json.get('query')
        if not query:
            return jsonify({'error': 'Consulta no proporcionada'}), 400

        # Configurar opciones de búsqueda
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'default_search': 'ytsearch',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(f'ytsearch5:{query}', download=False)
            videos = [{
                'title': entry['title'],
                'url': entry['url'],
                'duration': entry.get('duration'),
                'view_count': entry.get('view_count'),
                'thumbnail': entry.get('thumbnail')
            } for entry in results['entries']]

        return jsonify({'videos': videos})

    except Exception as e:
        logger.error(f'Error en búsqueda: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/channel-info', methods=['POST'])
def get_channel_info():
    try:
        # Validar que la solicitud sea JSON
        if not request.is_json:
            logger.error('Solicitud no contiene JSON válido')
            return jsonify({'error': 'La solicitud debe ser JSON'}), 400

        channel_url = request.json.get('channelUrl')
        if not channel_url:
            logger.error('URL del canal no proporcionada')
            return jsonify({'error': 'URL del canal no proporcionada'}), 400

        # Normalizar URL del canal
        if '@' not in channel_url:
            logger.error(f'URL del canal inválida: {channel_url}')
            return jsonify({'error': 'URL del canal inválida. Debe incluir @'}), 400

        if not channel_url.startswith('http'):
            channel_url = f'https://www.youtube.com/{channel_url}'

        # Configurar opciones para obtener info del canal
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'extract_info': True,
            'force_generic_extractor': False
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                channel_info = ydl.extract_info(channel_url, download=False)
                if not channel_info:
                    logger.error(f'No se pudo obtener información del canal: {channel_url}')
                    return jsonify({'error': 'No se pudo obtener información del canal'}), 404

                info = {
                    'title': channel_info.get('title', 'Sin título'),
                    'description': channel_info.get('description', 'Sin descripción'),
                    'subscriber_count': channel_info.get('subscriber_count', 0),
                    'video_count': channel_info.get('entries_count', 0),
                    'channel_url': channel_url,
                    'thumbnail': channel_info.get('thumbnail', '')
                }
                logger.info(f'Información del canal obtenida exitosamente: {channel_url}')
                return jsonify(info)

            except yt_dlp.utils.DownloadError as e:
                logger.error(f'Error al descargar información del canal: {str(e)}')
                return jsonify({'error': 'No se pudo acceder al canal'}), 404

    except Exception as e:
        logger.error(f'Error al obtener info del canal: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/viral', methods=['POST'])
def get_viral_videos():
    try:
        if not request.is_json:
            return jsonify({'error': 'La solicitud debe ser JSON'}), 400

        # Configurar opciones de Chrome
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        try:
            # Inicializar el navegador
            driver = webdriver.Chrome(options=chrome_options)
            driver.get('https://www.youtube.com/feed/trending')

            # Esperar a que los videos se carguen
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'ytd-video-renderer'))
            )

            # Obtener información de los videos virales
            videos = []
            video_elements = driver.find_elements(By.TAG_NAME, 'ytd-video-renderer')[:5]

            for element in video_elements:
                try:
                    title = element.find_element(By.ID, 'video-title').text
                    url = element.find_element(By.ID, 'video-title').get_attribute('href')
                    thumbnail = element.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    channel = element.find_element(By.CLASS_NAME, 'ytd-channel-name').text
                    
                    videos.append({
                        'title': title,
                        'url': url,
                        'thumbnail': thumbnail,
                        'channel': channel
                    })
                except Exception as e:
                    logger.error(f'Error al extraer información del video: {str(e)}')
                    continue

            return jsonify({'videos': videos})

        except Exception as e:
            logger.error(f'Error al obtener videos virales: {str(e)}')
            return jsonify({'error': 'Error al obtener videos virales'}), 500

        finally:
            if 'driver' in locals():
                driver.quit()

    except Exception as e:
        logger.error(f'Error general en videos virales: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)