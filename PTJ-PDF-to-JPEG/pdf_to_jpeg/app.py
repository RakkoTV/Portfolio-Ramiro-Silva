import os
import uuid
import fitz  # PyMuPDF
from flask import Flask, request, render_template, jsonify, url_for, send_from_directory
import zipfile
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = 'temp_uploads'
STATIC_IMAGE_FOLDER = os.path.join('static', 'uploads')
ZIP_FOLDER = 'temp_zips' # Carpeta para guardar los ZIPs temporalmente
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_IMAGE_FOLDER'] = STATIC_IMAGE_FOLDER
app.config['ZIP_FOLDER'] = ZIP_FOLDER

# Asegurarse de que las carpetas existan
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_IMAGE_FOLDER, exist_ok=True)
os.makedirs(ZIP_FOLDER, exist_ok=True)

# Función para convertir PDF a JPEGs
def pdf_to_jpegs(pdf_path, static_output_folder, original_filename):
    doc = fitz.open(pdf_path)
    results = [] # Almacenará tuplas (url, path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300) # Aumentar DPI para mejor calidad
        original_filename_base = os.path.splitext(original_filename)[0]
        # Crear un nombre de archivo único para evitar colisiones
        unique_suffix = uuid.uuid4().hex[:8]
        image_filename = f"{original_filename_base}_page_{page_num+1}_{unique_suffix}.jpeg"
        image_path = os.path.join(static_output_folder, image_filename)
        pix.save(image_path)
        # Generar la URL relativa para usar en el frontend
        image_url = url_for('static', filename=f'uploads/{image_filename}')
        results.append({'url': image_url, 'path': image_path})
    doc.close()
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No files part in the request'}), 400
    files = request.files.getlist('file')
    if not files or all(f.filename == '' for f in files):
        return jsonify({'error': 'No selected files'}), 400

    all_results = [] # Almacenará diccionarios {'url': ..., 'path': ...}
    temp_pdf_paths_to_clean = [] # Almacenar rutas de PDF temporales
    conversion_errors = []

    for file in files:
        if file and file.filename.lower().endswith('.pdf'):
            # Crear directorio temporal para el PDF si no existe
            temp_pdf_dir = app.config['UPLOAD_FOLDER']
            # Crear directorio estático para las imágenes si no existe
            static_image_dir = app.config['STATIC_IMAGE_FOLDER']

            # Guardar PDF en directorio temporal
            safe_filename = f"input_{uuid.uuid4().hex}.pdf"
            pdf_path = os.path.join(temp_pdf_dir, safe_filename)
            try:
                file.save(pdf_path)
                temp_pdf_paths_to_clean.append(pdf_path) # Añadir a la lista de limpieza
            except Exception as e:
                print(f"Error saving file {file.filename}: {str(e)}")
                conversion_errors.append(f"Error saving {file.filename}")
                continue # Saltar al siguiente archivo

            # Convertir PDF a imágenes (guardadas en static/uploads)
            try:
                # pdf_to_jpegs ahora devuelve una lista de diccionarios {'url': ..., 'path': ...}
                image_results = pdf_to_jpegs(pdf_path, static_image_dir, file.filename)
                all_results.extend(image_results)
            except Exception as e:
                print(f"Error converting {file.filename}: {str(e)}")
                conversion_errors.append(f"Error converting {file.filename}")
                # Continuar con otros archivos
                continue # Saltar al siguiente archivo
        elif file.filename:
            # Opcional: informar al usuario sobre archivos inválidos
            print(f"Skipping non-PDF file: {file.filename}")
            conversion_errors.append(f"Skipped non-PDF: {file.filename}")

    # Limpiar los archivos PDF temporales después de la conversión
    for pdf_path in temp_pdf_paths_to_clean:
        try:
            os.remove(pdf_path)
        except OSError as e:
            print(f"Error cleaning up temporary PDF {pdf_path}: {e}")

    image_urls = [result['url'] for result in all_results]
    image_paths = [result['path'] for result in all_results]
    zip_url = None
    zip_filename = None

    # Crear ZIP si se generaron imágenes
    if image_paths:
        try:
            zip_filename = f"converted_images_{uuid.uuid4().hex}.zip"
            zip_path = os.path.join(app.config['ZIP_FOLDER'], zip_filename)

            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for img_path in image_paths:
                    # Añadir al zip usando solo el nombre base del archivo
                    zipf.write(img_path, os.path.basename(img_path))

            zip_url = url_for('download_zip', filename=zip_filename)

            # Limpiar las imágenes individuales generadas (opcional, si no se quieren mantener)
            # for img_path in image_paths:
            #     try:
            #         os.remove(img_path)
            #     except OSError as e:
            #         print(f"Error cleaning up image {img_path}: {e}")

        except Exception as e:
            print(f"Error creating zip file: {str(e)}")
            conversion_errors.append("Error creating ZIP file.")
            zip_url = None # Asegurarse de que no se envíe una URL de zip si falla

    # Preparar respuesta
    response_data = {'image_urls': image_urls}
    if zip_url:
        response_data['zip_url'] = zip_url
    if conversion_errors:
        response_data['errors'] = conversion_errors # Opcional: informar errores específicos

    if not image_urls and not zip_url:
        # Si no hubo éxito en absoluto
        error_msg = 'No valid PDFs processed or conversion failed for all files.'
        if conversion_errors:
            error_msg += " Errors: " + "; ".join(conversion_errors)
        return jsonify({'error': error_msg}), 400

    # Devolver las URLs de las imágenes y/o del ZIP
    return jsonify(response_data)

# Nueva ruta para descargar el archivo ZIP
@app.route('/download_zip/<filename>')
def download_zip(filename):
    zip_folder_path = os.path.abspath(app.config['ZIP_FOLDER'])
    file_path = os.path.join(zip_folder_path, filename)

    # Verificar que el archivo existe y está dentro de la carpeta esperada
    if not os.path.exists(file_path) or not os.path.abspath(file_path).startswith(zip_folder_path):
        return "File not found", 404



    return send_from_directory(app.config['ZIP_FOLDER'], filename, as_attachment=True)

@app.route('/status')
def status():
    # Simple check to confirm the server is running
    # Could be expanded to check dependencies like PyMuPDF availability
    try:
        # Attempt a basic PyMuPDF operation (optional, can be more complex)
        # fitz.Document()
        return jsonify({'status': 'ok', 'message': 'Server and dependencies seem fine.'})
    except Exception as e:
        print(f"Status check error: {e}")
        return jsonify({'status': 'error', 'message': 'Server is running, but a dependency might be missing or causing issues.'}), 500

if __name__ == '__main__':
    # Make sure to use 0.0.0.0 to be accessible on the network if needed
    # The default port is 5000
    app.run(host='0.0.0.0', port=5000, debug=True)