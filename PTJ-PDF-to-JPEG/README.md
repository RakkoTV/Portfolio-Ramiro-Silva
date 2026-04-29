# PTJ - Convertidor PDF a JPEG

Esta aplicación permite convertir archivos PDF a imágenes JPEG de alta calidad. La aplicación verifica automáticamente si las dependencias necesarias están instaladas y las instala si es necesario.

## Características

- Conversión de múltiples archivos PDF a imágenes JPEG
- Calidad de imagen configurable (300 DPI por defecto)
- Creación automática de archivos ZIP con todas las imágenes generadas
- Interfaz gráfica intuitiva y moderna
- Instalación automática de dependencias

## Requisitos

- Windows 7/8/10/11
- Python 3.6 o superior (si se ejecuta desde el código fuente)
- Conexión a Internet (solo para la instalación automática de dependencias)

## Instalación

### Opción 1: Ejecutable independiente

1. Descargue el archivo ejecutable `PTJ.exe` de la sección de releases
2. Ejecute el archivo descargado
3. La aplicación verificará e instalará automáticamente las dependencias necesarias si no están presentes

### Opción 2: Desde el código fuente

1. Clone o descargue este repositorio
2. Ejecute el archivo `PTJ.py`:
   ```
   python PTJ.py
   ```
3. La aplicación verificará e instalará automáticamente las dependencias necesarias si no están presentes

## Compilación del ejecutable

Si desea compilar su propio ejecutable, siga estos pasos:

1. Asegúrese de tener PyInstaller instalado:
   ```
   pip install pyinstaller
   ```

2. Compile el ejecutable usando el archivo spec incluido:
   ```
   pyinstaller ptj.spec
   ```

3. El ejecutable se generará en la carpeta `dist`

## Uso

1. Inicie la aplicación
2. Haga clic en "Seleccionar PDFs" para elegir uno o más archivos PDF
3. Haga clic en "Convertir" para iniciar el proceso de conversión
4. Una vez finalizada la conversión, se mostrarán las imágenes generadas
5. Haga clic en "Descargar Todo (ZIP)" para obtener un archivo ZIP con todas las imágenes

## Solución de problemas

Si la instalación automática de dependencias falla, puede instalarlas manualmente con los siguientes comandos:

```
pip install PyQt5
pip install PyMuPDF
```

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.