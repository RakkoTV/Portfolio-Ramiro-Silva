import sys
import os
import uuid
import zipfile
import subprocess
import importlib.util
import threading
import time

# Función para verificar si un módulo está instalado
def is_module_installed(module_name):
    return importlib.util.find_spec(module_name) is not None

# Función para instalar un módulo usando pip
def install_module(module_name, package_name=None):
    if package_name is None:
        package_name = module_name
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

# Verificar e instalar dependencias
def check_and_install_dependencies():
    # Primero verificamos si PyQt5 está instalado para poder mostrar el diálogo
    has_pyqt = is_module_installed("PyQt5")
    
    dependencies = [
        {"module": "PyQt5", "package": "PyQt5"},
        {"module": "fitz", "package": "PyMuPDF"}
    ]
    
    missing_deps = []
    for dep in dependencies:
        if not is_module_installed(dep["module"]):
            missing_deps.append(dep)
    
    if not missing_deps:
        return True, []
    
    # Si PyQt5 está instalado, mostramos un diálogo de progreso
    if has_pyqt:
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
        
        dialog = DependencyInstallDialog(missing_deps)
        dialog.show()
    
    # Hay dependencias faltantes, intentar instalarlas
    failed_installs = []
    for i, dep in enumerate(missing_deps):
        status_msg = f"Instalando {dep['package']}..."
        print(status_msg)
        
        if has_pyqt:
            dialog.update_status(dep['package'], "Descargando e instalando...", i)
        
        if not install_module(dep["module"], dep["package"]):
            failed_installs.append(dep["package"])
            if has_pyqt:
                dialog.update_status(dep['package'], "Error al instalar", i+1)
        else:
            if has_pyqt:
                dialog.update_status(dep['package'], "Instalado correctamente", i+1)
    
    if has_pyqt:
        dialog.close()
    
    return len(failed_installs) == 0, failed_installs

# Ahora importamos los módulos necesarios
try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                                QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, 
                                QProgressBar, QScrollArea, QGridLayout, QMessageBox, QDialog)
    from PyQt5.QtGui import QPixmap, QIcon
    from PyQt5.QtCore import Qt, QThread, pyqtSignal
    import fitz  # PyMuPDF
    
    # Diálogo de progreso para la instalación de dependencias
    class DependencyInstallDialog(QDialog):
        def __init__(self, dependencies):
            super().__init__()
            self.setWindowTitle("Instalando Dependencias")
            self.setFixedSize(400, 150)
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            
            layout = QVBoxLayout()
            
            self.status_label = QLabel("Preparando instalación...")
            layout.addWidget(self.status_label)
            
            self.progress_bar = QProgressBar()
            self.progress_bar.setRange(0, len(dependencies))
            self.progress_bar.setValue(0)
            layout.addWidget(self.progress_bar)
            
            self.detail_label = QLabel("")
            layout.addWidget(self.detail_label)
            
            self.setLayout(layout)
            
            # No bloqueamos la interfaz para poder actualizarla
            self.setModal(False)
        
        def update_status(self, package_name, status, progress):
            self.status_label.setText(f"Instalando {package_name}...")
            self.detail_label.setText(status)
            self.progress_bar.setValue(progress)
            QApplication.processEvents()
    
    # Verificar dependencias antes de importar
    all_deps_installed, failed_deps = check_and_install_dependencies()
    
except ImportError as e:
    # Si llegamos aquí, significa que la instalación automática falló
    print(f"Error al importar módulos: {e}")
    print("No se pudieron instalar automáticamente las dependencias.")
    if 'failed_deps' in locals() and failed_deps:
        print(f"Dependencias que no se pudieron instalar: {', '.join(failed_deps)}")
    print("Por favor, instale manualmente las dependencias e intente nuevamente.")
    sys.exit(1)

class PDFConverter(QThread):
    progress_signal = pyqtSignal(int, int)  # (página actual, total de páginas)
    finished_signal = pyqtSignal(list)  # Lista de rutas de imágenes generadas
    error_signal = pyqtSignal(str)  # Mensaje de error
    
    def __init__(self, pdf_paths, output_folder):
        super().__init__()
        self.pdf_paths = pdf_paths
        self.output_folder = output_folder
        
    def run(self):
        all_image_paths = []
        total_pages = 0
        processed_pages = 0
        
        # Primero contamos el total de páginas
        for pdf_path in self.pdf_paths:
            try:
                doc = fitz.open(pdf_path)
                total_pages += len(doc)
                doc.close()
            except Exception as e:
                self.error_signal.emit(f"Error al abrir {os.path.basename(pdf_path)}: {str(e)}")
                return
        
        # Ahora procesamos los PDFs
        for pdf_path in self.pdf_paths:
            try:
                doc = fitz.open(pdf_path)
                original_filename = os.path.basename(pdf_path)
                original_filename_base = os.path.splitext(original_filename)[0]
                
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    pix = page.get_pixmap(dpi=300)  # 300 DPI para mejor calidad
                    
                    # Crear un nombre de archivo único
                    unique_suffix = uuid.uuid4().hex[:8]
                    image_filename = f"{original_filename_base}_page_{page_num+1}_{unique_suffix}.jpeg"
                    image_path = os.path.join(self.output_folder, image_filename)
                    
                    # Guardar la imagen
                    pix.save(image_path)
                    all_image_paths.append(image_path)
                    
                    # Actualizar progreso
                    processed_pages += 1
                    self.progress_signal.emit(processed_pages, total_pages)
                
                doc.close()
            except Exception as e:
                self.error_signal.emit(f"Error al procesar {os.path.basename(pdf_path)}: {str(e)}")
                return
        
        self.finished_signal.emit(all_image_paths)

