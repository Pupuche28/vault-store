from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import controllers.controlador_pagos as controlador_pagos

from flask_jwt_extended import jwt_required, get_jwt_identity

# Crear el Blueprint para pagos
pago_bp = Blueprint('pago_bp', __name__)

# Ruta para listar todos los pagos
@pago_bp.route('/menu_man_pago', methods=["GET"])
def menu_man_pago():
    pagos = controlador_pagos.obtener_pagos()
    return render_template('menuManPago.html', pagos=pagos)

# Ruta para eliminar un pago
@pago_bp.route('/eliminar_pago/<int:idPago>', methods=["POST"])
def eliminar_pago(idPago):
    controlador_pagos.eliminar_pago(idPago)
    flash("Pago eliminado exitosamente", "success")
    return redirect(url_for('pago_bp.menu_man_pago'))


# ==========================
# INICIO DE APIS PARA PAGOS
# ==========================

# API para listar todos los pagos
@pago_bp.route("/api/listarPagos", methods=["GET"])
@jwt_required()
def listar_pagos():
    try:
        pagos = controlador_pagos.obtener_pagos()
        return jsonify({"data": pagos, "message": "Pagos obtenidos correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})


# API para listar un pago por ID
@pago_bp.route("/api/listarPagoPorId/<int:idPago>", methods=["GET"])
@jwt_required()
def listar_pago_por_id(idPago):
    try:
        pago = controlador_pagos.obtener_pago_por_id(idPago)
        if pago:
            pago_dict = {
                "idPago": pago[0],  # idPago
                "fechapago": pago[1],  # Fecha de pago
                "monto": pago[2],  # Monto
                "metodopago": pago[3],  # Método de pago
                "usuario": pago[4],  # Nombre del usuario
                "nroTarjeta": pago[5],  # Número de tarjeta
            }
            return jsonify({"data": pago_dict, "message": "Pago obtenido correctamente", "status": 1})
        else:
            return jsonify({"data": [], "message": "Pago no encontrado", "status": 0})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})


# API para eliminar un pago
@pago_bp.route("/api/eliminarPago/<int:idPago>", methods=["DELETE"])
@jwt_required()
def eliminar_pago_api(idPago):  # Renombrado para evitar conflicto
    try:
        controlador_pagos.eliminar_pago(idPago)
        return jsonify({"message": f"Pago con ID {idPago} eliminado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})


# API para actualizar un pago
@pago_bp.route("/api/actualizarPago/<int:idPago>", methods=["PUT"])
@jwt_required()
def actualizar_pago(idPago):
    try:
        data = request.json
        controlador_pagos.actualizar_pago(
            idPago, 
            data["fechapago"], 
            data["monto"], 
            data["metodopago"], 
            data["idPedido"], 
            data.get("idTarjeta")
        )
        return jsonify({"message": "Pago actualizado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})


# API para insertar un pago
@pago_bp.route("/api/insertarPago", methods=["POST"])
@jwt_required()
def insertar_pago():
    try:
        data = request.json
        fechapago = data["fechapago"]
        monto = data["monto"]
        metodopago = data["metodopago"]
        idPedido = data["idPedido"]
        idTarjeta = data.get("idTarjeta", None)  # idTarjeta puede ser opcional
        
        # Validación de datos
        if not fechapago or not monto or not metodopago or not idPedido:
            return jsonify({"data": [], "message": "Todos los campos son obligatorios", "status": 0})

        controlador_pagos.insertar_pago(fechapago, monto, metodopago, idPedido, idTarjeta)
        return jsonify({"data": [], "message": "Pago registrado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})
