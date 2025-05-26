from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import controllers.controlador_detalleAdmin as controlador_detalleAdmin
from flask_jwt_extended import jwt_required

# Crear el Blueprint para los detalles de pedido
detalleAdmin_bp = Blueprint('detalleAdmin', __name__, url_prefix='/detalle')


# Ruta para listar todos los detalles de los pedidos
@detalleAdmin_bp.route('/menu_man_detalle', methods=["GET"])
def menu_man_detalle():
    detalles = controlador_detalleAdmin.obtener_detalles_pedido()
    return render_template('menuManDetalle.html', detalles=detalles)

# Ruta para eliminar un detalle de pedido
@detalleAdmin_bp.route('/eliminar_detalle/<int:idPedido>/<int:idProducto>', methods=["POST"])
def eliminar_detalle(idPedido, idProducto):
    controlador_detalleAdmin.eliminar_detalle_pedido(idPedido, idProducto)
    flash("Detalle de pedido eliminado exitosamente", "success")
    return redirect(url_for('detalleAdmin.menu_man_detalle'))

# ==========================
# INICIO DE APIS PARA DETALLES
# ==========================

# API para listar todos los detalles de los pedidos
@detalleAdmin_bp.route("/api/listarDetalles", methods=["GET"])
@jwt_required()
def listar_detalles():
    try:
        detalles = controlador_detalleAdmin.obtener_detalles_pedido()
        return jsonify({"data": detalles, "message": "Detalles obtenidos correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para listar un detalle por ID de pedido
@detalleAdmin_bp.route("/api/listarDetallePorIdPedido/<int:idPedido>", methods=["GET"])
@jwt_required()
def listar_detalle_por_id_pedido(idPedido):
    try:
        detalles = controlador_detalleAdmin.obtener_detalle_por_pedido(idPedido)
        if detalles:
            detalle_dict = [{
                "idPedido": detalle[0],
                "idProducto": detalle[1],
                "cantidad": detalle[2],
                "precio": detalle[3],
                "descuento": detalle[4],
                "igv": detalle[5],
                "subtotal": detalle[6],
                "total": detalle[7],
                "nombredeproducto": detalle[8]
            } for detalle in detalles]
            return jsonify({"data": detalle_dict, "message": "Detalles obtenidos correctamente", "status": 1})
        else:
            return jsonify({"data": [], "message": "Detalles no encontrados", "status": 0})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para eliminar un detalle de pedido
@detalleAdmin_bp.route("/api/eliminarDetalle/<int:idPedido>/<int:idProducto>", methods=["DELETE"])
@jwt_required()
def eliminar_detalle_api(idPedido, idProducto):
    try:
        controlador_detalleAdmin.eliminar_detalle_pedido(idPedido, idProducto)
        return jsonify({"message": f"Detalle de pedido con ID {idPedido} y Producto {idProducto} eliminado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})

# API para actualizar un detalle de pedido
@detalleAdmin_bp.route("/api/actualizarDetalle/<int:idPedido>/<int:idProducto>", methods=["PUT"])
@jwt_required()
def actualizar_detalle(idPedido, idProducto):
    try:
        data = request.json
        controlador_detalleAdmin.actualizar_detalle_pedido(
            idPedido,
            idProducto,
            data["cantidad"],
            data["precio"],
            data.get("descuento", 0),
            data.get("igv", 0),
            data["subtotal"],
            data["total"]
        )
        return jsonify({"message": "Detalle de pedido actualizado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})

# API para insertar un detalle de pedido
@detalleAdmin_bp.route("/api/insertarDetalle", methods=["POST"])
@jwt_required()
def insertar_detalle():
    try:
        data = request.json
        idPedido = data["idPedido"]
        idProducto = data["idProducto"]
        cantidad = data["cantidad"]
        precio = data["precio"]
        descuento = data.get("descuento", 0)
        igv = data.get("igv", 0)
        subtotal = data["subtotal"]
        total = data["total"]

        # Validación de datos
        if not all([idPedido, idProducto, cantidad, precio, subtotal, total]):
            return jsonify({"data": [], "message": "Faltan datos requeridos", "status": 0})

        controlador_detalleAdmin.insertar_detalle_pedido(idPedido, idProducto, cantidad, precio, descuento, igv, subtotal, total)
        return jsonify({"data": [], "message": "Detalle de pedido registrado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})
