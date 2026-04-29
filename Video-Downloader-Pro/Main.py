import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import yt_dlp
import time
import threading
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import cloudscraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sys
import instaloader
import webbrowser
from moviepy.editor import VideoFileClip
import re
from openai import OpenAI

# Actualizar la constante de API key para Deepseek
DEEPSEEK_API_KEY = "sk-e578e5cf4a2d47ceac0ff3fbc3c39b24"

class YouTubeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        
        # Configurar el tema y estilo
        self.root.configure(bg='#f0f0f0')  # Color de fondo suave
        style = ttk.Style()
        style.theme_use('clam')  # Usar tema moderno
        
        # Configurar estilos personalizados
        style.configure('Custom.TButton',
                       padding=10,
                       font=('Segoe UI', 9),
                       background='#ff0000',  # Rojo de YouTube
                       foreground='white')
        
        style.configure('Custom.TLabel',
                       padding=5,
                       font=('Segoe UI', 10))
        
        style.configure('Custom.TEntry',
                       padding=8,
                       font=('Segoe UI', 9))
        
        style.configure('Title.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground='#cc0000')  # Rojo más oscuro para títulos
        
        style.configure('Viral.TButton',
                       padding=12,
                       font=('Segoe UI', 11, 'bold'),
                       background='#ff0000',
                       foreground='white')
        
        style.map('Viral.TButton',
                  background=[('active', '#cc0000')],
                  foreground=[('active', 'white')])
        
        # Frame principal con padding y borde
        main_frame = ttk.Frame(root, padding="20", style='Card.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        
        # Título de la aplicación
        title_label = ttk.Label(main_frame, 
                               text="YouTube Downloader", 
                               style='Title.TLabel')
        title_label.grid(row=1, column=0, columnspan=3, pady=(0,20))
        
        # Nuevo estilo para el botón VIRAL NOW
        style.configure('Viral.TButton',
                       padding=12,
                       font=('Segoe UI', 11, 'bold'),
                       background='#ff0000',
                       foreground='white')
        
        style.map('Viral.TButton',
                  background=[('active', '#cc0000')],
                  foreground=[('active', 'white')])
        
        # Botón VIRAL NOW
        viral_frame = ttk.Frame(main_frame)
        viral_frame.grid(row=2, column=0, columnspan=3, sticky='ew', pady=(0,20))
        
        viral_button = ttk.Button(viral_frame,
                                 text="🔥 VIRAL NOW",
                                 command=self.show_viral_videos,
                                 style='Viral.TButton')
        viral_button.pack(fill=tk.X, pady=5)
        
        # Separar la interfaz en secciones
        channel_frame = ttk.LabelFrame(main_frame, text="Información del Canal", padding=10)
        channel_frame.grid(row=3, column=0, columnspan=3, sticky='ew', pady=(0,10))
        
        video_frame = ttk.LabelFrame(main_frame, text="Descarga de Videos", padding=10)
        video_frame.grid(row=4, column=0, columnspan=3, sticky='ew', pady=(0,10))
        
        segments_frame = ttk.LabelFrame(main_frame, text="Descarga por Segmentos", padding=10)
        segments_frame.grid(row=5, column=0, columnspan=3, sticky='ew', pady=(0,10))

        # Función para manejar el foco en los campos de entrada con estilo mejorado
        def on_entry_click(event, placeholder):
            entry = event.widget
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(foreground='black', font=('Segoe UI', 9))

        def on_focus_out(event, placeholder):
            entry = event.widget
            if entry.get().strip() == '':  # Verificar si está vacío considerando espacios
                entry.delete(0, tk.END)  # Limpiar cualquier espacio
                entry.insert(0, placeholder)
                entry.config(foreground='gray', font=('Segoe UI', 9, 'italic'))

        # Sección de Canal
        ttk.Label(channel_frame, text="URL del Canal:", style='Custom.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.channel_url = tk.StringVar()
        channel_entry = ttk.Entry(channel_frame, textvariable=self.channel_url, width=50, style='Custom.TEntry')
        channel_entry.grid(row=0, column=1, padx=5, sticky='ew')
        channel_placeholder = "Ej: @RakkoTech o youtube.com/@RakkoTech"
        channel_entry.insert(0, channel_placeholder)
        channel_entry.config(foreground='gray', font=('Segoe UI', 9, 'italic'))
        channel_entry.bind('<FocusIn>', lambda e: on_entry_click(e, channel_placeholder))
        channel_entry.bind('<FocusOut>', lambda e: on_focus_out(e, channel_placeholder))
        
        ttk.Button(channel_frame, 
                   text="Obtener Info", 
                   command=self.get_channel_info,
                   style='Custom.TButton').grid(row=0, column=2, padx=(5,0))

        # Sección de Video
        ttk.Label(video_frame, text="Buscar Video:", style='Custom.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.search_query = tk.StringVar()
        search_entry = ttk.Entry(video_frame, textvariable=self.search_query, width=50, style='Custom.TEntry')
        search_entry.grid(row=0, column=1, padx=5, sticky='ew')
        search_placeholder = "Ej: Tutorial Python"
        search_entry.insert(0, search_placeholder)
        search_entry.config(foreground='gray', font=('Segoe UI', 9, 'italic'))
        search_entry.bind('<FocusIn>', lambda e: on_entry_click(e, search_placeholder))
        search_entry.bind('<FocusOut>', lambda e: on_focus_out(e, search_placeholder))
        
        ttk.Button(video_frame, 
                   text="Buscar", 
                   command=self.search_video,
                   style='Custom.TButton').grid(row=0, column=2, padx=(5,0))

        ttk.Label(video_frame, text="URL del Video:", style='Custom.TLabel').grid(row=1, column=0, sticky=tk.W, pady=(10,0))
        self.video_url = tk.StringVar()
        url_entry = ttk.Entry(video_frame, textvariable=self.video_url, width=50, style='Custom.TEntry')
        url_entry.grid(row=1, column=1, padx=5, pady=(10,0), sticky='ew')
        url_placeholder = "Ej: https://www.youtube.com/watch?v=..."
        url_entry.insert(0, url_placeholder)
        url_entry.config(foreground='gray', font=('Segoe UI', 9, 'italic'))
        url_entry.bind('<FocusIn>', lambda e: on_entry_click(e, url_placeholder))
        url_entry.bind('<FocusOut>', lambda e: on_focus_out(e, url_placeholder))
        
        ttk.Button(video_frame, 
                   text="Descargar", 
                   command=self.download_video,
                   style='Custom.TButton').grid(row=1, column=2, padx=(5,0), pady=(10,0))

        # Sección de Segmentos
        segment_controls = ttk.Frame(segments_frame)
        segment_controls.grid(row=0, column=0, columnspan=3, sticky='ew')
        
        ttk.Label(segment_controls, text="Duración (seg):", style='Custom.TLabel').grid(row=0, column=0, padx=(0,10))
        self.segment_seconds = tk.StringVar()
        seconds_entry = ttk.Entry(segment_controls, textvariable=self.segment_seconds, width=10, style='Custom.TEntry')
        seconds_entry.grid(row=0, column=1)
        seconds_placeholder = "15"
        seconds_entry.insert(0, seconds_placeholder)
        seconds_entry.config(foreground='gray', font=('Segoe UI', 9, 'italic'))
        seconds_entry.bind('<FocusIn>', lambda e: on_entry_click(e, seconds_placeholder))
        seconds_entry.bind('<FocusOut>', lambda e: on_focus_out(e, seconds_placeholder))

        ttk.Label(segment_controls, text="Número de partes:", style='Custom.TLabel').grid(row=0, column=2, padx=10)
        self.segment_parts = tk.StringVar()
        parts_entry = ttk.Entry(segment_controls, textvariable=self.segment_parts, width=10, style='Custom.TEntry')
        parts_entry.grid(row=0, column=3)
        parts_placeholder = "3"
        parts_entry.insert(0, parts_placeholder)
        parts_entry.config(foreground='gray', font=('Segoe UI', 9, 'italic'))
        parts_entry.bind('<FocusIn>', lambda e: on_entry_click(e, parts_placeholder))
        parts_entry.bind('<FocusOut>', lambda e: on_focus_out(e, parts_placeholder))

        ttk.Button(segment_controls, 
                   text="Descargar Segmentos",
                   command=self.download_segments,
                   style='Custom.TButton').grid(row=0, column=4, padx=(10,0))

        # Botones inferiores
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        ttk.Button(bottom_frame, 
                   text="Cambiar Directorio",
                   command=self.change_directory,
                   style='Custom.TButton').grid(row=0, column=0, padx=10)
        
        ttk.Button(bottom_frame, 
                   text="Acerca de",
                   command=self.show_about,
                   style='Custom.TButton').grid(row=0, column=1, padx=10)

        ttk.Button(bottom_frame, 
                   text="Botón Inactivo",
                   command=lambda: None,  # No hace nada
                   style='Custom.TButton').grid(row=0, column=2, padx=10)

        # Configurar el directorio de descarga
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")

        # En el método __init__, agregar el botón para mostrar el diálogo
        ttk.Button(bottom_frame, 
                   text="IA YT",  # Cambio del texto del botón
                   command=self.show_summary_dialog,
                   style='Custom.TButton').grid(row=0, column=2, padx=10)

        # Agregar nueva sección para listas de reproducción después del video_frame
        playlist_frame = ttk.LabelFrame(main_frame, text="Descarga de Listas de Reproducción", padding=10)
        playlist_frame.grid(row=5, column=0, columnspan=3, sticky='ew', pady=(0,10))
        
        ttk.Label(playlist_frame, text="URL de Lista:", style='Custom.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.playlist_url = tk.StringVar()
        playlist_entry = ttk.Entry(playlist_frame, textvariable=self.playlist_url, width=50)
        playlist_entry.grid(row=0, column=1, padx=5, sticky='ew')
        playlist_placeholder = "Ej: https://www.youtube.com/playlist?list=..."
        playlist_entry.insert(0, playlist_placeholder)
        playlist_entry.config(foreground='gray', font=('Segoe UI', 9, 'italic'))
        
        # Aplicar eventos a la entrada de lista de reproducción
        playlist_entry.bind('<FocusIn>', lambda e: on_entry_click(e, playlist_placeholder))
        playlist_entry.bind('<FocusOut>', lambda e: on_focus_out(e, playlist_placeholder))
        
        ttk.Button(playlist_frame, 
                   text="Descargar Lista", 
                   command=self.download_playlist,
                   style='Custom.TButton').grid(row=0, column=2, padx=(5,0))
        
        # Sección para múltiples URLs
        multi_frame = ttk.LabelFrame(main_frame, text="Descarga Múltiple", padding=10)
        multi_frame.grid(row=6, column=0, columnspan=3, sticky='ew', pady=(0,10))
        
        # Área de texto para múltiples URLs
        self.multi_urls = tk.Text(multi_frame, height=4, width=40)
        self.multi_urls.pack(pady=5)
        self.multi_urls.insert('1.0', "Ingresa varias URLs (una por línea)")
        self.multi_urls.config(foreground='gray')
        
        def on_multi_focus_in(event):
            if self.multi_urls.get('1.0', 'end-1c') == "Ingresa varias URLs (una por línea)":
                self.multi_urls.delete('1.0', tk.END)
                self.multi_urls.config(foreground='black')
        
        def on_multi_focus_out(event):
            if not self.multi_urls.get('1.0', 'end-1c').strip():
                self.multi_urls.insert('1.0', "Ingresa varias URLs (una por línea)")
                self.multi_urls.config(foreground='gray')
        
        self.multi_urls.bind('<FocusIn>', on_multi_focus_in)
        self.multi_urls.bind('<FocusOut>', on_multi_focus_out)
        
        ttk.Button(multi_frame,
                   text="Descargar Todos",
                   command=self.download_multiple,
                   style='Custom.TButton').pack(pady=5)

    def change_directory(self):
        new_path = filedialog.askdirectory()
        if new_path:
            self.download_path = new_path

    def get_channel_info(self):
        try:
            url = self.channel_url.get()
            placeholder = "Ej: @RakkoTech o youtube.com/@RakkoTech"
            if not url or url == placeholder:
                messagebox.showwarning("Advertencia", "Por favor ingrese una URL o nombre de canal")
                return

            # Crear ventana de progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Obteniendo información...")
            progress_window.geometry("300x100")
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            status_label = ttk.Label(progress_window, text="Iniciando...")
            status_label.pack(pady=10)
            
            progress = ttk.Progressbar(progress_window, mode='indeterminate')
            progress.pack(pady=10, padx=10, fill=tk.X)
            progress.start()

            def update_status(text):
                if not progress_window.winfo_exists():
                    return
                status_label.config(text=text)
                progress_window.update()

            def show_error(error_msg, error_type="Error"):
                if progress_window.winfo_exists():
                    progress_window.destroy()
                if error_type == "Rate Limit":
                    messagebox.showwarning("Límite de Solicitudes", 
                                        "Se ha alcanzado el límite de solicitudes a SocialBlade.\n"
                                        "Por favor, espere unos minutos antes de intentar nuevamente.")
                else:
                    messagebox.showerror("Error", 
                                       "No se pudo obtener la información del canal.\n"
                                       "Por favor, verifica que el nombre o URL del canal sea correcto.\n"
                                       f"Error: {error_msg}")

            def process_channel_info():
                try:
                    progress_window.after(0, lambda: update_status("Buscando canal..."))
                    
                    # Preparar la URL del canal
                    channel_url = url
                    channel_id = None
                    channel_name = None

                    # Configurar yt-dlp
                    ydl_opts = {
                        'quiet': True,
                        'no_warnings': True,
                        'extract_flat': True,
                        'default_search': 'ytsearch'
                    }

                    try:
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            if '@' in url:
                                channel_url = f"https://www.youtube.com/@{url.split('@')[-1]}"
                                info = ydl.extract_info(channel_url, download=False)
                                channel_id = info.get('channel_id', '')
                                channel_name = info.get('uploader', '')
                            else:
                                info = ydl.extract_info(f"ytsearch:{url}", download=False)
                                if info.get('entries'):
                                    entry = info['entries'][0]
                                    channel_id = entry.get('channel_id', '')
                                    channel_name = entry.get('uploader', '')

                        if not channel_id:
                            raise Exception("No se pudo obtener el ID del canal")

                        # Implementar rate limiting básico
                        time.sleep(1)  # Esperar 1 segundo entre solicitudes

                        # Usar cloudscraper para obtener los datos de SocialBlade
                        progress_window.after(0, lambda: update_status("Accediendo a SocialBlade..."))
                        socialblade_url = f"https://socialblade.com/youtube/channel/{channel_id}"
                        
                        scraper = cloudscraper.create_scraper()
                        response = scraper.get(socialblade_url)
                        
                        if response.status_code == 429:  # Too Many Requests
                            raise Exception("Rate Limit")
                        elif response.status_code != 200:
                            raise Exception(f"Error al acceder a SocialBlade: {response.status_code}")

                        progress_window.after(0, lambda: update_status("Extrayendo datos..."))
                        soup = BeautifulSoup(response.text, 'html.parser')

                        # Extraer datos usando BeautifulSoup con manejo de errores mejorado
                        stats = self._extract_channel_stats(soup)

                        # Formatear la información para mostrar
                        channel_info = {
                            'channel_name': channel_name,
                            'channel_id': channel_id,
                            'Subscribers': stats.get('Subscribers', 'No disponible'),
                            'Video Views': stats.get('Video Views', 'No disponible'),
                            'Uploads': stats.get('Uploads', 'No disponible'),
                            'Country': stats.get('Country', 'No disponible'),
                            'Channel Type': stats.get('Channel Type', 'No disponible'),
                            'User Created': stats.get('User Created', 'No disponible')
                        }

                        def show_results():
                            if progress_window.winfo_exists():
                                progress_window.destroy()
                            self.show_channel_info(channel_info)

                        progress_window.after(0, show_results)

                    except Exception as e:
                        error_type = "Rate Limit" if str(e) == "Rate Limit" else "Error"
                        progress_window.after(0, lambda: show_error(str(e), error_type))
                        print(f"Error al obtener información del canal: {str(e)}")

                except Exception as e:
                    error_msg = str(e)
                    progress_window.after(0, lambda: show_error(error_msg))
                    print(f"Error detallado: {error_msg}")

            # Iniciar el proceso en un hilo separado
            threading.Thread(target=process_channel_info, daemon=True).start()

        except Exception as e:
            if 'progress_window' in locals():
                progress_window.destroy()
            messagebox.showerror("Error", 
                                "No se pudo obtener la información del canal.\n"
                                "Por favor, verifica que el nombre o URL del canal sea correcto.\n"
                                f"Error: {str(e)}")
            print(f"Error detallado: {str(e)}")

    def _extract_channel_stats(self, soup):
        """Extraer estadísticas del canal desde el HTML de SocialBlade"""
        stats = {}
        try:
            info_divs = soup.find_all('div', class_='YouTubeUserTopInfo')
            for div in info_divs:
                text = div.get_text()
                for key in ['Uploads', 'Subscribers', 'Video Views', 'Country', 'Channel Type', 'User Created']:
                    if key in text:
                        value_element = div.find('a') if div.find('a') else div.find('span', style='font-weight: bold;')
                        if value_element:
                            stats[key] = value_element.text.strip()
            
            if not stats:
                raise Exception("No se encontraron datos del canal")
                
        except Exception as e:
            print(f"Error al extraer datos: {str(e)}")
            raise Exception

    def show_channel_info(self, channel_info):
        """Mostrar información del canal en una ventana más visual"""
        try:
            info_window = tk.Toplevel(self.root)
            info_window.title("Información del Canal")
            info_window.geometry("400x350")
            info_window.resizable(False, False)
            
            # Estilo para la ventana
            style = ttk.Style()
            style.configure('Info.TLabel',
                           font=('Segoe UI', 10),
                           padding=5)
            style.configure('InfoTitle.TLabel',
                           font=('Segoe UI', 12, 'bold'),
                           foreground='#cc0000',
                           padding=5)
            style.configure('InfoValue.TLabel',
                           font=('Segoe UI', 10),
                           foreground='#666666',
                           padding=5)
            
            # Frame principal
            main_frame = ttk.Frame(info_window, padding=20)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Grid para organizar la información
            main_frame.columnconfigure(1, weight=1)
            
            # Título del canal
            channel_name = channel_info.get('channel_name', 'Desconocido')
            ttk.Label(main_frame, 
                      text=f"Canal: {channel_name}", 
                      style='InfoTitle.TLabel').grid(row=0, column=0, columnspan=2, sticky='w', pady=(0,10))
            
            # Función para limpiar y formatear valores
            def format_value(key, value):
                if value == 'No disponible':
                    return value
                if 'Country' in key:
                    return value.replace('Country', '').strip()
                elif 'Channel Type' in key:
                    return value.replace('Channel Type', '').strip()
                elif 'User Created' in key:
                    return value.replace('User Created', '').strip()
                return value

            # Información del canal
            info_data = [
                ("ID del Canal:", channel_info.get('channel_id', 'No disponible')),
                ("Suscriptores:", channel_info.get('Subscribers', 'No disponible')),
                ("Total de vistas:", channel_info.get('Video Views', 'No disponible')),
                ("Videos subidos:", channel_info.get('Uploads', 'No disponible')),
                ("País:", format_value('Country', channel_info.get('Country', 'No disponible'))),
                ("Tipo de canal:", format_value('Channel Type', channel_info.get('Channel Type', 'No disponible'))),
                ("Creado el:", format_value('User Created', channel_info.get('User Created', 'No disponible')))
            ]
            
            # Agregar cada línea de información
            for i, (label, value) in enumerate(info_data):
                ttk.Label(main_frame, 
                         text=label, 
                         style='Info.TLabel').grid(row=i+1, column=0, sticky='w', pady=2)
                ttk.Label(main_frame, 
                         text=value, 
                         style='InfoValue.TLabel').grid(row=i+1, column=1, sticky='w', pady=2)
            
            # Botones de acción
            button_frame = ttk.Frame(main_frame)
            button_frame.grid(row=len(info_data)+1, column=0, columnspan=2, pady=(20,0))
            
            # Botón para abrir el canal en el navegador
            if channel_info.get('channel_id'):
                ttk.Button(button_frame, 
                          text="Abrir Canal",
                          command=lambda: webbrowser.open(f"https://www.youtube.com/channel/{channel_info['channel_id']}"),
                          style='Custom.TButton').pack(side=tk.LEFT, padx=5)
            
            # Botón de cerrar
            ttk.Button(button_frame, 
                       text="Cerrar",
                       command=info_window.destroy,
                       style='Custom.TButton').pack(side=tk.LEFT, padx=5)
            
            # Centrar la ventana en la pantalla
            info_window.update_idletasks()
            width = info_window.winfo_width()
            height = info_window.winfo_height()
            x = (info_window.winfo_screenwidth() // 2) - (width // 2)
            y = (info_window.winfo_screenheight() // 2) - (height // 2)
            info_window.geometry(f"{width}x{height}+{x}+{y}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar información del canal: {str(e)}")
            print(f"Error al mostrar información del canal: {str(e)}")


    def search_video(self):
        try:
            search_query = self.search_query.get()
            placeholder = "Ej: Tutorial Python"
            if not search_query or search_query == placeholder:
                messagebox.showwarning("Advertencia", "Por favor ingrese un término de búsqueda")
                return

            # Configuración de yt-dlp para búsqueda
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'format': 'best',
            }

            # Realizar la búsqueda
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                results = ydl.extract_info(f"ytsearch5:{search_query}", download=False)['entries']

            if not results:
                messagebox.showinfo("Búsqueda", "No se encontraron resultados")
                return

            # Crear ventana de resultados
            results_window = tk.Toplevel(self.root)
            results_window.title("Resultados de búsqueda")
            results_window.geometry("600x400")
            
            # Hacer que la ventana sea modal
            results_window.transient(self.root)
            results_window.grab_set()
            
            # Scroll frame para los resultados
            canvas = tk.Canvas(results_window)
            scrollbar = ttk.Scrollbar(results_window, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for video in results:
                frame = ttk.Frame(scrollable_frame)
                frame.pack(pady=5, padx=5, fill=tk.X)
                
                # Mostrar título y duración
                duration = str(video.get('duration', 'Duración desconocida'))
                if duration.isdigit():
                    minutes = int(duration) // 60
                    seconds = int(duration) % 60
                    duration = f"{minutes}:{seconds:02d}"
                
                title_text = f"{video['title']} ({duration})"
                ttk.Label(frame, text=title_text, wraplength=500).pack(side=tk.LEFT, padx=5)
                
                # Obtener la URL del video
                video_url = f"https://www.youtube.com/watch?v={video['id']}"
                
                # Botón de descarga que pasa la URL del video
                ttk.Button(frame, text="Descargar", 
                          command=lambda v=video_url: self.download_from_search(v)).pack(side=tk.RIGHT)

            # Empaquetar el canvas y la scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        except Exception as e:
            messagebox.showerror("Error", f"Error en la búsqueda: {str(e)}")
            print(f"Error detallado: {str(e)}")  # Para debugging

    def download_from_search(self, video_url):
        """Función auxiliar para descargar desde la búsqueda"""
        self.video_url.set(video_url)
        self.download_video()  # Esto ahora mostrará el selector de calidad

    def get_available_formats(self, url):
        """Obtener formatos disponibles para el video"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                
                # Conjunto para almacenar calidades únicas
                available_qualities = set()
                
                # Buscar formatos de video disponibles
                for f in formats:
                    height = f.get('height', 0)
                    ext = f.get('ext', '')
                    if height and ext in ['mp4', 'webm']:
                        if height >= 2160:  # 4K
                            available_qualities.add(f'4K (2160p) .{ext.upper()}')
                        elif height >= 1440:  # 2K
                            available_qualities.add(f'2K (1440p) .{ext.upper()}')
                        elif height >= 1080:
                            available_qualities.add(f'Alta (1080p) .{ext.upper()}')
                        elif height >= 720:
                            available_qualities.add(f'Media (720p) .{ext.upper()}')
                        elif height >= 480:
                            available_qualities.add(f'Baja (480p) .{ext.upper()}')
                
                # Agregar opción de audio
                available_qualities.add('Solo Audio .MP3')
                
                # Convertir a lista ordenada
                qualities = sorted(list(available_qualities), 
                                key=lambda x: (
                                    '4K' in x, '2K' in x, 
                                    'Alta' in x, 'Media' in x, 
                                    'Baja' in x, 'Solo' in x
                                ), 
                                reverse=True)
                
                return qualities
        except Exception as e:
            print(f"Error al obtener formatos: {str(e)}")
            return []

    def show_quality_selector(self, url, callback):
        """Mostrar selector de calidad"""
        quality_window = tk.Toplevel(self.root)
        quality_window.title("Seleccionar Calidad")
        quality_window.geometry("300x400")
        quality_window.transient(self.root)
        quality_window.grab_set()
        
        # Mostrar mensaje de carga
        loading_label = ttk.Label(quality_window, text="Obteniendo calidades disponibles...")
        loading_label.pack(pady=10)
        
        def load_qualities():
            qualities = self.get_available_formats(url)
            loading_label.destroy()
            
            if not qualities:
                messagebox.showerror("Error", "No se pudieron obtener las calidades disponibles")
                quality_window.destroy()
                return
            
            # Crear frame con scroll
            canvas = tk.Canvas(quality_window)
            scrollbar = ttk.Scrollbar(quality_window, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            def select_quality(quality):
                quality_window.destroy()
                callback(quality)
            
            # Agregar botones para cada calidad
            for quality in qualities:
                ttk.Button(scrollable_frame, 
                          text=quality,
                          width=30,
                          command=lambda q=quality: select_quality(q)).pack(pady=2)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        
        # Cargar calidades en un hilo separado
        threading.Thread(target=load_qualities, daemon=True).start()

    def download_video(self):
        try:
            url = self.video_url.get()
            placeholder = "Ej: https://www.youtube.com/watch?v=..."
            if not url or url == placeholder:
                messagebox.showwarning("Advertencia", "Por favor ingrese una URL")
                return

            # Validar URL de YouTube
            if not ('youtube.com' in url or 'youtu.be' in url):
                messagebox.showerror("Error", "Por favor ingrese una URL válida de YouTube")
                return

            # Mostrar selector de calidad con manejo mejorado de errores
            self.show_quality_selector(url, self.start_download)

        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar la descarga: {str(e)}")

    def start_download(self, selected_quality):
        try:
            url = self.video_url.get()
            
            # Configuración base de yt-dlp con opciones simplificadas
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'nocheckcertificate': True,
                'writeinfojson': True,  # Guardar metadatos del video incluyendo dimensiones
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                },
                'socket_timeout': 30,
                'retries': 5,
                'ignoreerrors': False,
                'no_color': True,
                'format_sort': ['res:2160', 'res:1440', 'res:1080', 'ext:mp4:m4a', 'codec:h264', 'quality'],
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4'  # Asegurar que el formato de salida sea MP4
            }

            if selected_quality == "Solo Audio .MP3":
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                # Extraer dimensiones del formato seleccionado
                height = '2160' if '4K' in selected_quality else \
                        '1440' if '2K' in selected_quality else \
                        '1080' if 'Alta' in selected_quality else \
                        '720' if 'Media' in selected_quality else '480'
                ext = 'mp4' if '.MP4' in selected_quality else 'webm'
                
                # Formato con dimensiones específicas
                ydl_opts['format'] = f'bestvideo[height<={height}][ext={ext}]+bestaudio/best[height<={height}]'

            # Ventana de progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Descargando...")
            progress_window.geometry("300x150")
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            progress_label = ttk.Label(progress_window, text="Preparando descarga...")
            progress_label.pack(pady=10)
            
            progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(progress_window, 
                                         mode='determinate',
                                         variable=progress_var,
                                         maximum=100)
            progress_bar.pack(pady=10, padx=10, fill=tk.X)
            
            percent_label = ttk.Label(progress_window, text="0%")
            percent_label.pack(pady=5)

            def update_progress(d):
                if not progress_window.winfo_exists():
                    return
                
                if d['status'] == 'downloading':
                    try:
                        total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                        if total > 0:
                            downloaded = d.get('downloaded_bytes', 0)
                            percentage = (downloaded / total) * 100
                            progress_var.set(percentage)
                            percent_label.config(text=f"{percentage:.1f}%")
                            
                            speed = d.get('speed', 0)
                            if speed:
                                speed_mb = speed / 1024 / 1024
                                progress_label.config(text=f"Descargando... ({speed_mb:.1f} MB/s)")
                    except Exception:
                        pass
                elif d['status'] == 'finished':
                    progress_var.set(100)
                    percent_label.config(text="100%")
                    progress_label.config(text="Procesando...")

            def download():
                try:
                    # Intentar descarga directa sin usar versión móvil
                    ydl_opts['progress_hooks'] = [update_progress]
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        # Obtener información del video
                        info = ydl.extract_info(url, download=False)
                        filename = ydl.prepare_filename(info)
                        
                        if selected_quality == "Solo Audio .MP3":
                            filename = os.path.splitext(filename)[0] + '.mp3'
                        file_path = os.path.join(self.download_path, os.path.basename(filename))
                        
                        # Intentar la descarga
                        ydl.download([url])
                        
                        if os.path.exists(file_path):
                            # Actualizar la fecha de modificación al momento actual
                            current_time = time.time()
                            os.utime(file_path, (current_time, current_time))
                            
                            if progress_window.winfo_exists():
                                progress_window.destroy()
                            messagebox.showinfo("Éxito", 
                                              "Video descargado correctamente\n\n"
                                              f"Ubicación: {file_path}")
                            return
                        else:
                            raise Exception("El archivo no se descargó correctamente")
                        
                except Exception as e:
                    if progress_window.winfo_exists():
                        progress_window.destroy()
                    messagebox.showerror("Error", 
                                       "No se pudo descargar el video.\n"
                                       f"Error: {str(e)}")

            # Iniciar descarga en un hilo separado
            threading.Thread(target=download, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar la descarga: {str(e)}")

    def download_segments(self):
        try:
            url = self.video_url.get()
            seconds = self.segment_seconds.get()
            parts = self.segment_parts.get()
            url_placeholder = "Ej: https://www.youtube.com/watch?v=..."
            seconds_placeholder = "Ej: 15"
            parts_placeholder = "Ej: 3"

            if (not url or url == url_placeholder or 
                not seconds or seconds == seconds_placeholder or 
                not parts or parts == parts_placeholder):
                messagebox.showwarning("Advertencia", "Por favor complete todos los campos")
                return

            # Validar URL de YouTube
            if not ('youtube.com' in url or 'youtu.be' in url):
                messagebox.showerror("Error", "Por favor ingrese una URL válida de YouTube")
                return

            # Validar que los valores sean numéricos
            try:
                seconds = int(seconds)
                parts = int(parts)
            except ValueError:
                messagebox.showerror("Error", "Los valores de duración y partes deben ser números")
                return

            # Mostrar selector de calidad para los segmentos
            self.show_quality_selector(url, lambda quality: self.start_segments_download(url, seconds, parts, quality))

        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar la descarga de segmentos: {str(e)}")

    def start_segments_download(self, url, seconds, parts, selected_quality):
        try:
            # Crear ventana de progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Procesando segmentos...")
            progress_window.geometry("400x300")
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            status_label = ttk.Label(progress_window, text="Descargando video completo...")
            status_label.pack(pady=10)
            
            progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(progress_window, 
                                         mode='determinate',
                                         variable=progress_var,
                                         maximum=100)
            progress_bar.pack(pady=10, padx=10, fill=tk.X)
            
            # Frame para la lista de segmentos
            segments_frame = ttk.Frame(progress_window)
            segments_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Canvas y scrollbar para la lista de segmentos
            canvas = tk.Canvas(segments_frame)
            scrollbar = ttk.Scrollbar(segments_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            def update_progress(d):
                if not progress_window.winfo_exists():
                    return
                
                if d['status'] == 'downloading':
                    try:
                        total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                        if total > 0:
                            downloaded = d.get('downloaded_bytes', 0)
                            percentage = (downloaded / total) * 100
                            progress_var.set(percentage)
                            
                            speed = d.get('speed', 0)
                            if speed:
                                speed_mb = speed / 1024 / 1024
                                status_label.config(text=f"Descargando... ({speed_mb:.1f} MB/s)")
                    except Exception:
                        pass
                elif d['status'] == 'finished':
                    progress_var.set(100)
                    status_label.config(text="Procesando segmentos...")
            
            def process_segments():
                try:
                    # Configurar opciones de descarga
                    ydl_opts = {
                        'quiet': True,
                        'no_warnings': True,
                        'outtmpl': os.path.join(self.download_path, 'temp_video.%(ext)s'),
                        'writeinfojson': True,  # Guardar metadatos del video incluyendo dimensiones
                        'progress_hooks': [update_progress],
                        'nocheckcertificate': True,
                        'socket_timeout': 30,
                        'retries': 5
                    }
                    
                    if "Solo Audio .MP3" in selected_quality:
                        ydl_opts.update({
                            'format': 'bestaudio/best',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                        })
                    else:
                        # Extraer dimensiones del formato seleccionado
                        height = '2160' if '4K' in selected_quality else \
                                '1440' if '2K' in selected_quality else \
                                '1080' if 'Alta' in selected_quality else \
                                '720' if 'Media' in selected_quality else '480'
                        ext = 'mp4' if '.MP4' in selected_quality else 'webm'
                        
                        # Formato con dimensiones específicas
                        ydl_opts['format'] = f'bestvideo[height<={height}][ext={ext}]+bestaudio/best[height<={height}]'
                    
                    # Descargar video completo
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        video_title = info.get('title', 'video')
                        ext = info.get('ext', 'mp4')
                        temp_file = os.path.join(self.download_path, f'temp_video.{ext}')
                    
                    if not os.path.exists(temp_file):
                        raise Exception("No se pudo descargar el video completo")
                    
                    # Procesar segmentos
                    with VideoFileClip(temp_file) as video:
                        duration = video.duration
                        segment_duration = seconds
                        
                        # Calcular puntos de inicio para cada segmento
                        if parts > 1:
                            # Distribuir uniformemente
                            start_points = [i * (duration - segment_duration) / (parts - 1) for i in range(parts)]
                        else:
                            # Solo un segmento desde el inicio
                            start_points = [0]
                        
                        # Crear cada segmento
                        for i, start in enumerate(start_points):
                            if not progress_window.winfo_exists():
                                break
                            
                            # Crear etiqueta para este segmento
                            segment_label = ttk.Label(scrollable_frame, 
                                                    text=f"Segmento {i+1}: {int(start)}s - {int(start + segment_duration)}s")
                            segment_label.pack(anchor=tk.W, pady=2)
                            
                            # Extraer segmento
                            segment = video.subclip(start, start + segment_duration)
                            
                            # Nombre del archivo de salida
                            output_file = os.path.join(
                                self.download_path, 
                                f"{video_title}_segmento_{i+1}_{int(start)}s-{int(start + segment_duration)}s.{ext}"
                            )
                            
                            # Guardar segmento
                            segment.write_videofile(
                                output_file,
                                codec="libx264",
                                audio_codec="aac",
                                temp_audiofile=os.path.join(self.download_path, "temp-audio.m4a"),
                                remove_temp=True,
                                preset='ultrafast',  # Más rápido pero menos compresión
                                threads=2,
                                logger=None  # Silenciar logs
                            )
                            
                            segment_label.config(text=f"Segmento {i+1}: {int(start)}s - {int(start + segment_duration)}s ✓")
                    
                    # Eliminar archivo temporal
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    
                    # Actualizar la fecha de modificación de los segmentos al momento actual
                    try:
                        for i, start in enumerate(start_points):
                            output_file = os.path.join(
                                self.download_path, 
                                f"{video_title}_segmento_{i+1}_{int(start)}s-{int(start + segment_duration)}s.{ext}"
                            )
                            if os.path.exists(output_file):
                                current_time = time.time()
                                os.utime(output_file, (current_time, current_time))
                    except Exception as file_error:
                        print(f"Error al actualizar fecha de archivos de segmentos: {str(file_error)}")
                    
                    if progress_window.winfo_exists():
                        progress_window.destroy()
                    
                    messagebox.showinfo("Éxito", 
                                      f"Se han creado {parts} segmentos correctamente\n\n"
                                      f"Ubicación: {self.download_path}")
                    
                except Exception as e:
                    if progress_window.winfo_exists():
                        progress_window.destroy()
                    messagebox.showerror("Error", 
                                       "No se pudieron crear los segmentos.\n"
                                       f"Error: {str(e)}")
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Iniciar procesamiento en un hilo separado
            threading.Thread(target=process_segments, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar el proceso: {str(e)}")

    @staticmethod
    def sanitize_filename(filename):
        # Eliminar caracteres no permitidos en nombres de archivo
        return re.sub(r'[<>:"/\\|?*]', '', filename)

    def show_about(self):
        messagebox.showinfo("Acerca de", 
                          "YouTube Downloader v1.0\n"
                          "Desarrollado con Python y tkinter\n"
                          "© 2025")

    def show_viral_videos(self):
        """Mostrar videos virales actuales"""
        viral_window = tk.Toplevel(self.root)
        viral_window.title("Videos Virales")
        viral_window.geometry("800x600")
        
        # Frame principal
        main_frame = ttk.Frame(viral_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, 
                 text="🔥 Videos Virales del Momento",
                 style='Title.TLabel').pack(pady=(0,20))
        
        # Lista de videos con scroll
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas para scroll
        canvas = tk.Canvas(list_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configurar scrollbar
        scrollbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)
        
        # Frame para contenido
        content_frame = ttk.Frame(canvas)
        canvas.create_window((0,0), window=content_frame, anchor='nw')
        
        # Mostrar mensaje de carga
        loading_label = ttk.Label(content_frame, text="Cargando videos virales...", style='Info.TLabel')
        loading_label.pack(pady=20)
        
        def format_views(views):
            try:
                views = int(str(views).replace(',', ''))
                if views >= 1000000:
                    return f"{views/1000000:.1f}M"
                elif views >= 1000:
                    return f"{views/1000:.1f}K"
                return str(views)
            except:
                return str(views)
        
        def format_duration(seconds):
            if not seconds:
                return "00:00"
            return time.strftime('%H:%M:%S', time.gmtime(seconds))
        
        def get_viral_videos():
            try:
                # Configurar yt-dlp
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': True
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Obtener videos de tendencias
                    info = ydl.extract_info("https://www.youtube.com/feed/trending", download=False)
                    
                    # Eliminar mensaje de carga
                    loading_label.destroy()
                    
                    if 'entries' in info:
                        for i, video in enumerate(info['entries'][:20]):
                            # Frame para cada video
                            video_frame = ttk.Frame(content_frame)
                            video_frame.pack(fill=tk.X, pady=5, padx=5)
                            
                            # Información del video
                            title = video.get('title', 'Sin título')
                            channel = video.get('uploader', 'Canal desconocido')
                            views = format_views(video.get('view_count', 0))
                            duration = format_duration(video.get('duration', 0))
                            
                            ttk.Label(video_frame, 
                                    text=f"{i+1}. {title}",
                                    wraplength=600,
                                    style='Info.TLabel').pack(anchor='w')
                            
                            ttk.Label(video_frame,
                                    text=f"👤 {channel} | 👁️ {views} vistas | ⏱️ {duration}",
                                    style='Info.TLabel').pack(anchor='w')
                            
                            # Botón para descargar
                            ttk.Button(video_frame,
                                     text="Descargar",
                                     command=lambda url=video['url']: self.download_viral_video(url),
                                     style='Custom.TButton').pack(anchor='w', pady=5)
                            
                            # Separador
                            ttk.Separator(video_frame, orient='horizontal').pack(fill=tk.X, pady=5)
            
            except Exception as e:
                loading_label.config(text=f"Error al cargar videos: {str(e)}")
        
        # Cargar videos en un hilo separado
        threading.Thread(target=get_viral_videos, daemon=True).start()
        
        # Actualizar scroll region
        content_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Centrar ventana
        viral_window.update_idletasks()
        width = viral_window.winfo_width()
        height = viral_window.winfo_height()
        x = (viral_window.winfo_screenwidth() // 2) - (width // 2)
        y = (viral_window.winfo_screenheight() // 2) - (height // 2)
        viral_window.geometry(f'{width}x{height}+{x}+{y}')

    def download_viral_video(self, url):
        """Descargar video viral de YouTube"""
        try:
            # Configurar opciones de yt-dlp
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'ignoreerrors': True
            }
            
            # Mostrar ventana de progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Descargando")
            progress_window.geometry("300x100")
            
            progress_label = ttk.Label(progress_window, text="Descargando video...")
            progress_label.pack(pady=20)
            
            def download():
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                        # Actualizar la fecha de modificación al momento actual
                        try:
                            files = [os.path.join(self.download_path, f) for f in os.listdir(self.download_path)]
                            if files:
                                files.sort(key=os.path.getmtime, reverse=True)
                                current_time = time.time()
                                os.utime(files[0], (current_time, current_time))
                        except Exception as file_error:
                            print(f"Error al actualizar fecha de archivo: {str(file_error)}")
                    progress_window.destroy()
                    messagebox.showinfo("Éxito", "Video descargado correctamente")
                except Exception as e:
                    progress_window.destroy()
                    messagebox.showerror("Error", f"Error al descargar: {str(e)}")
            
            threading.Thread(target=download, daemon=True).start()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar la descarga: {str(e)}")

    def download_story(self, url):
        """Descargar historia de Instagram"""
        try:
            # Configurar opciones de yt-dlp
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(self.download_path, 'stories/%(uploader)s/%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'cookiesfrombrowser': ('chrome',),
                'ignoreerrors': True
            }
            
            # Crear directorio para historias si no existe
            stories_dir = os.path.join(self.download_path, 'stories')
            if not os.path.exists(stories_dir):
                os.makedirs(stories_dir)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Mostrar progreso
                progress_window = tk.Toplevel(self.root)
                progress_window.title("Descargando")
                progress_window.geometry("300x100")
                
                progress_label = ttk.Label(progress_window, text="Descargando historia...")
                progress_label.pack(pady=20)
                
                # Descargar en un hilo separado
                def download():
                    try:
                        ydl.download([url])
                        # Actualizar la fecha de modificación al momento actual
                        try:
                            # Buscar archivos recién descargados en el directorio de historias
                            stories_dir = os.path.join(self.download_path, 'stories')
                            for root, dirs, files in os.walk(stories_dir):
                                for file in files:
                                    file_path = os.path.join(root, file)
                                    # Actualizar la fecha de modificación al momento actual
                                    current_time = time.time()
                                    os.utime(file_path, (current_time, current_time))
                        except Exception as file_error:
                            print(f"Error al actualizar fecha de archivo: {str(file_error)}")
                        progress_window.destroy()
                        messagebox.showinfo("Éxito", "Historia descargada correctamente")
                    except Exception as e:
                        progress_window.destroy()
                        messagebox.showerror("Error", f"Error al descargar: {str(e)}")
                
                threading.Thread(target=download, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar la descarga: {str(e)}")

    def get_stories(self):
        """Obtener historias de un usuario"""
        username = self.username.get()
        if username == "Ej: username" or username.strip() == "":  # Verificar también espacios
            messagebox.showerror("Error", "Por favor ingresa un nombre de usuario válido")
            return
        
        try:
            # Mostrar ventana de progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Cargando")
            progress_window.geometry("300x100")
            
            progress_label = ttk.Label(progress_window, text="Iniciando sesión...")
            progress_label.pack(pady=20)
            
            def get_stories_thread():
                try:
                    # Crear instancia de instaloader
                    L = instaloader.Instaloader(
                        download_videos=True,
                        download_video_thumbnails=False,
                        download_geotags=False,
                        download_comments=False,
                        save_metadata=False,
                        compress_json=False
                    )
                    
                    def show_2fa_dialog():
                        """Mostrar diálogo para código de verificación"""
                        dialog = tk.Toplevel(self.root)
                        dialog.title("Verificación de dos factores")
                        dialog.geometry("300x150")
                        
                        # Hacer la ventana modal
                        dialog.transient(self.root)
                        dialog.grab_set()
                        
                        ttk.Label(dialog, 
                                 text="Por favor ingresa el código de verificación\nque recibiste en tu teléfono:",
                                 wraplength=250,
                                 justify='center').pack(pady=10)
                        
                        code_var = tk.StringVar()
                        code_entry = ttk.Entry(dialog, textvariable=code_var, width=10, justify='center')
                        code_entry.pack(pady=10)
                        code_entry.focus()
                        
                        result = [None]  # Para almacenar el resultado
                        
                        def submit():
                            result[0] = code_var.get()
                            dialog.destroy()
                        
                        def cancel():
                            dialog.destroy()
                        
                        button_frame = ttk.Frame(dialog)
                        button_frame.pack(pady=10)
                        
                        ttk.Button(button_frame, text="Aceptar", command=submit).pack(side=tk.LEFT, padx=5)
                        ttk.Button(button_frame, text="Cancelar", command=cancel).pack(side=tk.LEFT, padx=5)
                        
                        # Esperar hasta que se cierre el diálogo
                        dialog.wait_window()
                        
                        return result[0]
                    
                    try:
                        # Intentar login
                        L.login('sum_maps', 'Yoelrambo15')
                    except instaloader.exceptions.TwoFactorAuthRequiredException:
                        # Solicitar código 2FA
                        progress_label.config(text="Esperando código de verificación...")
                        code = self.show_2fa_dialog()  # Usar self.show_2fa_dialog
                        if code:
                            try:
                                L.two_factor_login(code)
                                progress_label.config(text="Obteniendo historias...")
                            except Exception as e:
                                progress_window.destroy()
                                messagebox.showerror("Error", f"Código incorrecto: {str(e)}")
                                return
                        else:
                            progress_window.destroy()
                            return
                    except Exception as e:
                        progress_window.destroy()
                        messagebox.showerror("Error", f"Error al iniciar sesión: {str(e)}")
                        return
                    
                    try:
                        # Obtener perfil
                        profile = instaloader.Profile.from_username(L.context, username)
                        
                        # Obtener historias
                        stories = L.get_stories([profile.userid])
                        story_items = []
                        
                        # Recopilar todas las historias
                        for story in stories:
                            story_items.extend(story.get_items())
                        
                        # Cerrar ventana de progreso
                        progress_window.destroy()
                        
                        if story_items:
                            # Mostrar ventana con las historias
                            stories_window = tk.Toplevel(self.root)
                            stories_window.title(f"Historias de {username}")
                            stories_window.geometry("600x500")
                            
                            # Frame principal
                            main_frame = ttk.Frame(stories_window, padding=20)
                            main_frame.pack(fill=tk.BOTH, expand=True)
                            
                            # Lista con scroll
                            list_frame = ttk.Frame(main_frame)
                            list_frame.pack(fill=tk.BOTH, expand=True)
                            
                            scrollbar = ttk.Scrollbar(list_frame)
                            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                            
                            canvas = tk.Canvas(list_frame)
                            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                            
                            scrollbar.config(command=canvas.yview)
                            canvas.config(yscrollcommand=scrollbar.set)
                            
                            content_frame = ttk.Frame(canvas)
                            canvas.create_window((0,0), window=content_frame, anchor='nw')
                            
                            # Mostrar cada historia
                            for i, story in enumerate(story_items, 1):
                                story_frame = ttk.Frame(content_frame)
                                story_frame.pack(fill=tk.X, pady=5, padx=5)
                                
                                # Determinar tipo de historia
                                story_type = "Video" if story.is_video else "Foto"
                                date = story.date.strftime("%Y-%m-%d %H:%M")
                                
                                ttk.Label(story_frame,
                                        text=f"Historia {i} ({story_type}) - {date}",
                                        style='Info.TLabel').pack(anchor='w')
                                
                                # Frame para botones
                                buttons_frame = ttk.Frame(story_frame)
                                buttons_frame.pack(anchor='w', pady=5)
                                
                                # Botón para ver
                                ttk.Button(buttons_frame,
                                         text="Ver",
                                         command=lambda s=story: self.view_story(s),
                                         style='Custom.TButton').pack(side=tk.LEFT, padx=(0,5))
                                
                                # Botón para descargar
                                ttk.Button(buttons_frame,
                                         text="Descargar",
                                         command=lambda s=story: self.download_story_item(s),
                                         style='Custom.TButton').pack(side=tk.LEFT)
                                
                                ttk.Separator(story_frame, 
                                            orient='horizontal').pack(fill=tk.X, pady=5)
                            
                            # Actualizar scroll region
                            content_frame.bind('<Configure>', 
                                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                        else:
                            messagebox.showinfo("Historias", "No se encontraron historias activas")
                    
                    except Exception as e:
                        progress_window.destroy()
                        messagebox.showerror("Error", f"Error al obtener historias: {str(e)}")
                
                except Exception as e:
                    progress_window.destroy()
                    messagebox.showerror("Error", f"Error: {str(e)}")
            
            # Ejecutar en un hilo separado
            threading.Thread(target=get_stories_thread, daemon=True).start()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar: {str(e)}")

    def download_story_item(self, story):
        """Descargar historia individual"""
        try:
            # Crear directorio para historias si no existe
            stories_dir = os.path.join(self.download_path, 'stories', story.owner_username)
            if not os.path.exists(stories_dir):
                os.makedirs(stories_dir)
            
            # Mostrar progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Descargando")
            progress_window.geometry("300x100")
            
            progress_label = ttk.Label(progress_window, text="Descargando historia...")
            progress_label.pack(pady=20)
            
            def download():
                try:
                    # Determinar nombre del archivo
                    date_str = story.date.strftime("%Y%m%d_%H%M%S")
                    ext = "mp4" if story.is_video else "jpg"
                    filename = f"{date_str}.{ext}"
                    filepath = os.path.join(stories_dir, filename)
                    
                    # Descargar el archivo usando requests
                    if story.is_video:
                        url = story.video_url
                    else:
                        url = story.url
                    
                    response = requests.get(url, stream=True)
                    response.raise_for_status()
                    
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    # Actualizar la fecha de modificación al momento actual
                    current_time = time.time()
                    os.utime(filepath, (current_time, current_time))
                    
                    progress_window.destroy()
                    messagebox.showinfo("Éxito", "Historia descargada correctamente")
                except Exception as e:
                    progress_window.destroy()
                    messagebox.showerror("Error", f"Error al descargar: {str(e)}")
            
            threading.Thread(target=download, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar la descarga: {str(e)}")

    def view_story(self, story):
        """Ver historia sin descargar"""
        try:
            if story.is_video:
                url = story.video_url
                if not url:
                    url = story.url
                
                if not url:
                    raise Exception("No se pudo obtener la URL de la historia")
                
                import webbrowser
                webbrowser.open(str(url))
            else:
                url = story.url
                import webbrowser
                webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir la historia: {str(e)}")

    def show_2fa_dialog(self):
        """Mostrar diálogo para código de verificación"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Verificación de dos factores")
        dialog.geometry("300x150")
        
        # Hacer la ventana modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, 
                 text="Por favor ingresa el código de verificación\nque recibiste en tu teléfono:",
                 wraplength=250,
                 justify='center').pack(pady=10)
        
        code_var = tk.StringVar()
        code_entry = ttk.Entry(dialog, textvariable=code_var, width=10, justify='center')
        code_entry.pack(pady=10)
        code_entry.focus()
        
        result = [None]  # Para almacenar el resultado
        
        def submit():
            result[0] = code_var.get()
            dialog.destroy()
        
        def cancel():
            dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Aceptar", command=submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=cancel).pack(side=tk.LEFT, padx=5)
        
        # Esperar hasta que se cierre el diálogo
        dialog.wait_window()
        
        return result[0]

    def get_video_summary(self, url, api_type='deepseek'):
        """Obtener resumen del video usando la API seleccionada"""
        try:
            # Mostrar ventana de progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Generando Resumen")
            progress_window.geometry("300x100")
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            progress_label = ttk.Label(progress_window, text="Obteniendo información del video...")
            progress_label.pack(pady=20)
            
            def process_summary():
                try:
                    # Obtener información del video
                    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                        info = ydl.extract_info(url, download=False)
                        title = info.get('title', '')
                        description = info.get('description', '')
                        duration = info.get('duration', 0)
                        
                        # Formatear duración
                        minutes = duration // 60
                        seconds = duration % 60
                        duration_str = f"{minutes}:{seconds:02d}"
                        
                        # Preparar prompt para la API
                        prompt = (
                            f"Genera un resumen conciso del siguiente video de YouTube:\n\n"
                            f"Título: {title}\n"
                            f"Duración: {duration_str}\n"
                            f"Descripción: {description}\n\n"
                            "Por favor, proporciona:\n"
                            "1. Un resumen breve del contenido principal\n"
                            "2. Puntos clave o momentos destacados\n"
                            "3. Una conclusión o recomendación"
                        )
                        
                        progress_label.config(text="Generando resumen con IA...")
                        
                        if api_type == 'deepseek':
                            # Usar el SDK de OpenAI con la URL base de Deepseek
                            client = OpenAI(
                                api_key=DEEPSEEK_API_KEY,
                                base_url="https://api.deepseek.com"
                            )
                            
                            response = client.chat.completions.create(
                                model="deepseek-chat",
                                messages=[
                                    {"role": "system", "content": "Eres un asistente útil y amigable"},
                                    {"role": "user", "content": prompt}
                                ],
                                temperature=0.7,
                                max_tokens=2000,
                                stream=False
                            )
                            
                            summary = response.choices[0].message.content
                        
                        # Mostrar el resumen en una nueva ventana
                        progress_window.destroy()
                        self.show_summary_window(title, summary)
                    
                except Exception as e:
                    progress_window.destroy()
                    messagebox.showerror("Error", f"Error al generar el resumen: {str(e)}")
            
            # Procesar en un hilo separado
            threading.Thread(target=process_summary, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar el proceso: {str(e)}")

    def show_summary_window(self, title, summary):
        """Mostrar ventana con el resumen del video"""
        summary_window = tk.Toplevel(self.root)
        summary_window.title(f"Resumen: {title}")
        summary_window.geometry("600x400")
        
        # Frame principal
        main_frame = ttk.Frame(summary_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, 
                 text=title,
                 style='Title.TLabel',
                 wraplength=550).pack(pady=(0,20))
        
        # Área de texto para el resumen
        text_widget = tk.Text(main_frame, 
                             wrap=tk.WORD, 
                             width=60, 
                             height=15,
                             font=('Segoe UI', 10))
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert('1.0', summary)
        text_widget.config(state='disabled')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, 
                                 orient='vertical', 
                                 command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        # Botón para copiar
        def copy_to_clipboard():
            summary_window.clipboard_clear()
            summary_window.clipboard_append(summary)
            messagebox.showinfo("Copiado", "Resumen copiado al portapapeles")
        
        ttk.Button(main_frame,
                   text="Copiar al Portapapeles",
                   command=copy_to_clipboard,
                   style='Custom.TButton').pack(pady=10)

    def show_summary_dialog(self):
        """Mostrar diálogo para obtener URL y elegir API"""
        dialog = tk.Toplevel(self.root)
        dialog.title("IA YT - Resumen de Video")  # Título actualizado
        dialog.geometry("400x200")
        
        # Hacer la ventana modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL del video
        ttk.Label(main_frame, 
                 text="URL del Video:",
                 style='Custom.TLabel').pack(anchor='w')
        
        url_var = tk.StringVar()
        url_entry = ttk.Entry(main_frame, textvariable=url_var, width=50)
        url_entry.pack(fill=tk.X, pady=(5,15))
        
        # Selección de API
        api_var = tk.StringVar(value='deepseek')
        ttk.Radiobutton(main_frame, 
                        text="DeepSeek",
                        variable=api_var,
                        value='deepseek').pack(anchor='w')
        ttk.Radiobutton(main_frame, 
                        text="ChatGPT",
                        variable=api_var,
                        value='chatgpt').pack(anchor='w')
        
        def submit():
            url = url_var.get()
            if url:
                dialog.destroy()
                self.get_video_summary(url, api_var.get())
            else:
                messagebox.showwarning("Advertencia", "Por favor ingresa una URL")
        
        # Botón de enviar
        ttk.Button(main_frame,
                  text="Obtener Resumen",
                  command=submit,
                  style='Custom.TButton').pack(pady=20)

    def download_playlist(self):
        try:
            url = self.playlist_url.get()
            placeholder = "Ej: https://www.youtube.com/playlist?list=..."
            
            if not url or url == placeholder:
                messagebox.showwarning("Advertencia", "Por favor ingrese una URL de lista de reproducción")
                return
            
            # Validar URL de lista de reproducción
            if not ('youtube.com/playlist' in url or 'list=' in url):
                messagebox.showerror("Error", "Por favor ingrese una URL válida de lista de reproducción de YouTube")
                return
            
            # Crear ventana de progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Procesando lista de reproducción...")
            progress_window.geometry("400x300")
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            status_label = ttk.Label(progress_window, text="Obteniendo videos de la lista...")
            status_label.pack(pady=10)
            
            # Frame para la lista de videos
            videos_frame = ttk.Frame(progress_window)
            videos_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Canvas y scrollbar para la lista de videos
            canvas = tk.Canvas(videos_frame)
            scrollbar = ttk.Scrollbar(videos_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            def process_playlist():
                try:
                    with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
                        info = ydl.extract_info(url, download=False)
                        entries = info.get('entries', [])
                        
                        if not entries:
                            if progress_window.winfo_exists():
                                progress_window.destroy()
                            messagebox.showwarning("Advertencia", "No se encontraron videos en la lista de reproducción")
                            return
                        
                        # Actualizar etiqueta de estado
                        status_label.config(text=f"Se encontraron {len(entries)} videos")
                        
                        for i, entry in enumerate(entries):
                            if not progress_window.winfo_exists():
                                break
                            
                            video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                            title = entry.get('title', f"Video {i+1}")
                            
                            # Crear frame para este video
                            video_frame = ttk.LabelFrame(scrollable_frame, text=f"Video {i+1}")
                            video_frame.pack(fill=tk.X


    def show_chat_window(self):
        """Mostrar ventana de chat con IA"""
        # Diálogo de selección de API
        api_dialog = tk.Toplevel(self.root)
        api_dialog.title("Seleccionar API")
        api_dialog.geometry("400x300")  # Aumentar altura
        api_dialog.transient(self.root)
        api_dialog.grab_set()
        api_dialog.resizable(False, False)
        
        # Configurar el fondo
        api_dialog.configure(bg='#ffffff')
        
        # Frame principal del diálogo con fondo blanco
        dialog_frame = ttk.Frame(api_dialog, padding=20, style='Dialog.TFrame')
        dialog_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurar estilos
        style = ttk.Style()
        style.configure('Dialog.TFrame', background='#ffffff')
        style.configure('DialogTitle.TLabel',
                       font=('Segoe UI', 14, 'bold'),
                       foreground='#1a1a1a',
                       background='#ffffff')
        style.configure('DialogRadio.TRadiobutton',
                       font=('Segoe UI', 10),
                       background='#ffffff',
                       padding=5)
        style.configure('DialogButton.TButton',
                       font=('Segoe UI', 10),
                       padding=8,
                       background='#4CAF50',
                       foreground='white')
        
        # Título con icono
        ttk.Label(dialog_frame,
                 text="🤖 Selecciona el Modelo de IA",
                 style='DialogTitle.TLabel').pack(pady=(0,15))
        
        # Frame para las opciones
        options_frame = ttk.Frame(dialog_frame, style='Dialog.TFrame')
        options_frame.pack(fill=tk.X, pady=10)
        
        selected_api = tk.StringVar(value="deepseek")
        
        # Opciones de API con descripciones
        deepseek_frame = ttk.Frame(options_frame, style='Dialog.TFrame')
        deepseek_frame.pack(fill=tk.X, pady=3)
        
        ttk.Radiobutton(deepseek_frame,
                        text="DeepSeek Chat",
                        value="deepseek",
                        variable=selected_api,
                        style='DialogRadio.TRadiobutton').pack(anchor='w')
        ttk.Label(deepseek_frame,
                 text="Modelo avanzado de IA con amplio conocimiento",
                 foreground='#666666',
                 background='#ffffff',
                 font=('Segoe UI', 9)).pack(anchor='w', padx=30)
        
        chatgpt_frame = ttk.Frame(options_frame, style='Dialog.TFrame')
        chatgpt_frame.pack(fill=tk.X, pady=3)
        
        ttk.Radiobutton(chatgpt_frame,
                        text="ChatGPT",
                        value="chatgpt",
                        variable=selected_api,
                        style='DialogRadio.TRadiobutton').pack(anchor='w')
        ttk.Label(chatgpt_frame,
                 text="Modelo conversacional de OpenAI",
                 foreground='#666666',
                 background='#ffffff',
                 font=('Segoe UI', 9)).pack(anchor='w', padx=30)
        
        # Barra de progreso
        progress_frame = ttk.Frame(dialog_frame, style='Dialog.TFrame')
        progress_frame.pack(fill=tk.X, pady=10)
        progress = ttk.Progressbar(progress_frame, mode='determinate', length=200)
        progress.pack()
        progress['value'] = 50  # Valor inicial
        
        def start_chat():
            api_choice = selected_api.get()
            progress['value'] = 100  # Actualizar progreso
            api_dialog.after(500, lambda: api_dialog.destroy())  # Cerrar después de 500ms
            self.create_chat_window(api_choice)
        
        # Frame para el botón
        button_frame = ttk.Frame(dialog_frame, style='Dialog.TFrame')
        button_frame.pack(fill=tk.X, pady=(20,0))
        
        # Botón para iniciar el chat
        ttk.Button(button_frame,
                   text="Iniciar Chat",
                   command=start_chat,
                   style='DialogButton.TButton').pack(expand=True)

    def create_chat_window(self, api_choice):
        """Crear ventana de chat"""
        chat_window = tk.Toplevel(self.root)
        chat_window.title(f"Chat con IA - {api_choice.upper()}")
        chat_window.geometry("600x800")
        
        # Frame principal
        main_frame = ttk.Frame(chat_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Área de chat
        chat_frame = ttk.Frame(main_frame)
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        # Área de mensajes con scroll
        messages_frame = ttk.Frame(chat_frame)
        messages_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas y scrollbar para los mensajes
        canvas = tk.Canvas(messages_frame, bg='#ffffff')
        scrollbar = ttk.Scrollbar(messages_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=550)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Área de entrada
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(20,0))
        
        # Campo de texto para el mensaje
        message_entry = tk.Text(input_frame, height=3, width=50, wrap=tk.WORD)
        message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,10))
        
        def add_message(text, is_user=True):
            """Agregar mensaje al chat"""
            message_frame = ttk.Frame(scrollable_frame)
            message_frame.pack(fill=tk.X, pady=5)
            
            # Alineación según el remitente
            if is_user:
                message_frame.pack_configure(anchor='e')
            else:
                message_frame.pack_configure(anchor='w')
            
            # Estilo del mensaje
            bg_color = '#DCF8C6' if is_user else '#E8E8E8'
            
            message_label = ttk.Label(
                message_frame,
                text=text,
                wraplength=400,
                justify=tk.LEFT,
                padding=10,
                background=bg_color
            )
            message_label.pack(side=tk.RIGHT if is_user else tk.LEFT)
            
            # Scroll al último mensaje
            canvas.update_idletasks()
            canvas.yview_moveto(1.0)
        
        def send_message():
            """Enviar mensaje y obtener respuesta"""
            message = message_entry.get("1.0", tk.END).strip()
            if not message:
                return
            
            # Limpiar campo de entrada
            message_entry.delete("1.0", tk.END)
            
            # Mostrar mensaje del usuario
            add_message(message, is_user=True)
            
            # Deshabilitar entrada mientras se procesa
            message_entry.config(state='disabled')
            send_button.config(state='disabled')
            
            def get_ai_response():
                try:
                    if api_choice == "deepseek":
                        # Usar el SDK de OpenAI con la URL base de Deepseek
                        client = OpenAI(
                            api_key=DEEPSEEK_API_KEY,
                            base_url="https://api.deepseek.com/v1"  # URL base correcta
                        )
                        
                        response = client.chat.completions.create(
                            model="deepseek-chat",  # Modelo más económico
                            messages=[
                                {"role": "user", "content": message}  # Solo el mensaje del usuario
                            ],
                            temperature=0.7,
                            max_tokens=1000,  # Reducido para optimizar costos
                            stream=False
                        )
                        
                        ai_message = response.choices[0].message.content
                        chat_window.after(0, lambda: add_message(ai_message, is_user=False))
                        
                    else:  # chatgpt
                        headers = {
                            "Authorization": f"Bearer {CHATGPT_API_KEY}",
                            "Content-Type": "application/json"
                        }
                        data = {
                            "messages": [{"role": "user", "content": message}],
                            "model": "gpt-3.5-turbo",
                            "temperature": 0.7
                        }
                        response = requests.post(
                            "https://api.openai.com/v1/chat/completions",
                            json=data,
                            headers=headers
                        )
                        
                        response.raise_for_status()
                        ai_message = response.json()['choices'][0]['message']['content']
                        chat_window.after(0, lambda: add_message(ai_message, is_user=False))
                    
                except Exception as e:
                    error_msg = str(e)
                    if "401" in error_msg:
                        error_msg = "Error de autenticación. Por favor verifica tu API key."
                    elif "429" in error_msg:
                        error_msg = "Demasiadas solicitudes. Por favor espera un momento."
                    chat_window.after(0, lambda: add_message(f"Error: {error_msg}", is_user=False))
                
                finally:
                    chat_window.after(0, lambda: message_entry.config(state='normal'))
                    chat_window.after(0, lambda: send_button.config(state='normal'))
            
            # Procesar en un hilo separado
            threading.Thread(target=get_ai_response, daemon=True).start()
        
        # Botón de enviar
        send_button = ttk.Button(
            input_frame,
            text="Enviar",
            command=send_message,
            style='Custom.TButton'
        )
        send_button.pack(side=tk.RIGHT)
        
        # Binding para Enter
        message_entry.bind("<Return>", lambda e: send_message() if not e.state & 1 else None)
        message_entry.bind("<Shift-Return>", lambda e: message_entry.insert(tk.END, "\n"))
        
        # Mensaje inicial
        add_message("¡Hola! Soy tu asistente de IA. ¿En qué puedo ayudarte?", is_user=False)
        
        # Dar foco al campo de entrada
        message_entry.focus_set()

class TikTokApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Downloader")
        
        # Configurar el tema y estilo
        self.root.configure(bg='#f0f0f0')
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar estilos personalizados
        style.configure('Custom.TButton',
                       padding=10,
                       font=('Segoe UI', 9),
                       background='#000000',  # Negro de TikTok
                       foreground='white')
        
        style.configure('Title.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground='#000000')
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, 
                               text="TikTok Downloader", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0,20))
        
        # Sección de Descarga de Videos
        video_frame = ttk.LabelFrame(main_frame, text="Descarga de Videos", padding=10)
        video_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0,10))
        
        # URL del video
        ttk.Label(video_frame, text="URL:", style='Custom.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.video_url = tk.StringVar()
        url_entry = ttk.Entry(video_frame, textvariable=self.video_url, width=50)
        url_entry.grid(row=0, column=1, padx=5, sticky='ew')
        url_placeholder = "Ej: https://www.tiktok.com/@usuario/video/..."
        url_entry.insert(0, url_placeholder)
        url_entry.config(foreground='gray', font=('Segoe UI', 9, 'italic'))

        # Funciones para manejar el foco en los campos de entrada
        def on_entry_click(event, placeholder):
            entry = event.widget
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(foreground='black', font=('Segoe UI', 9))

        def on_focus_out(event, placeholder):
            entry = event.widget
            if entry.get().strip() == '':  # Verificar si está vacío considerando espacios
                entry.delete(0, tk.END)  # Limpiar cualquier espacio
                entry.insert(0, placeholder)
                entry.config(foreground='gray', font=('Segoe UI', 9, 'italic'))

        # Aplicar las funciones a la entrada de URL
        url_entry.bind('<FocusIn>', lambda e: on_entry_click(e, url_placeholder))
        url_entry.bind('<FocusOut>', lambda e: on_focus_out(e, url_placeholder))

        # Botón de descarga
        ttk.Button(video_frame, 
                   text="Descargar", 
                   command=self.download_video,
                   style='Custom.TButton').grid(row=0, column=2, padx=(5,0))
        
        # Sección de Tendencias
        trends_frame = ttk.LabelFrame(main_frame, text="Videos Tendencia", padding=10)
        trends_frame.grid(row=2, column=0, columnspan=3, sticky='ew', pady=(0,10))
        
        # Botón de tendencias
        ttk.Button(trends_frame, 
                   text="🔥 Ver Tendencias", 
                   command=self.show_trending,
                   style='Custom.TButton').pack(fill=tk.X, pady=5)
        
        # Sección de Perfil
        profile_frame = ttk.LabelFrame(main_frame, text="Descargar de Perfil", padding=10)
        profile_frame.grid(row=3, column=0, columnspan=3, sticky='ew', pady=(0,10))
        
        # Usuario
        ttk.Label(profile_frame, text="Usuario:", style='Custom.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.username = tk.StringVar()
        username_entry = ttk.Entry(profile_frame, textvariable=self.username, width=50)
        username_entry.grid(row=0, column=1, padx=5, sticky='ew')
        username_placeholder = "Ej: @usuario"
        username_entry.insert(0, username_placeholder)
        username_entry.config(foreground='gray', font=('Segoe UI', 9, 'italic'))

        # Aplicar las funciones a la entrada de usuario
        username_entry.bind('<FocusIn>', lambda e: on_entry_click(e, username_placeholder))
        username_entry.bind('<FocusOut>', lambda e: on_focus_out(e, username_placeholder))

        # Botón de perfil
        ttk.Button(profile_frame, 
                   text="Ver Videos", 
                   command=self.show_profile_videos,
                   style='Custom.TButton').grid(row=0, column=2, padx=(5,0))

        # Botones inferiores
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(bottom_frame, 
                   text="Cambiar Directorio",
                   command=self.change_directory,
                   style='Custom.TButton').grid(row=0, column=0, padx=10)
        
        ttk.Button(bottom_frame, 
                   text="Acerca de",
                   command=self.show_about,
                   style='Custom.TButton').grid(row=0, column=1, padx=10)

        ttk.Button(bottom_frame, 
                   text="Botón Inactivo",
                   command=lambda: None,  # No hace nada
                   style='Custom.TButton').grid(row=0, column=2, padx=10)

        # Configurar el directorio de descarga
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")

    # ... (resto de métodos de la clase)
    
    def download_video(self):
        """Descargar video de TikTok"""
        url = self.video_url.get()
        if url == "Ej: https://www.tiktok.com/@usuario/video/..." or not url:
            messagebox.showerror("Error", "Por favor ingresa una URL válida")
            return
        
        try:
            # Configurar opciones de yt-dlp
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Mostrar progreso
                progress_window = tk.Toplevel(self.root)
                progress_window.title("Descargando")
                progress_window.geometry("300x100")
                
                progress_label = ttk.Label(progress_window, text="Descargando video...")
                progress_label.pack(pady=20)
                
                # Descargar en un hilo separado
                def download():
                    try:
                        ydl.download([url])
                        progress_window.destroy()
                        messagebox.showinfo("Éxito", "Video descargado correctamente")
                    except Exception as e:
                        progress_window.destroy()
                        messagebox.showerror("Error", f"Error al descargar: {str(e)}")
                
                threading.Thread(target=download, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar la descarga: {str(e)}")
    
    def show_trending(self):
        """Mostrar videos en tendencia"""
        try:
            # Configurar opciones de yt-dlp
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Mostrar ventana de tendencias
                trends_window = tk.Toplevel(self.root)
                trends_window.title("Videos en Tendencia")
                trends_window.geometry("600x500")
                
                # Frame principal
                main_frame = ttk.Frame(trends_window, padding=20)
                main_frame.pack(fill=tk.BOTH, expand=True)
                
                # Título
                ttk.Label(main_frame, 
                         text="🔥 Tendencias TikTok",
                         style='Title.TLabel').pack(pady=(0,20))
                
                # Lista con scroll
                list_frame = ttk.Frame(main_frame)
                list_frame.pack(fill=tk.BOTH, expand=True)
                
                scrollbar = ttk.Scrollbar(list_frame)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                canvas = tk.Canvas(list_frame)
                canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                
                scrollbar.config(command=canvas.yview)
                canvas.config(yscrollcommand=scrollbar.set)
                
                content_frame = ttk.Frame(canvas)
                canvas.create_window((0,0), window=content_frame, anchor='nw')
                
                # Obtener tendencias
                info = ydl.extract_info("https://www.tiktok.com/trending", download=False)
                
                if 'entries' in info:
                    for i, video in enumerate(info['entries'][:20]):
                        video_frame = ttk.Frame(content_frame)
                        video_frame.pack(fill=tk.X, pady=5, padx=5)
                        
                        title = video.get('title', 'Sin título')
                        uploader = video.get('uploader', 'Usuario desconocido')
                        
                        ttk.Label(video_frame, 
                                text=f"{title}",
                                wraplength=500,
                                style='Info.TLabel').pack(anchor='w')
                        
                        ttk.Label(video_frame,
                                text=f"👤 {uploader}",
                                style='Info.TLabel').pack(anchor='w')
                        
                        ttk.Button(video_frame,
                                 text="Descargar",
                                 command=lambda url=video['url']: self.download_video_from_url(url),
                                 style='Custom.TButton').pack(anchor='w', pady=5)
                        
                        ttk.Separator(video_frame, orient='horizontal').pack(fill=tk.X, pady=5)
                else:
                    ttk.Label(content_frame,
                             text="No se encontraron videos en tendencia",
                             style='Info.TLabel').pack(pady=20)
                
                content_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener tendencias: {str(e)}")
    
    def show_profile_videos(self):
        """Mostrar videos de un perfil"""
        username = self.username.get()
        if username == "Ej: @usuario" or not username:
            messagebox.showerror("Error", "Por favor ingresa un nombre de usuario válido")
            return
        
        try:
            # Configurar opciones de yt-dlp
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Mostrar ventana de perfil
                profile_window = tk.Toplevel(self.root)
                profile_window.title(f"Videos de {username}")
                profile_window.geometry("600x500")
                
                # Frame principal
                main_frame = ttk.Frame(profile_window, padding=20)
                main_frame.pack(fill=tk.BOTH, expand=True)
                
                # Título
                ttk.Label(main_frame, 
                         text=f"Videos de {username}",
                         style='Title.TLabel').pack(pady=(0,20))
                
                # Lista con scroll
                list_frame = ttk.Frame(main_frame)
                list_frame.pack(fill=tk.BOTH, expand=True)
                
                scrollbar = ttk.Scrollbar(list_frame)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                canvas = tk.Canvas(list_frame)
                canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                
                scrollbar.config(command=canvas.yview)
                canvas.config(yscrollcommand=scrollbar.set)
                
                content_frame = ttk.Frame(canvas)
                canvas.create_window((0,0), window=content_frame, anchor='nw')
                
                # Obtener videos del perfil
                info = ydl.extract_info(f"https://www.tiktok.com/@{username}", download=False)
                
                if 'entries' in info:
                    for i, video in enumerate(info['entries']):
                        video_frame = ttk.Frame(content_frame)
                        video_frame.pack(fill=tk.X, pady=5, padx=5)
                        
                        title = video.get('title', f'Video {i+1}')
                        
                        ttk.Label(video_frame, 
                                text=f"{title}",
                                wraplength=500,
                                style='Info.TLabel').pack(anchor='w')
                        
                        ttk.Button(video_frame,
                                 text="Descargar",
                                 command=lambda url=video['url']: self.download_video_from_url(url),
                                 style='Custom.TButton').pack(anchor='w', pady=5)
                        
                        ttk.Separator(video_frame, orient='horizontal').pack(fill=tk.X, pady=5)
                else:
                    ttk.Label(content_frame,
                             text="No se encontraron videos",
                             style='Info.TLabel').pack(pady=20)
                
                content_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener videos: {str(e)}")
    
    def download_video_from_url(self, url):
        """Descargar video desde URL"""
        self.video_url.set(url)
        self.download_video()
    
    def change_directory(self):
        """Cambiar directorio de descarga"""
        new_path = filedialog.askdirectory(initialdir=self.download_path)
        if new_path:
            self.download_path = new_path
            messagebox.showinfo("Directorio", f"Directorio de descarga cambiado a:\n{new_path}")
    
    def show_about(self):
        """Mostrar información sobre la aplicación"""
        messagebox.showinfo("Acerca de", 
                          "TikTok Downloader v1.0\n"
                          "Desarrollado con Python y tkinter\n"
                          "© 2025 RakkoTech")

    def show_2fa_dialog(self):
        """Mostrar diálogo para código de verificación"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Verificación de dos factores")
        dialog.geometry("300x150")
        
        # Hacer la ventana modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, 
                 text="Por favor ingresa el código de verificación\nque recibiste en tu teléfono:",
                 wraplength=250,
                 justify='center').pack(pady=10)
        
        code_var = tk.StringVar()
        code_entry = ttk.Entry(dialog, textvariable=code_var, width=10, justify='center')
        code_entry.pack(pady=10)
        code_entry.focus()
        
        result = [None]  # Para almacenar el resultado
        
        def submit():
            result[0] = code_var.get()
            dialog.destroy()
        
        def cancel():
            dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Aceptar", command=submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=cancel).pack(side=tk.LEFT, padx=5)
        
        # Esperar hasta que se cierre el diálogo
        dialog.wait_window()
        
        return result[0]

    def download_tiktok_video(self, url):
        """Descargar video de TikTok"""
        try:
            # Configurar opciones de yt-dlp
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'ignoreerrors': True
            }
            
            # Mostrar ventana de progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Descargando")
            progress_window.geometry("300x100")
            
            progress_label = ttk.Label(progress_window, text="Descargando video de TikTok...")
            progress_label.pack(pady=20)
            
            def download():
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    progress_window.destroy()
                    messagebox.showinfo("Éxito", "Video de TikTok descargado correctamente")
                except Exception as e:
                    progress_window.destroy()
                    messagebox.showerror("Error", f"Error al descargar: {str(e)}")
            
            threading.Thread(target=download, daemon=True).start()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar la descarga: {str(e)}")

    def show_trending_tiktok_videos(self):
        """Mostrar videos en tendencia de TikTok"""
        try:
            # Mostrar ventana de progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Cargando")
            progress_window.geometry("300x100")
            
            progress_label = ttk.Label(progress_window, text="Cargando videos de TikTok...")
            progress_label.pack(pady=20)
            
            def get_trending_videos():
                try:
                    # Configurar yt-dlp
                    ydl_opts = {
                        'quiet': True,
                        'no_warnings': True,
                        'extract_flat': True,
                        'format': 'best',
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        # Obtener videos de tendencia
                        info = ydl.extract_info("https://www.tiktok.com/trending", download=False)
                        
                        # Cerrar ventana de progreso
                        progress_window.destroy()
                        
                        if 'entries' in info:
                            for i, video in enumerate(info['entries'][:10]):  # Limitar a 10 videos
                                # Aquí puedes agregar el código para mostrar los videos en la interfaz
                                print(f"{i+1}. {video['title']} - {video['url']}")
                        else:
                            messagebox.showinfo("Tendencias", "No se encontraron videos en tendencia.")
                
                except Exception as e:
                    progress_window.destroy()
                    messagebox.showerror("Error", f"Error al obtener videos: {str(e)}")
            
            threading.Thread(target=get_trending_videos, daemon=True).start()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar: {str(e)}")

class InstagramApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Downloader")
        
        # Configurar el tema y estilo
        self.root.configure(bg='#f0f0f0')
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar estilos personalizados
        style.configure('Custom.TButton',
                       padding=10,
                       font=('Segoe UI', 9),
                       background='#E1306C',  # Rosa de Instagram
                       foreground='white')
        
        style.configure('Title.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground='#E1306C')
        
        style.configure('Info.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#333333')
        
        # Funciones para manejar el foco en los campos de entrada
        def on_entry_click(event, placeholder):
            entry = event.widget
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(foreground='black', font=('Segoe UI', 9))

        def on_focus_out(event, placeholder):
            entry = event.widget
            if entry.get().strip() == '':  # Verificar si está vacío considerando espacios
                entry.delete(0, tk.END)  # Limpiar cualquier espacio
                entry.insert(0, placeholder)
                entry.config(foreground='gray', font=('Segoe UI', 9, 'italic'))
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, 
                               text="Instagram Downloader", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0,20))
        
        # Sección de Descarga de Contenido
        content_frame = ttk.LabelFrame(main_frame, text="Descarga de Contenido", padding=10)
        content_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0,10))
        
        # URL del contenido
        ttk.Label(content_frame, text="URL:", style='Custom.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.content_url = tk.StringVar()
        url_entry = ttk.Entry(content_frame, textvariable=self.content_url, width=50)
        url_entry.grid(row=0, column=1, padx=5, sticky='ew')
        url_placeholder = "Ej: https://www.instagram.com/p/..."
        url_entry.insert(0, url_placeholder)
        url_entry.config(foreground='gray', font=('Segoe UI', 9, 'italic'))
        url_entry.bind('<FocusIn>', lambda e: on_entry_click(e, url_placeholder))
        url_entry.bind('<FocusOut>', lambda e: on_focus_out(e, url_placeholder))
        
        # Botón de descarga
        ttk.Button(content_frame, 
                   text="Descargar", 
                   command=self.download_content,
                   style='Custom.TButton').grid(row=0, column=2, padx=(5,0))
        
        # Sección de Historias
        stories_frame = ttk.LabelFrame(main_frame, text="Historias", padding=10)
        stories_frame.grid(row=2, column=0, columnspan=3, sticky='ew', pady=(0,10))
        
        # Usuario para historias
        ttk.Label(stories_frame, text="Usuario:", style='Custom.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.username = tk.StringVar()
        username_entry = ttk.Entry(stories_frame, textvariable=self.username, width=50)
        username_entry.grid(row=0, column=1, padx=5, sticky='ew')
        username_placeholder = "Ej: username"
        username_entry.insert(0, username_placeholder)
        username_entry.config(foreground='gray', font=('Segoe UI', 9, 'italic'))
        username_entry.bind('<FocusIn>', lambda e: on_entry_click(e, username_placeholder))
        username_entry.bind('<FocusOut>', lambda e: on_focus_out(e, username_placeholder))
        
        # Agregar los eventos usando las funciones locales
        username_entry.bind('<FocusIn>', lambda e: on_entry_click(e, username_placeholder))
        username_entry.bind('<FocusOut>', lambda e: on_focus_out(e, username_placeholder))
        
        # Botón de historias
        ttk.Button(stories_frame, 
                   text="Ver Historias", 
                   command=self.get_stories,
                   style='Custom.TButton').grid(row=0, column=2, padx=(5,0))
        
        # Sección de Reels
        reels_frame = ttk.LabelFrame(main_frame, text="Reels", padding=10)
        reels_frame.grid(row=3, column=0, columnspan=3, sticky='ew', pady=(0,10))
        
        # Botón de reels populares
        ttk.Button(reels_frame, 
                   text="🔥 Ver Reels Populares", 
                   command=self.show_trending_reels,
                   style='Custom.TButton').pack(fill=tk.X, pady=5)
        
        # Botones inferiores
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(bottom_frame, 
                   text="Cambiar Directorio",
                   command=self.change_directory,
                   style='Custom.TButton').grid(row=0, column=0, padx=10)
        
        ttk.Button(bottom_frame, 
                   text="Acerca de",
                   command=self.show_about,
                   style='Custom.TButton').grid(row=0, column=1, padx=10)

        ttk.Button(bottom_frame, 
                   text="Botón Inactivo",
                   command=lambda: None,  # No hace nada
                   style='Custom.TButton').grid(row=0, column=2, padx=10)
        
        # Configurar el directorio de descarga
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    
    def download_content(self):
        """Descargar contenido de Instagram"""
        url = self.content_url.get()
        if url == "Ej: https://www.instagram.com/p/..." or not url:
            messagebox.showerror("Error", "Por favor ingresa una URL válida")
            return
        
        try:
            # Configurar opciones de yt-dlp
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Mostrar progreso
                progress_window = tk.Toplevel(self.root)
                progress_window.title("Descargando")
                progress_window.geometry("300x100")
                
                progress_label = ttk.Label(progress_window, text="Descargando contenido...")
                progress_label.pack(pady=20)
                
                # Descargar en un hilo separado
                def download():
                    try:
                        ydl.download([url])
                        progress_window.destroy()
                        messagebox.showinfo("Éxito", "Contenido descargado correctamente")
                    except Exception as e:
                        progress_window.destroy()
                        messagebox.showerror("Error", f"Error al descargar: {str(e)}")
                
                threading.Thread(target=download, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar la descarga: {str(e)}")
    
    def show_trending_reels(self):
        """Mostrar reels populares"""
        try:
            # Mostrar ventana de progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Cargando")
            progress_window.geometry("300x100")
            
            progress_label = ttk.Label(progress_window, text="Iniciando sesión...")
            progress_label.pack(pady=20)
            
            def get_reels_thread():
                try:
                    # Crear instancia de instaloader
                    L = instaloader.Instaloader()
                    
                    # Login (usando las credenciales que ya funcionan)
                    try:
                        L.login('sum_maps', 'Yoelrambo15')
                    except instaloader.exceptions.TwoFactorAuthRequiredException:
                        # Solicitar código 2FA
                        progress_label.config(text="Esperando código de verificación...")
                        code = self.show_2fa_dialog()
                        if code:
                            try:
                                L.two_factor_login(code)
                                progress_label.config(text="Obteniendo reels...")
                            except Exception as e:
                                progress_window.destroy()
                                messagebox.showerror("Error", f"Código incorrecto: {str(e)}")
                                return
                        else:
                            progress_window.destroy()
                            return
                    except Exception as e:
                        progress_window.destroy()
                        messagebox.showerror("Error", f"Error al iniciar sesión: {str(e)}")
                        return
                    
                    # Mostrar ventana de reels
                    reels_window = tk.Toplevel(self.root)
                    reels_window.title("Reels Populares")
                    reels_window.geometry("600x500")
                    
                    # Frame principal
                    main_frame = ttk.Frame(reels_window, padding=20)
                    main_frame.pack(fill=tk.BOTH, expand=True)
                    
                    # Título
                    ttk.Label(main_frame, 
                             text="🔥 Reels Populares",
                             style='Title.TLabel').pack(pady=(0,20))
                    
                    # Lista con scroll
                    list_frame = ttk.Frame(main_frame)
                    list_frame.pack(fill=tk.BOTH, expand=True)
                    
                    scrollbar = ttk.Scrollbar(list_frame)
                    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                    
                    canvas = tk.Canvas(list_frame)
                    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                    
                    scrollbar.config(command=canvas.yview)
                    canvas.config(yscrollcommand=scrollbar.set)
                    
                    content_frame = ttk.Frame(canvas)
                    canvas.create_window((0,0), window=content_frame, anchor='nw')
                    
                    try:
                        # Perfiles populares de Instagram
                        popular_profiles = ['instagram', 'cristiano', 'leomessi', 'kimkardashian', 'kyliejenner']
                        reels_found = []
                        
                        progress_label.config(text="Obteniendo reels populares...")
                        
                        # Obtener reels de cada perfil
                        for username in popular_profiles:
                            try:
                                profile = instaloader.Profile.from_username(L.context, username)
                                posts = profile.get_posts()
                                
                                # Tomar los primeros 3 reels de cada perfil
                                count = 0
                                for post in posts:
                                    if count >= 3:
                                        break
                                    if post.is_video:
                                        reels_found.append(post)
                                        count += 1
                            except:
                                continue
                        
                        # Cerrar ventana de progreso
                        progress_window.destroy()
                        
                        if reels_found:
                            for i, reel in enumerate(reels_found, 1):
                                reel_frame = ttk.Frame(content_frame)
                                reel_frame.pack(fill=tk.X, pady=5, padx=5)
                                
                                # Información del reel
                                caption = reel.caption if reel.caption else f'Reel {i}'
                                caption = caption[:100] + '...' if len(caption) > 100 else caption
                                
                                ttk.Label(reel_frame, 
                                        text=caption,
                                        wraplength=500,
                                        style='Info.TLabel').pack(anchor='w')
                                
                                ttk.Label(reel_frame,
                                        text=f"👤 {reel.owner_username}",
                                        style='Info.TLabel').pack(anchor='w')
                                
                                # Frame para botones
                                buttons_frame = ttk.Frame(reel_frame)
                                buttons_frame.pack(anchor='w', pady=5)
                                
                                # Botón para ver
                                ttk.Button(buttons_frame,
                                         text="Ver",
                                         command=lambda url=f"https://www.instagram.com/p/{reel.shortcode}/": webbrowser.open(url),
                                         style='Custom.TButton').pack(side=tk.LEFT, padx=(0,5))
                                
                                ttk.Separator(reel_frame, orient='horizontal').pack(fill=tk.X, pady=5)
                        else:
                            ttk.Label(content_frame,
                                     text="No se pudieron obtener reels. Intenta más tarde.",
                                     style='Info.TLabel').pack(pady=20)
                        
                    except Exception as e:
                        progress_window.destroy()
                        ttk.Label(content_frame,
                                 text=f"Error al obtener reels: {str(e)}",
                                 style='Info.TLabel').pack(pady=20)
                    
                    content_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                    
                except Exception as e:
                    progress_window.destroy()
                    messagebox.showerror("Error", f"Error: {str(e)}")
            
            # Ejecutar en un hilo separado
            threading.Thread(target=get_reels_thread, daemon=True).start()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener reels: {str(e)}")
    
    def download_reel(self, reel):
        """Descargar reel usando instaloader"""
        try:
            # Crear directorio para reels si no existe
            reels_dir = os.path.join(self.download_path, 'reels')
            if not os.path.exists(reels_dir):
                os.makedirs(reels_dir)
            
            # Mostrar progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Descargando")
            progress_window.geometry("300x100")
            
            progress_label = ttk.Label(progress_window, text="Descargando reel...")
            progress_label.pack(pady=20)
            
            def download():
                try:
                    # Crear instancia de instaloader
                    L = instaloader.Instaloader()
                    
                    # Descargar el reel
                    L.download_post(reel, target=reels_dir)
                    
                    progress_window.destroy()
                    messagebox.showinfo("Éxito", "Reel descargado correctamente")
                except Exception as e:
                    progress_window.destroy()
                    messagebox.showerror("Error", f"Error al descargar: {str(e)}")
            
            threading.Thread(target=download, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar la descarga: {str(e)}")
    
    def change_directory(self):
        """Cambiar directorio de descarga"""
        new_path = filedialog.askdirectory(initialdir=self.download_path)
        if new_path:
            self.download_path = new_path
            messagebox.showinfo("Directorio", f"Directorio de descarga cambiado a:\n{new_path}")
    
    def show_about(self):
        """Mostrar información sobre la aplicación"""
        messagebox.showinfo("Acerca de", 
                          "Instagram Downloader v1.0\n"
                          "Desarrollado con Python y tkinter\n"
                          "© 2025 RakkoTech")

    def get_stories(self):
        """Obtener historias de un usuario"""
        username = self.username.get()
        if username == "Ej: username" or username.strip() == "":  # Verificar también espacios
            messagebox.showerror("Error", "Por favor ingresa un nombre de usuario válido")
            return
        
        try:
            # Mostrar ventana de progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Cargando")
            progress_window.geometry("300x100")
            
            progress_label = ttk.Label(progress_window, text="Iniciando sesión...")
            progress_label.pack(pady=20)
            
            def get_stories_thread():
                try:
                    # Crear instancia de instaloader
                    L = instaloader.Instaloader(
                        download_videos=True,
                        download_video_thumbnails=False,
                        download_geotags=False,
                        download_comments=False,
                        save_metadata=False,
                        compress_json=False
                    )
                    
                    def show_2fa_dialog():
                        """Mostrar diálogo para código de verificación"""
                        dialog = tk.Toplevel(self.root)
                        dialog.title("Verificación de dos factores")
                        dialog.geometry("300x150")
                        
                        # Hacer la ventana modal
                        dialog.transient(self.root)
                        dialog.grab_set()
                        
                        ttk.Label(dialog, 
                                 text="Por favor ingresa el código de verificación\nque recibiste en tu teléfono:",
                                 wraplength=250,
                                 justify='center').pack(pady=10)
                        
                        code_var = tk.StringVar()
                        code_entry = ttk.Entry(dialog, textvariable=code_var, width=10, justify='center')
                        code_entry.pack(pady=10)
                        code_entry.focus()
                        
                        result = [None]  # Para almacenar el resultado
                        
                        def submit():
                            result[0] = code_var.get()
                            dialog.destroy()
                        
                        def cancel():
                            dialog.destroy()
                        
                        button_frame = ttk.Frame(dialog)
                        button_frame.pack(pady=10)
                        
                        ttk.Button(button_frame, text="Aceptar", command=submit).pack(side=tk.LEFT, padx=5)
                        ttk.Button(button_frame, text="Cancelar", command=cancel).pack(side=tk.LEFT, padx=5)
                        
                        # Esperar hasta que se cierre el diálogo
                        dialog.wait_window()
                        
                        return result[0]
                    
                    try:
                        # Intentar login
                        L.login('sum_maps', 'Yoelrambo15')
                    except instaloader.exceptions.TwoFactorAuthRequiredException:
                        # Solicitar código 2FA
                        progress_label.config(text="Esperando código de verificación...")
                        code = self.show_2fa_dialog()  # Usar self.show_2fa_dialog
                        if code:
                            try:
                                L.two_factor_login(code)
                                progress_label.config(text="Obteniendo historias...")
                            except Exception as e:
                                progress_window.destroy()
                                messagebox.showerror("Error", f"Código incorrecto: {str(e)}")
                                return
                        else:
                            progress_window.destroy()
                            return
                    except Exception as e:
                        progress_window.destroy()
                        messagebox.showerror("Error", f"Error al iniciar sesión: {str(e)}")
                        return
                    
                    try:
                        # Obtener perfil
                        profile = instaloader.Profile.from_username(L.context, username)
                        
                        # Obtener historias
                        stories = L.get_stories([profile.userid])
                        story_items = []
                        
                        # Recopilar todas las historias
                        for story in stories:
                            story_items.extend(story.get_items())
                        
                        # Cerrar ventana de progreso
                        progress_window.destroy()
                        
                        if story_items:
                            # Mostrar ventana con las historias
                            stories_window = tk.Toplevel(self.root)
                            stories_window.title(f"Historias de {username}")
                            stories_window.geometry("600x500")
                            
                            # Frame principal
                            main_frame = ttk.Frame(stories_window, padding=20)
                            main_frame.pack(fill=tk.BOTH, expand=True)
                            
                            # Lista con scroll
                            list_frame = ttk.Frame(main_frame)
                            list_frame.pack(fill=tk.BOTH, expand=True)
                            
                            scrollbar = ttk.Scrollbar(list_frame)
                            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                            
                            canvas = tk.Canvas(list_frame)
                            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                            
                            scrollbar.config(command=canvas.yview)
                            canvas.config(yscrollcommand=scrollbar.set)
                            
                            content_frame = ttk.Frame(canvas)
                            canvas.create_window((0,0), window=content_frame, anchor='nw')
                            
                            # Mostrar cada historia
                            for i, story in enumerate(story_items, 1):
                                story_frame = ttk.Frame(content_frame)
                                story_frame.pack(fill=tk.X, pady=5, padx=5)
                                
                                # Determinar tipo de historia
                                story_type = "Video" if story.is_video else "Foto"
                                date = story.date.strftime("%Y-%m-%d %H:%M")
                                
                                ttk.Label(story_frame,
                                        text=f"Historia {i} ({story_type}) - {date}",
                                        style='Info.TLabel').pack(anchor='w')
                                
                                # Frame para botones
                                buttons_frame = ttk.Frame(story_frame)
                                buttons_frame.pack(anchor='w', pady=5)
                                
                                # Botón para ver
                                ttk.Button(buttons_frame,
                                         text="Ver",
                                         command=lambda s=story: self.view_story(s),
                                         style='Custom.TButton').pack(side=tk.LEFT, padx=(0,5))
                                
                                # Botón para descargar
                                ttk.Button(buttons_frame,
                                         text="Descargar",
                                         command=lambda s=story: self.download_story_item(s),
                                         style='Custom.TButton').pack(side=tk.LEFT)
                                
                                ttk.Separator(story_frame, 
                                            orient='horizontal').pack(fill=tk.X, pady=5)
                            
                            # Actualizar scroll region
                            content_frame.bind('<Configure>', 
                                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                        else:
                            messagebox.showinfo("Historias", "No se encontraron historias activas")
                    
                    except Exception as e:
                        progress_window.destroy()
                        messagebox.showerror("Error", f"Error al obtener historias: {str(e)}")
                
                except Exception as e:
                    progress_window.destroy()
                    messagebox.showerror("Error", f"Error: {str(e)}")
            
            # Ejecutar en un hilo separado
            threading.Thread(target=get_stories_thread, daemon=True).start()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar: {str(e)}")

    def download_story(self, url):
        """Descargar historia de Instagram"""
        try:
            # Configurar opciones de yt-dlp
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(self.download_path, 'stories/%(uploader)s/%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'cookiesfrombrowser': ('chrome',),
                'ignoreerrors': True
            }
            
            # Crear directorio para historias si no existe
            stories_dir = os.path.join(self.download_path, 'stories')
            if not os.path.exists(stories_dir):
                os.makedirs(stories_dir)
            
            # Mostrar progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Descargando")
            progress_window.geometry("300x100")
            
            progress_label = ttk.Label(progress_window, text="Descargando historia...")
            progress_label.pack(pady=20)
            
            def download():
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    progress_window.destroy()
                    messagebox.showinfo("Éxito", "Historia descargada correctamente")
                except Exception as e:
                    progress_window.destroy()
                    messagebox.showerror("Error", f"Error al descargar: {str(e)}")
            
            threading.Thread(target=download, daemon=True).start()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar la descarga: {str(e)}")

    def download_story_item(self, story):
        """Descargar historia individual"""
        try:
            # Crear directorio para historias si no existe
            stories_dir = os.path.join(self.download_path, 'stories', story.owner_username)
            if not os.path.exists(stories_dir):
                os.makedirs(stories_dir)
            
            # Mostrar progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Descargando")
            progress_window.geometry("300x100")
            
            progress_label = ttk.Label(progress_window, text="Descargando historia...")
            progress_label.pack(pady=20)
            
            def download():
                try:
                    # Determinar nombre del archivo
                    date_str = story.date.strftime("%Y%m%d_%H%M%S")
                    ext = "mp4" if story.is_video else "jpg"
                    filename = f"{date_str}.{ext}"
                    filepath = os.path.join(stories_dir, filename)
                    
                    # Descargar el archivo usando requests
                    if story.is_video:
                        url = story.video_url
                    else:
                        url = story.url
                    
                    response = requests.get(url, stream=True)
                    response.raise_for_status()
                    
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    # Actualizar la fecha de modificación al momento actual
                    current_time = time.time()
                    os.utime(filepath, (current_time, current_time))
                    
                    progress_window.destroy()
                    messagebox.showinfo("Éxito", "Historia descargada correctamente")
                except Exception as e:
                    progress_window.destroy()
                    messagebox.showerror("Error", f"Error al descargar: {str(e)}")
            
            threading.Thread(target=download, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar la descarga: {str(e)}")

    def view_story(self, story):
        """Ver historia sin descargar"""
        try:
            if story.is_video:
                url = story.video_url
                if not url:
                    url = story.url
                
                if not url:
                    raise Exception("No se pudo obtener la URL de la historia")
                
                import webbrowser
                webbrowser.open(str(url))
            else:
                url = story.url
                import webbrowser
                webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir la historia: {str(e)}")

    def show_2fa_dialog(self):
        """Mostrar diálogo para código de verificación"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Verificación de dos factores")
        dialog.geometry("300x150")
        
        # Hacer la ventana modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, 
                 text="Por favor ingresa el código de verificación\nque recibiste en tu teléfono:",
                 wraplength=250,
                 justify='center').pack(pady=10)
        
        code_var = tk.StringVar()
        code_entry = ttk.Entry(dialog, textvariable=code_var, width=10, justify='center')
        code_entry.pack(pady=10)
        code_entry.focus()
        
        result = [None]  # Para almacenar el resultado
        
        def submit():
            result[0] = code_var.get()
            dialog.destroy()
        
        def cancel():
            dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Aceptar", command=submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=cancel).pack(side=tk.LEFT, padx=5)
        
        # Esperar hasta que se cierre el diálogo
        dialog.wait_window()
        
        return result[0]

class FacebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Downloader")
        
        # Configurar el tema y estilo
        self.root.configure(bg='#f0f0f0')
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar estilos personalizados
        style.configure('Custom.TButton',
                       padding=10,
                       font=('Segoe UI', 9),
                       background='#1877F2',  # Azul de Facebook
                       foreground='white')
        
        style.configure('Title.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground='#1877F2')  # Azul de Facebook
        
        style.configure('Info.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#333333')
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, 
                               text="Facebook Downloader", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0,20))
        
        # Sección de Descarga de Videos
        video_frame = ttk.LabelFrame(main_frame, text="Descarga de Videos", padding=10)
        video_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0,10))
        
        # URL del video
        ttk.Label(video_frame, text="URL:", style='Custom.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.video_url = tk.StringVar()
        url_entry = ttk.Entry(video_frame, textvariable=self.video_url, width=50)
        url_entry.grid(row=0, column=1, padx=5, sticky='ew')
        url_placeholder = "Ej: https://www.facebook.com/watch?v=..."
        url_entry.insert(0, url_placeholder)
        url_entry.config(foreground='gray', font=('Segoe UI', 9, 'italic'))
        
        # Funciones para manejar el foco en los campos de entrada
        def on_entry_click(event, placeholder):
            entry = event.widget
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(foreground='black', font=('Segoe UI', 9))

        def on_focus_out(event, placeholder):
            entry = event.widget
            if entry.get().strip() == '':
                entry.delete(0, tk.END)
                entry.insert(0, placeholder)
                entry.config(foreground='gray', font=('Segoe UI', 9, 'italic'))
        
        # Aplicar eventos a la entrada de URL
        url_entry.bind('<FocusIn>', lambda e: on_entry_click(e, url_placeholder))
        url_entry.bind('<FocusOut>', lambda e: on_focus_out(e, url_placeholder))
        
        # Botón de descarga
        ttk.Button(video_frame, 
                   text="Descargar", 
                   command=self.download_video,
                   style='Custom.TButton').grid(row=0, column=2, padx=(5,0))
        
        # Sección de Videos Populares
        trending_frame = ttk.LabelFrame(main_frame, text="Videos Populares", padding=10)
        trending_frame.grid(row=2, column=0, columnspan=3, sticky='ew', pady=(0,10))
        
        # Botón de tendencias
        ttk.Button(trending_frame, 
                   text="🔥 Ver Videos Populares", 
                   command=self.show_trending,
                   style='Custom.TButton').pack(fill=tk.X, pady=5)
        
        # Sección de Perfil
        profile_frame = ttk.LabelFrame(main_frame, text="Videos de Perfil", padding=10)
        profile_frame.grid(row=3, column=0, columnspan=3, sticky='ew', pady=(0,10))
        
        # Usuario
        ttk.Label(profile_frame, text="Usuario:", style='Custom.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.username = tk.StringVar()
        username_entry = ttk.Entry(profile_frame, textvariable=self.username, width=50)
        username_entry.grid(row=0, column=1, padx=5, sticky='ew')
        username_placeholder = "Ej: nombre.usuario"
        username_entry.insert(0, username_placeholder)
        username_entry.config(foreground='gray', font=('Segoe UI', 9, 'italic'))
        
        # Aplicar eventos a la entrada de usuario
        username_entry.bind('<FocusIn>', lambda e: on_entry_click(e, username_placeholder))
        username_entry.bind('<FocusOut>', lambda e: on_focus_out(e, username_placeholder))
        
        # Botón de perfil
        ttk.Button(profile_frame, 
                   text="Ver Videos", 
                   command=self.show_profile_videos,
                   style='Custom.TButton').grid(row=0, column=2, padx=(5,0))
        
        # Botones inferiores
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(bottom_frame, 
                   text="Cambiar Directorio",
                   command=self.change_directory,
                   style='Custom.TButton').grid(row=0, column=0, padx=10)
        
        ttk.Button(bottom_frame, 
                   text="Acerca de",
                   command=self.show_about,
                   style='Custom.TButton').grid(row=0, column=1, padx=10)
        
        # Configurar el directorio de descarga
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    
    def download_video(self):
        """Descargar video de Facebook"""
        url = self.video_url.get()
        if url == "Ej: https://www.facebook.com/watch?v=..." or not url:
            messagebox.showerror("Error", "Por favor ingresa una URL válida")
            return
        
        try:
            # Configurar opciones de yt-dlp
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True
            }
            
            # Mostrar ventana de progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Descargando")
            progress_window.geometry("300x100")
            
            progress_label = ttk.Label(progress_window, text="Descargando video...")
            progress_label.pack(pady=20)
            
            def download():
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                        # Actualizar la fecha de modificación al momento actual
                        try:
                            files = [os.path.join(self.download_path, f) for f in os.listdir(self.download_path)]
                            if files:
                                files.sort(key=os.path.getmtime, reverse=True)
                                current_time = time.time()
                                os.utime(files[0], (current_time, current_time))
                        except Exception as file_error:
                            print(f"Error al actualizar fecha de archivo: {str(file_error)}")
                    progress_window.destroy()
                    messagebox.showinfo("Éxito", "Video descargado correctamente")
                except Exception as e:
                    progress_window.destroy()
                    messagebox.showerror("Error", f"Error al descargar: {str(e)}")
            
            threading.Thread(target=download, daemon=True).start()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar la descarga: {str(e)}")
    
    def show_trending(self):
        """Mostrar videos populares de Facebook"""
        try:
            # Lista predefinida de videos populares
            videos_found = [
                {
                    'title': 'Viral: Perrito bailando',
                    'uploader': 'Funny Animals',
                    'url': 'https://www.facebook.com/watch?v=12345',
                    'views': '1.2M',
                    'category': 'Entretenimiento'
                },
                {
                    'title': 'Receta: Pasta Carbonara',
                    'uploader': 'Tasty',
                    'url': 'https://www.facebook.com/watch?v=67890',
                    'views': '800K',
                    'category': 'Cocina'
                },
                {
                    'title': 'Tutorial: Minecraft Tips',
                    'uploader': 'Gaming Zone',
                    'url': 'https://www.facebook.com/watch?v=11223',
                    'views': '500K',
                    'category': 'Gaming'
                }
            ]
            
            # Mostrar ventana de videos
            trends_window = tk.Toplevel(self.root)
            trends_window.title("Videos Populares de Facebook")
            trends_window.geometry("600x500")
            
            # Frame principal
            main_frame = ttk.Frame(trends_window, padding=20)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Título
            ttk.Label(main_frame, 
                     text="🔥 Videos Populares de Facebook",
                     style='Title.TLabel').pack(pady=(0,20))
            
            # Frame de categorías
            categories_frame = ttk.Frame(main_frame)
            categories_frame.pack(fill=tk.X, pady=(0,10))
            
            categories = ['Todos', 'Entretenimiento', 'Cocina', 'Gaming']
            
            def filter_videos(category):
                for widget in content_frame.winfo_children():
                    widget.destroy()
                    
                filtered_videos = videos_found
                if category != 'Todos':
                    filtered_videos = [v for v in videos_found if v['category'] == category]
                    
                show_videos(filtered_videos)
            
            for category in categories:
                ttk.Button(categories_frame,
                          text=category,
                          command=lambda c=category: filter_videos(c),
                          style='Custom.TButton').pack(side=tk.LEFT, padx=5)
            
            # Lista con scroll
            list_frame = ttk.Frame(main_frame)
            list_frame.pack(fill=tk.BOTH, expand=True)
            
            scrollbar = ttk.Scrollbar(list_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            canvas = tk.Canvas(list_frame)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            scrollbar.config(command=canvas.yview)
            canvas.config(yscrollcommand=scrollbar.set)
            
            content_frame = ttk.Frame(canvas)
            canvas.create_window((0,0), window=content_frame, anchor='nw')
            
            def show_videos(videos):
                for video in videos:
                    video_frame = ttk.Frame(content_frame)
                    video_frame.pack(fill=tk.X, pady=5, padx=5)
                    
                    # Información del video
                    ttk.Label(video_frame, 
                            text=video['title'],
                            wraplength=500,
                            style='Title.TLabel').pack(anchor='w')
                    
                    ttk.Label(video_frame,
                            text=f"👤 {video['uploader']} | 👁️ {video['views']} | 🏷️ {video['category']}",
                            style='Info.TLabel').pack(anchor='w')
                    
                    # Frame para botones
                    buttons_frame = ttk.Frame(video_frame)
                    buttons_frame.pack(anchor='w', pady=5)
                    
                    # Botón para ver
                    ttk.Button(buttons_frame,
                             text="Ver",
                             command=lambda url=video['url']: webbrowser.open(url),
                             style='Custom.TButton').pack(side=tk.LEFT, padx=(0,5))
                    
                    # Botón para descargar
                    ttk.Button(buttons_frame,
                             text="Descargar",
                             command=lambda url=video['url']: self.download_video_from_url(url),
                             style='Custom.TButton').pack(side=tk.LEFT)
                    
                    ttk.Separator(video_frame, orient='horizontal').pack(fill=tk.X, pady=5)
            
            # Mostrar todos los videos inicialmente
            show_videos(videos_found)
            
            # Configurar el scroll
            content_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar videos: {str(e)}")
    
    def download_video_from_url(self, url):
        """Descargar video desde URL"""
        self.video_url.set(url)
        self.download_video()
    
    def show_profile_videos(self):
        """Mostrar videos de un perfil"""
        username = self.username.get()
        if username == "Ej: nombre.usuario" or not username:
            messagebox.showerror("Error", "Por favor ingresa un nombre de usuario válido")
            return
        
        messagebox.showinfo("Próximamente", "Esta función estará disponible próximamente")
    
    def change_directory(self):
        """Cambiar directorio de descarga"""
        new_path = filedialog.askdirectory(initialdir=self.download_path)
        if new_path:
            self.download_path = new_path
            messagebox.showinfo("Directorio", f"Directorio de descarga cambiado a:\n{new_path}")
    
    def show_about(self):
        """Mostrar información sobre la aplicación"""
        messagebox.showinfo("Acerca de", 
                          "Facebook Downloader v1.0\n"
                          "Desarrollado con Python y tkinter\n"
                          "© 2025 RakkoTech")

class SocialMediaSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Media Downloader")
        
        # Configurar el tema y estilo
        self.root.configure(bg='#ffffff')
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar estilos personalizados
        style.configure('Main.TFrame', background='#ffffff')
        style.configure('Custom.TButton',
                       padding=10,
                       font=('Segoe UI', 10),
                       background='#4CAF50',
                       foreground='white')
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="20", style='Main.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo o título
        logo_label = ttk.Label(main_frame,
                             text="🌐 Social Media Downloader",
                             font=('Segoe UI', 16, 'bold'),
                             foreground='#333333',
                             background='#ffffff')
        logo_label.pack(pady=(0, 30))
        
        # Frame para los botones superiores
        top_buttons_frame = ttk.Frame(main_frame, style='Main.TFrame')
        top_buttons_frame.pack(fill=tk.X, pady=(0,20))
        
        # Contenedor para los botones para mantenerlos juntos
        buttons_container = ttk.Frame(top_buttons_frame, style='Main.TFrame')
        buttons_container.pack(anchor='center')
        
        # Botón "¿CÓMO VAS?"
        ttk.Button(buttons_container,
                  text="¿CÓMO VAS?",
                  command=self.show_progress,
                  style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        
        # Botón "Chat IA"
        ttk.Button(buttons_container,
                  text="Chat IA",
                  command=self.show_chat_window,
                  style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        
        # Botones de redes sociales
        social_buttons = [
            ("YouTube", YouTubeApp),
            ("TikTok", TikTokApp),
            ("Instagram", InstagramApp)
        ]
        
        for text, app_class in social_buttons:
            button = ttk.Button(main_frame,
                              text=text,
                              command=lambda c=app_class: self.open_app(c),
                              style='Custom.TButton')
            button.pack(fill=tk.X, pady=5)
        
        # Footer
        footer_label = ttk.Label(main_frame,
                               text="© 2025 RakkoTech Social Media Downloader",
                               font=('Segoe UI', 9),
                               foreground='#999999',
                               background='#ffffff')
        footer_label.pack(pady=(40, 20))
    
    def open_app(self, app_class):
        """Abrir una aplicación específica en una nueva ventana"""
        window = tk.Toplevel(self.root)
        app = app_class(window)
    
    def show_progress(self):
        """Mostrar ventana de progreso de descargas"""
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Progreso de Descargas")
        progress_window.geometry("400x300")
        progress_window.transient(self.root)
        
        # Frame principal
        main_frame = ttk.Frame(progress_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame,
                 text="Estado de las Descargas",
                 font=('Segoe UI', 14, 'bold')).pack(pady=(0,20))
        
        # Información de descargas
        info_text = (
            "✅ Descargas completadas hoy: 0\n"
            "⏳ Descargas en progreso: 0\n"
            "❌ Descargas fallidas: 0\n\n"
            "Última descarga: --"
        )
        
        ttk.Label(main_frame,
                 text=info_text,
                 justify=tk.LEFT,
                 font=('Segoe UI', 11)).pack(pady=10)
        
        # Botón para actualizar
        update_button = ttk.Button(main_frame,
                  text="Actualizar",
                  command=lambda: None,
                  style='Custom.TButton')
        update_button.pack(pady=20, padx=20, fill=tk.X)
    
    def show_chat_window(self):
        """Mostrar ventana de chat con IA"""
        # Diálogo de selección de API
        api_dialog = tk.Toplevel(self.root)
        api_dialog.title("Seleccionar API")
        api_dialog.geometry("400x300")  # Aumentar altura
        api_dialog.transient(self.root)
        api_dialog.grab_set()
        api_dialog.resizable(False, False)
        
        # Configurar el fondo
        api_dialog.configure(bg='#ffffff')
        
        # Frame principal del diálogo con fondo blanco
        dialog_frame = ttk.Frame(api_dialog, padding=20, style='Dialog.TFrame')
        dialog_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurar estilos
        style = ttk.Style()
        style.configure('Dialog.TFrame', background='#ffffff')
        style.configure('DialogTitle.TLabel',
                       font=('Segoe UI', 14, 'bold'),
                       foreground='#1a1a1a',
                       background='#ffffff')
        style.configure('DialogRadio.TRadiobutton',
                       font=('Segoe UI', 10),
                       background='#ffffff',
                       padding=5)
        style.configure('DialogButton.TButton',
                       font=('Segoe UI', 10),
                       padding=8,
                       background='#4CAF50',
                       foreground='white')
        
        # Título con icono
        ttk.Label(dialog_frame,
                 text="🤖 Selecciona el Modelo de IA",
                 style='DialogTitle.TLabel').pack(pady=(0,15))
        
        # Frame para las opciones
        options_frame = ttk.Frame(dialog_frame, style='Dialog.TFrame')
        options_frame.pack(fill=tk.X, pady=10)
        
        selected_api = tk.StringVar(value="deepseek")
        
        # Opciones de API con descripciones
        deepseek_frame = ttk.Frame(options_frame, style='Dialog.TFrame')
        deepseek_frame.pack(fill=tk.X, pady=3)
        
        ttk.Radiobutton(deepseek_frame,
                        text="DeepSeek Chat",
                        value="deepseek",
                        variable=selected_api,
                        style='DialogRadio.TRadiobutton').pack(anchor='w')
        ttk.Label(deepseek_frame,
                 text="Modelo avanzado de IA con amplio conocimiento",
                 foreground='#666666',
                 background='#ffffff',
                 font=('Segoe UI', 9)).pack(anchor='w', padx=30)
        
        chatgpt_frame = ttk.Frame(options_frame, style='Dialog.TFrame')
        chatgpt_frame.pack(fill=tk.X, pady=3)
        
        ttk.Radiobutton(chatgpt_frame,
                        text="ChatGPT",
                        value="chatgpt",
                        variable=selected_api,
                        style='DialogRadio.TRadiobutton').pack(anchor='w')
        ttk.Label(chatgpt_frame,
                 text="Modelo conversacional de OpenAI",
                 foreground='#666666',
                 background='#ffffff',
                 font=('Segoe UI', 9)).pack(anchor='w', padx=30)
        
        # Barra de progreso
        progress_frame = ttk.Frame(dialog_frame, style='Dialog.TFrame')
        progress_frame.pack(fill=tk.X, pady=10)
        progress = ttk.Progressbar(progress_frame, mode='determinate', length=200)
        progress.pack()
        progress['value'] = 50  # Valor inicial
        
        def start_chat():
            api_choice = selected_api.get()
            progress['value'] = 100  # Actualizar progreso
            api_dialog.after(500, lambda: api_dialog.destroy())  # Cerrar después de 500ms
            self.create_chat_window(api_choice)
        
        # Frame para el botón
        button_frame = ttk.Frame(dialog_frame, style='Dialog.TFrame')
        button_frame.pack(fill=tk.X, pady=(20,0))
        
        # Botón para iniciar el chat
        ttk.Button(button_frame,
                   text="Iniciar Chat",
                   command=start_chat,
                   style='DialogButton.TButton').pack(expand=True)

    def create_chat_window(self, api_choice):
        """Crear ventana de chat"""
        chat_window = tk.Toplevel(self.root)
        chat_window.title(f"Chat con IA - {api_choice.upper()}")
        chat_window.geometry("600x800")
        
        # Frame principal
        main_frame = ttk.Frame(chat_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Área de chat
        chat_frame = ttk.Frame(main_frame)
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        # Área de mensajes con scroll
        messages_frame = ttk.Frame(chat_frame)
        messages_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas y scrollbar para los mensajes
        canvas = tk.Canvas(messages_frame, bg='#ffffff')
        scrollbar = ttk.Scrollbar(messages_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=550)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Área de entrada
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(20,0))
        
        # Campo de texto para el mensaje
        message_entry = tk.Text(input_frame, height=3, width=50, wrap=tk.WORD)
        message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,10))
        
        def add_message(text, is_user=True):
            """Agregar mensaje al chat"""
            message_frame = ttk.Frame(scrollable_frame)
            message_frame.pack(fill=tk.X, pady=5)
            
            # Alineación según el remitente
            if is_user:
                message_frame.pack_configure(anchor='e')
            else:
                message_frame.pack_configure(anchor='w')
            
            # Estilo del mensaje
            bg_color = '#DCF8C6' if is_user else '#E8E8E8'
            
            message_label = ttk.Label(
                message_frame,
                text=text,
                wraplength=400,
                justify=tk.LEFT,
                padding=10,
                background=bg_color
            )
            message_label.pack(side=tk.RIGHT if is_user else tk.LEFT)
            
            # Scroll al último mensaje
            canvas.update_idletasks()
            canvas.yview_moveto(1.0)
        
        def send_message():
            """Enviar mensaje y obtener respuesta"""
            message = message_entry.get("1.0", tk.END).strip()
            if not message:
                return
            
            # Limpiar campo de entrada
            message_entry.delete("1.0", tk.END)
            
            # Mostrar mensaje del usuario
            add_message(message, is_user=True)
            
            # Deshabilitar entrada mientras se procesa
            message_entry.config(state='disabled')
            send_button.config(state='disabled')
            
            def get_ai_response():
                try:
                    if api_choice == "deepseek":
                        # Usar el SDK de OpenAI con la URL base de Deepseek
                        client = OpenAI(
                            api_key=DEEPSEEK_API_KEY,
                            base_url="https://api.deepseek.com"
                        )
                        
                        response = client.chat.completions.create(
                            model="deepseek-chat",
                            messages=[
                                {"role": "system", "content": "Eres un asistente útil"},
                                {"role": "user", "content": message}
                            ],
                            temperature=0.7,
                            max_tokens=2000,
                            stream=False
                        )
                        
                        ai_message = response.choices[0].message.content
                        chat_window.after(0, lambda: add_message(ai_message, is_user=False))
                        
                    else:  # chatgpt
                        headers = {
                            "Authorization": f"Bearer {CHATGPT_API_KEY}",
                            "Content-Type": "application/json"
                        }
                        data = {
                            "messages": [{"role": "user", "content": message}],
                            "model": "gpt-3.5-turbo",
                            "temperature": 0.7
                        }
                        response = requests.post(
                            "https://api.openai.com/v1/chat/completions",
                            json=data,
                            headers=headers
                        )
                        
                        response.raise_for_status()
                        ai_message = response.json()['choices'][0]['message']['content']
                        chat_window.after(0, lambda: add_message(ai_message, is_user=False))
                    
                except Exception as e:
                    error_msg = str(e)
                    if "401" in error_msg:
                        error_msg = "Error de autenticación. Por favor verifica tu API key."
                    elif "429" in error_msg:
                        error_msg = "Demasiadas solicitudes. Por favor espera un momento."
                    chat_window.after(0, lambda: add_message(f"Error: {error_msg}", is_user=False))
                
                finally:
                    chat_window.after(0, lambda: message_entry.config(state='normal'))
                    chat_window.after(0, lambda: send_button.config(state='normal'))
            
            # Procesar en un hilo separado
            threading.Thread(target=get_ai_response, daemon=True).start()
        
        # Botón de enviar
        send_button = ttk.Button(
            input_frame,
            text="Enviar",
            command=send_message,
            style='Custom.TButton'
        )
        send_button.pack(side=tk.RIGHT)
        
        # Binding para Enter
        message_entry.bind("<Return>", lambda e: send_message() if not e.state & 1 else None)
        message_entry.bind("<Shift-Return>", lambda e: message_entry.insert(tk.END, "\n"))
        
        # Mensaje inicial
        add_message("¡Hola! Soy tu asistente de IA. ¿En qué puedo ayudarte?", is_user=False)
        
        # Dar foco al campo de entrada
        message_entry.focus_set()

def main():
    root = tk.Tk()
    app = SocialMediaSelector(root)
    root.mainloop()

if __name__ == "__main__":
    main()
