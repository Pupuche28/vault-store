from flask import Blueprint
from controllers.controlador_tipoentrega import cargar_tipo_entrega

# Crear el Blueprint para las rutas relacionadas con el tipo de entrega
tipo_entrega_bp = Blueprint('tipo_entrega', __name__)

# Definir la ruta para mostrar la página de tipo de entrega
@tipo_entrega_bp.route('/tipoentrega')
def mostrar_tipo_entrega():
    return cargar_tipo_entrega()  # Llamar a la función del controlador para renderizar la página
