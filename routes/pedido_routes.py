from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import controllers.controlador_pedido as controlador_pedido

from flask_jwt_extended import jwt_required, get_jwt_identity

# Crear el Blueprint para pedidos
pedido_bp = Blueprint('pedido_bp', __name__)

# Ruta para mostrar la página de gestión de pedidos
@pedido_bp.route('/menu_man_pedido', methods=["GET"])
def menu_man_pedido():
    pedidos = controlador_pedido.obtener_todos_pedidos()
    usuarios = controlador_pedido.obtener_todos_usuarios()
    return render_template('menuManPedido.html', pedidos=pedidos, usuarios=usuarios)

# Ruta para agregar un nuevo pedido
@pedido_bp.route('/agregar_pedido', methods=["POST"])
def agregar_pedido():
    fechainicio = request.form.get('fechainicio')
    idUsuario = request.form.get('idUsuario')
    
    if not fechainicio or not idUsuario:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for('pedido_bp.menu_man_pedido'))

    try:
        controlador_pedido.agregar_pedido(fechainicio, idUsuario)
        flash("Pedido agregado exitosamente", "success")
    except Exception as e:
        flash(f"Error al agregar pedido: {str(e)}", "error")
    
    return redirect(url_for('pedido_bp.menu_man_pedido'))

# Ruta para actualizar un pedido
@pedido_bp.route('/actualizar_pedido', methods=["POST"])
def actualizar_pedido():
    idPedido = request.form.get('idPedido')
    fechainicio = request.form.get('fechainicio')
    fechafinalizado = request.form.get('fechafinalizado')
    estado = request.form.get('estado')
    idUsuario = request.form.get('idUsuario')
    
    if not idPedido or not fechainicio or not estado or not idUsuario:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for('pedido_bp.menu_man_pedido'))

    try:
        controlador_pedido.actualizar_pedido(idPedido, fechainicio, fechafinalizado, estado, idUsuario)
        flash("Pedido actualizado exitosamente", "success")
    except Exception as e:
        flash(f"Error al actualizar pedido: {str(e)}", "error")

    return redirect(url_for('pedido_bp.menu_man_pedido'))

# Ruta para eliminar un pedido
@pedido_bp.route('/eliminar_pedido/<int:idPedido>', methods=["POST"])
def eliminar_pedido(idPedido):
    try:
        controlador_pedido.eliminar_pedido(idPedido)
        flash("Pedido eliminado exitosamente", "success")
    except Exception as e:
        flash(f"Error al eliminar pedido: {str(e)}", "error")
    
    return redirect(url_for('pedido_bp.menu_man_pedido'))


# ==========================
# INICIO DE APIS PARA PEDIDO
# ==========================

# API para listar todos los pedidos en formato JSON
@pedido_bp.route("/api/listarPedidos", methods=["GET"])
@jwt_required()
def listar_pedidos():
    try:
        pedidos = controlador_pedido.obtener_todos_pedidos()
        return jsonify({"data": pedidos, "message": "Pedidos obtenidos correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})


# API para listar un pedido por ID en formato JSON
@pedido_bp.route("/api/listarPedidoPorId/<int:idPedido>", methods=["GET"])
@jwt_required()
def listar_pedido_por_id(idPedido):
    try:
        pedido = controlador_pedido.obtener_pedido_por_id(idPedido)
        if pedido:
            pedido_dict = {
                "idPedido": pedido[0],
                "fechainicio": pedido[1],
                "fechafinalizado": pedido[2],
                "estado": pedido[3],
                "idUsuario": pedido[4],
                "fechaCreacion": pedido[5],
                "fechaModificacion": pedido[6]
            }
            return jsonify({"data": pedido_dict, "message": "Pedido obtenido correctamente", "status": 1})
        else:
            return jsonify({"data": [], "message": "Pedido no encontrado", "status": 0})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})


# API para eliminar un pedido
@pedido_bp.route("/api/eliminarPedido/<int:idPedido>", methods=["DELETE"])
@jwt_required()
def eliminar_pedido_api(idPedido):
    try:
        controlador_pedido.eliminar_pedido(idPedido)
        return jsonify({"message": f"Pedido con ID {idPedido} eliminado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})


# API para actualizar un pedido
@pedido_bp.route("/api/actualizarPedido/<int:idPedido>", methods=["PUT"])
@jwt_required()
def actualizar_pedido_ruta(idPedido):
    try:
        data = request.json
        controlador_pedido.actualizar_pedido(
            idPedido, data["fechainicio"], data["fechafinalizado"], data["estado"], data["idUsuario"]
        )
        return jsonify({"message": "Pedido actualizado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})


# API para insertar un nuevo pedido desde JSON
@pedido_bp.route("/api/insertarPedido", methods=["POST"])
@jwt_required()
def insertar_pedido_desde_json():
    try:
        data = request.json
        fechainicio = data["fechainicio"]
        idUsuario = data["idUsuario"]
        estado = data.get("estado", "Pendiente de Entrega")  # El estado por defecto es "Pendiente de Entrega"
        
        # Validación de datos
        if not fechainicio or not idUsuario:
            return jsonify({"data": [], "message": "Todos los campos son obligatorios", "status": 0})

        controlador_pedido.agregar_pedido(fechainicio, idUsuario, estado)
        return jsonify({"data": [], "message": "Pedido registrado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})