class ZipCreator(QThread):
    finished_signal = pyqtSignal(str)  # Ruta del archivo ZIP creado
    error_signal = pyqtSignal(str)  # Mensaje de error
    
    def __init__(self, image_paths, output_folder):
        super().__init__()
        self.image_paths = image_paths
        self.output_folder = output_folder
    
    def run(self):
        try:
            # Crear nombre único para el ZIP
            zip_filename = f"converted_images_{uuid.uuid4().hex}.zip"
            zip_path = os.path.join(self.output_folder, zip_filename)
            
            # Crear el archivo ZIP
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for img_path in self.image_paths:
                    # Añadir al ZIP usando solo el nombre base del archivo
                    zipf.write(img_path, os.path.basename(img_path))
            
            self.finished_signal.emit(zip_path)
        except Exception as e:
            self.error_signal.emit(f"Error al crear archivo ZIP: {str(e)}")

class PTJApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PTJ - Convertidor PDF a JPEG")
        self.setMinimumSize(800, 600)
        
        # Crear directorios de trabajo si no existen
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(self.base_dir, "output")
        self.zip_dir = os.path.join(self.base_dir, "zips")
        
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.zip_dir, exist_ok=True)
        
        # Variables para almacenar rutas
        self.pdf_paths = []
        self.image_paths = []
        self.zip_path = ""
        
        # Configurar la interfaz
        self.setup_ui()
    
    def setup_ui(self):
        # Widget principal
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Título
        title_label = QLabel("Convertidor PDF a JPEG")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #1a73e8; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        
        self.select_button = QPushButton("Seleccionar PDFs")
        self.select_button.setStyleSheet("""
            QPushButton {
                background-color: #e8f0fe;
                color: #1a73e8;
                border-radius: 8px;
                padding: 12px 25px;
                font-weight: 500;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #d2e3fc;
            }
        """)
        self.select_button.clicked.connect(self.select_pdfs)
        button_layout.addWidget(self.select_button)
        
        self.convert_button = QPushButton("Convertir")
        self.convert_button.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                border-radius: 8px;
                padding: 12px 25px;
                font-weight: 500;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1558b0;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.convert_button.clicked.connect(self.start_conversion)
        self.convert_button.setEnabled(False)  # Deshabilitado hasta que se seleccionen archivos
        button_layout.addWidget(self.convert_button)
        
        main_layout.addLayout(button_layout)
        
        # Etiqueta para mostrar archivos seleccionados
        self.files_label = QLabel("No hay archivos seleccionados")
        self.files_label.setStyleSheet("margin-top: 10px; color: #555;")
        self.files_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.files_label)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 5px;
                text-align: center;
                margin-top: 20px;
            }
            QProgressBar::chunk {
                background-color: #1a73e8;
                border-radius: 5px;
            }
        """)
        self.progress_bar.hide()
        main_layout.addWidget(self.progress_bar)
        
        # Área de visualización de imágenes
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #eee;
                border-radius: 8px;
                background-color: #f9f9f9;
                margin-top: 20px;
            }
        """)
        
        self.image_container = QWidget()
        self.image_layout = QGridLayout(self.image_container)
        self.scroll_area.setWidget(self.image_container)
        main_layout.addWidget(self.scroll_area)
        
        # Botón de descarga ZIP
        self.download_button = QPushButton("Descargar Todo (ZIP)")
        self.download_button.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                border-radius: 8px;
                padding: 12px 25px;
                font-weight: 500;
                font-size: 16px;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #1558b0;
            }
        """)
        self.download_button.clicked.connect(self.open_zip)
        self.download_button.hide()
        main_layout.addWidget(self.download_button)
        
        # Establecer el widget principal
        self.setCentralWidget(main_widget)
    
    def select_pdfs(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Archivos PDF (*.pdf)")
        
        if file_dialog.exec_():
            self.pdf_paths = file_dialog.selectedFiles()
            
            if self.pdf_paths:
                # Actualizar etiqueta con archivos seleccionados
                if len(self.pdf_paths) == 1:
                    self.files_label.setText(f"1 archivo seleccionado: {os.path.basename(self.pdf_paths[0])}")
                else:
                    self.files_label.setText(f"{len(self.pdf_paths)} archivos seleccionados")
                
                # Habilitar botón de conversión
                self.convert_button.setEnabled(True)
    
    def start_conversion(self):
        if not self.pdf_paths:
            QMessageBox.warning(self, "Advertencia", "No hay archivos PDF seleccionados.")
            return
        
        # Limpiar imágenes anteriores
        self.clear_images()
        
        # Ocultar botón de descarga
        self.download_button.hide()
        
        # Mostrar barra de progreso
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        
        # Deshabilitar botones durante la conversión
        self.select_button.setEnabled(False)
        self.convert_button.setEnabled(False)
        
        # Iniciar el proceso de conversión en un hilo separado
        self.converter = PDFConverter(self.pdf_paths, self.output_dir)
        self.converter.progress_signal.connect(self.update_progress)
        self.converter.finished_signal.connect(self.conversion_finished)
        self.converter.error_signal.connect(self.show_error)
        self.converter.start()
    
    def update_progress(self, current, total):
        progress_percentage = int((current / total) * 100)
        self.progress_bar.setValue(progress_percentage)
        self.progress_bar.setFormat(f"{current}/{total} páginas procesadas ({progress_percentage}%)")
    
    def conversion_finished(self, image_paths):
        self.image_paths = image_paths
        
        # Mostrar las imágenes en la interfaz
        self.display_images()
        
        # Crear archivo ZIP
        self.create_zip()
        
        # Habilitar botones
        self.select_button.setEnabled(True)
        self.convert_button.setEnabled(True)
        
        # Ocultar barra de progreso
        self.progress_bar.hide()
    
    def display_images(self):
        # Limpiar el contenedor de imágenes
        self.clear_images()
        
        # Mostrar las imágenes en una cuadrícula
        cols = 3  # Número de columnas en la cuadrícula
        for i, img_path in enumerate(self.image_paths):
            try:
                # Crear un QLabel para mostrar la imagen
                img_label = QLabel()
                pixmap = QPixmap(img_path)
                pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                img_label.setPixmap(pixmap)
                img_label.setAlignment(Qt.AlignCenter)
                img_label.setStyleSheet("""
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 5px;
                    background-color: white;
                """)
                
                # Añadir a la cuadrícula
                row, col = divmod(i, cols)
                self.image_layout.addWidget(img_label, row, col)
            except Exception as e:
                print(f"Error al mostrar imagen {img_path}: {str(e)}")
    
    def clear_images(self):
        # Eliminar todos los widgets del layout
        while self.image_layout.count():
            item = self.image_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
    
    def create_zip(self):
        if not self.image_paths:
            return
        
        # Crear ZIP en un hilo separado
        self.zip_creator = ZipCreator(self.image_paths, self.zip_dir)
        self.zip_creator.finished_signal.connect(self.zip_created)
        self.zip_creator.error_signal.connect(self.show_error)
        self.zip_creator.start()
    
    def zip_created(self, zip_path):
        self.zip_path = zip_path
        self.download_button.show()
    
    def open_zip(self):
        if os.path.exists(self.zip_path):
            # En Windows, esto abrirá el archivo con la aplicación predeterminada
            os.startfile(self.zip_path)
        else:
            QMessageBox.warning(self, "Error", "El archivo ZIP no existe o no se puede acceder.")
    
    def show_error(self, error_message):
        QMessageBox.critical(self, "Error", error_message)
        
        # Habilitar botones en caso de error
        self.select_button.setEnabled(True)
        self.convert_button.setEnabled(True)
        self.progress_bar.hide()

class SplashScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PTJ - Iniciando")
        self.setFixedSize(400, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        layout = QVBoxLayout()
        
        # Título
        title_label = QLabel("PTJ - Convertidor PDF a JPEG")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #1a73e8;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Mensaje
        self.message_label = QLabel("Verificando dependencias...")
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Modo indeterminado
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
        
    def update_message(self, message):
        self.message_label.setText(message)
        QApplication.processEvents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Estilo moderno
    
    # Mostrar pantalla de bienvenida
    splash = SplashScreen()
    splash.show()
    
    # Pequeña pausa para que se muestre la pantalla de bienvenida
    splash.update_message("Iniciando aplicación...")
    time.sleep(1)
    
    # Iniciar la aplicación principal
    window = PTJApp()
    
    # Cerrar la pantalla de bienvenida y mostrar la ventana principal
    splash.close()
    window.show()
    
    sys.exit(app.exec_())