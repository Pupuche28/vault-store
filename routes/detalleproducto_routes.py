from flask import Blueprint, render_template
from controllers.controlador_detalleproducto import obtener_producto_por_id

detalle_producto_bp = Blueprint('detalle_producto', __name__)

@detalle_producto_bp.route('/producto/<int:id_producto>')
def detalle_producto(id_producto):
    # Obtener el producto desde la base de datos
    producto = obtener_producto_por_id(id_producto)
    if producto:
        # Renderizar la plantilla con los datos del producto
        return render_template('productodetalle.html', producto=producto)
    else:
        return "Producto no encontrado", 404
