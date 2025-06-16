from flask import Blueprint, request, jsonify, send_file
from controllers.controlador_archivos import guardar_archivo, obtener_archivos_usuario, obtener_archivo_por_id
from flask_login import login_required, current_user
import os

archivos_bp = Blueprint('archivos', __name__)

@archivos_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No se ha enviado ningún archivo'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se ha seleccionado ningún archivo'}), 400
    
    result = guardar_archivo(file, current_user.id)
    if result['success']:
        return jsonify({
            'message': 'Archivo subido exitosamente',
            'archivo': result['archivo']
        }), 200
    else:
        return jsonify({'error': result['error']}), 400

@archivos_bp.route('/list', methods=['GET'])
@login_required
def list_files():
    archivos = obtener_archivos_usuario(current_user.id)
    return jsonify({'archivos': archivos}), 200

@archivos_bp.route('/download/<int:archivo_id>', methods=['GET'])
@login_required
def download_file(archivo_id):
    archivo = obtener_archivo_por_id(archivo_id)
    if archivo and archivo['usuario_id'] == current_user.id:
        return send_file(
            archivo['ruta'],
            as_attachment=True,
            download_name=archivo['nombre']
        )
    return jsonify({'error': 'Archivo no encontrado'}), 404 