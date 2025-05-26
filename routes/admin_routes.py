from flask import Blueprint, render_template

# Crear el blueprint de admin
admin_bp = Blueprint('admin_bp', __name__)

# Definir la ruta para el menú del administrador
@admin_bp.route('/menu_administrador')
def menu_administrador():
    return render_template('menuAdministrador.html')  # Asegúrate de tener este archivo HTML en tu carpeta de plantillas

