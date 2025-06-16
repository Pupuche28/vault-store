import os
from flask import current_app
from werkzeug.utils import secure_filename
from datetime import datetime

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

# Lista para almacenar la información de los archivos
archivos_subidos = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def guardar_archivo(archivo, usuario_id):
    if archivo and allowed_file(archivo.filename):
        filename = secure_filename(archivo.filename)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        
        # Generar un nombre único para el archivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        archivo.save(filepath)
        
        # Guardar información del archivo
        archivo_info = {
            'id': len(archivos_subidos) + 1,
            'nombre': filename,
            'nombre_archivo': unique_filename,
            'fecha_subida': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'usuario_id': usuario_id,
            'ruta': filepath
        }
        archivos_subidos.append(archivo_info)
        
        return {'success': True, 'archivo': archivo_info}
    return {'success': False, 'error': 'Tipo de archivo no permitido'}

def obtener_archivos_usuario(usuario_id):
    return [archivo for archivo in archivos_subidos if archivo['usuario_id'] == usuario_id]

def obtener_archivo_por_id(archivo_id):
    for archivo in archivos_subidos:
        if archivo['id'] == archivo_id:
            return archivo
    return None 