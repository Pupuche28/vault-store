from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import controllers.controlador_roles as controlador_roles  # Importa el controlador de roles

from flask_jwt_extended import jwt_required, get_jwt_identity

# Crear el Blueprint para roles
rol_bp = Blueprint('rol_bp', __name__)

# Ruta para mostrar la página de gestión de roles
@rol_bp.route('/menu_man_rol', methods=["GET"])
def menu_man_rol():
    roles = controlador_roles.obtener_roles()  # Llama al controlador para obtener roles
    return render_template('menuManRol.html', roles=roles)

# Ruta para agregar un nuevo rol
@rol_bp.route('/agregar_rol', methods=["POST"])
def agregar_rol():
    nombre = request.form.get('nombre')
    if not nombre:
        flash("El nombre del rol es obligatorio", "error")
        return redirect(url_for('rol_bp.menu_man_rol'))

    controlador_roles.agregar_rol(nombre)  # Llama al controlador para agregar el rol
    flash("Rol agregado exitosamente", "success")
    return redirect(url_for('rol_bp.menu_man_rol'))

# Ruta para actualizar un rol
@rol_bp.route('/actualizar_rol', methods=["POST"])
def actualizar_rol():
    idRol = request.form.get('idRol')
    nombre = request.form.get('nombre')
    if not idRol or not nombre:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for('rol_bp.menu_man_rol'))

    controlador_roles.actualizar_rol(idRol, nombre)  # Llama al controlador para actualizar el rol
    flash("Rol actualizado exitosamente", "success")
    return redirect(url_for('rol_bp.menu_man_rol'))

# Ruta para eliminar un rol
@rol_bp.route('/eliminar_rol/<int:idRol>', methods=["POST"])
def eliminar_rol(idRol):
    controlador_roles.eliminar_rol(idRol)  # Llama al controlador para eliminar el rol
    flash("Rol eliminado exitosamente", "success")
    return redirect(url_for('rol_bp.menu_man_rol'))

# ==========================
# INICIO DE APIS
# ==========================

# API para listar todos los roles en formato JSON
@rol_bp.route("/api/listarRoles", methods=["GET"])
@jwt_required()
def listar_roles():
    try:
        roles = controlador_roles.obtener_roles()
        return jsonify({"data": roles, "message": "Roles obtenidos correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para listar un rol por ID en formato JSON
@rol_bp.route("/api/listarRolPorId/<int:idRol>", methods=["GET"])
@jwt_required()
def listar_rol_por_id(idRol):
    try:
        rol = controlador_roles.obtener_rol_por_id(idRol)
        if rol:
            return jsonify({"data": rol, "message": "Rol obtenido correctamente", "status": 1})
        else:
            return jsonify({"data": [], "message": "Rol no encontrado", "status": 0})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para agregar un nuevo rol
@rol_bp.route("/api/insertarRol", methods=["POST"])
@jwt_required()
def insertar_rol():
    try:
        data = request.json
        nombre = data.get("nombre")
        if not nombre:
            return jsonify({"data": [], "message": "El nombre del rol es obligatorio", "status": -1})
        controlador_roles.agregar_rol(nombre)
        return jsonify({"message": "Rol agregado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})

# API para actualizar un rol
@rol_bp.route("/api/actualizarRol/<int:idRol>", methods=["PUT"])
@jwt_required()
def actualizar_rol_api(idRol):
    try:
        data = request.json
        nombre = data.get("nombre")
        if not nombre:
            return jsonify({"data": [], "message": "El nombre del rol es obligatorio", "status": -1})
        controlador_roles.actualizar_rol(idRol, nombre)
        return jsonify({"message": "Rol actualizado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})

# API para eliminar un rol
@rol_bp.route("/api/eliminarRol/<int:idRol>", methods=["DELETE"])
@jwt_required()
def eliminar_rol_api(idRol):
    try:
        controlador_roles.eliminar_rol(idRol)
        return jsonify({"message": f"Rol con ID {idRol} eliminado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})