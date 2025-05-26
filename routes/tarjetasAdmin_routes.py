from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import controllers.controlador_tarjetasAdmin as controlador_tarjetas

from flask_jwt_extended import jwt_required, get_jwt_identity

# Crear el Blueprint para tarjetas bajo la nueva denominación tarjetaAdmin_bp
tarjetaAdmin_bp = Blueprint('tarjetaAdmin_bp', __name__)

# ==========================
# Funcionalidades para la página
# ==========================

# Ruta para mostrar la página de gestión de tarjetas
@tarjetaAdmin_bp.route('/menu_man_tarjeta', methods=["GET"])
def menu_man_tarjeta():
    tarjetas = controlador_tarjetas.obtener_todas_tarjetas()
    usuarios = controlador_tarjetas.obtener_todos_usuarios()
    return render_template('menuManTarjeta.html', tarjetas=tarjetas, usuarios=usuarios)

# Ruta para agregar una nueva tarjeta
@tarjetaAdmin_bp.route('/agregar_tarjeta', methods=["POST"])
def agregar_tarjeta():
    nombre = request.form.get('nombre')
    nroTarjeta = request.form.get('nroTarjeta')
    fecha = request.form.get('fecha')
    idUsuario = request.form.get('idUsuario')
    
    controlador_tarjetas.agregar_tarjeta(nombre, nroTarjeta, fecha, idUsuario)
    flash("Tarjeta agregada exitosamente", "success")
    return redirect(url_for('tarjetaAdmin_bp.menu_man_tarjeta'))

# Ruta para actualizar una tarjeta
@tarjetaAdmin_bp.route('/actualizar_tarjeta', methods=["POST"])
def actualizar_tarjeta():
    idTarjeta = request.form.get('idTarjeta')
    nombre = request.form.get('nombre')
    nroTarjeta = request.form.get('nroTarjeta')
    fecha = request.form.get('fecha')
    idUsuario = request.form.get('idUsuario')
    
    controlador_tarjetas.actualizar_tarjeta(idTarjeta, nombre, nroTarjeta, fecha, idUsuario)
    flash("Tarjeta actualizada exitosamente", "success")
    return redirect(url_for('tarjetaAdmin_bp.menu_man_tarjeta'))

# Ruta para eliminar una tarjeta
@tarjetaAdmin_bp.route('/eliminar_tarjeta/<int:idTarjeta>', methods=["POST"])
def eliminar_tarjeta(idTarjeta):
    controlador_tarjetas.eliminar_tarjeta(idTarjeta)
    flash("Tarjeta eliminada exitosamente", "success")
    return redirect(url_for('tarjetaAdmin_bp.menu_man_tarjeta'))

# ==========================
# INICIO DE APIS
# ==========================

# API para listar todas las tarjetas en formato JSON
@tarjetaAdmin_bp.route("/api/listarTarjetas", methods=["GET"])
@jwt_required()
def listar_tarjetas():
    try:
        tarjetas = controlador_tarjetas.obtener_todas_tarjetas()
        return jsonify({"data": tarjetas, "message": "Tarjetas obtenidas correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para listar una tarjeta por ID en formato JSON
@tarjetaAdmin_bp.route("/api/listarTarjetaPorId/<int:idTarjeta>", methods=["GET"])
@jwt_required()
def listar_tarjeta_por_id(idTarjeta):
    try:
        tarjeta = controlador_tarjetas.obtener_tarjeta_por_id(idTarjeta)
        if tarjeta:
            return jsonify({"data": tarjeta, "message": "Tarjeta obtenida correctamente", "status": 1})
        else:
            return jsonify({"data": [], "message": "Tarjeta no encontrada", "status": 0})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para agregar una nueva tarjeta
@tarjetaAdmin_bp.route("/api/insertarTarjeta", methods=["POST"])
@jwt_required()
def insertar_tarjeta_api():
    try:
        data = request.json
        nombre = data.get("nombre")
        nroTarjeta = data.get("nroTarjeta")
        fecha = data.get("fecha")
        idUsuario = data.get("idUsuario")
        if not (nombre and nroTarjeta and fecha and idUsuario):
            return jsonify({"data": [], "message": "Todos los campos son obligatorios", "status": -1})
        controlador_tarjetas.agregar_tarjeta(nombre, nroTarjeta, fecha, idUsuario)
        return jsonify({"message": "Tarjeta agregada correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})

# API para actualizar una tarjeta
@tarjetaAdmin_bp.route("/api/actualizarTarjeta/<int:idTarjeta>", methods=["PUT"])
@jwt_required()
def actualizar_tarjeta_api(idTarjeta):
    try:
        data = request.json
        nombre = data.get("nombre")
        nroTarjeta = data.get("nroTarjeta")
        fecha = data.get("fecha")
        idUsuario = data.get("idUsuario")
        if not (nombre and nroTarjeta and fecha and idUsuario):
            return jsonify({"data": [], "message": "Todos los campos son obligatorios", "status": -1})
        controlador_tarjetas.actualizar_tarjeta(idTarjeta, nombre, nroTarjeta, fecha, idUsuario)
        return jsonify({"message": "Tarjeta actualizada correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})

# API para eliminar una tarjeta
@tarjetaAdmin_bp.route("/api/eliminarTarjeta/<int:idTarjeta>", methods=["DELETE"])
@jwt_required()
def eliminar_tarjeta_api(idTarjeta):
    try:
        controlador_tarjetas.eliminar_tarjeta(idTarjeta)
        return jsonify({"message": f"Tarjeta con ID {idTarjeta} eliminada correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})
