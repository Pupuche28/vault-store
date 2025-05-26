from flask import Blueprint, request, jsonify
import controllers.controlador_carrito as controlador_carrito

# Crear el Blueprint para el carrito
carrito_bp = Blueprint('carrito_bp', __name__)

# Ruta para agregar productos al carrito
@carrito_bp.route('/agregar_producto', methods=["POST"])
def agregar_producto():
    data = request.json
    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad', 1)

    try:
        controlador_carrito.agregar_al_carrito(producto_id, cantidad)
        return jsonify({"mensaje": "Producto agregado al carrito correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Ruta para obtener los productos del carrito
@carrito_bp.route('/obtener_productos', methods=["GET"])
def obtener_productos():
    try:
        productos = controlador_carrito.obtener_carrito()
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Ruta para eliminar un producto del carrito
@carrito_bp.route('/eliminar_producto', methods=["POST"])
def eliminar_producto():
    data = request.json
    producto_id = data.get('producto_id')

    try:
        controlador_carrito.eliminar_del_carrito(producto_id)
        return jsonify({"mensaje": "Producto eliminado del carrito correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
