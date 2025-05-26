from flask import Blueprint, jsonify, request, flash, redirect, render_template, url_for
import controllers.controlador_usuarios as controlador_usuarios
import controllers.controlador_resenas as controlador_resenas
import traceback  # Importar traceback para manejo de errores detallado

from flask_jwt_extended import jwt_required, get_jwt_identity


# Crear el blueprint para usuario
usuario_bp = Blueprint('usuario_bp', __name__)

# ==========================
# FUNCIONALIDAD
# ==========================

# Ruta para registrar un usuario
@usuario_bp.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nombres = request.form.get("nombres")
        apellidos = request.form.get("apellidos")
        email = request.form.get("email")
        telefono = request.form.get("telefono")
        documento = request.form.get("documento")
        contrasena = request.form.get("contrasena")
        direccion = request.form.get("direccion")

        if not nombres or not apellidos or not email or not telefono or not documento or not contrasena or not direccion:
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for("usuario_bp.registrar"))

        try:
            controlador_usuarios.insertar_usuario(nombres, apellidos, email, telefono, documento, contrasena, direccion, 2)
            flash("Usuario registrado exitosamente", "success")
            return redirect(url_for("home"))
        except Exception as e:
            print(f"Error al registrar usuario: {str(e)}")
            print(traceback.format_exc())
            flash(f"Error al registrar usuario: {str(e)}", "error")
            return redirect(url_for("usuario_bp.registrar"))

    return render_template("registrate.html")


# Ruta para gestionar los usuarios en menuManUsuario.html
@usuario_bp.route("/menu_man_usuario", methods=["GET"])
def menu_man_usuario():
    usuarios = controlador_usuarios.obtener_todos_los_usuarios()
    return render_template("menuManUsuario.html", usuarios=usuarios)


# Ruta para agregar un usuario desde la parte del administrador
@usuario_bp.route("/agregar_usuario_administrador", methods=["POST"])
def agregar_usuario_administrador():
    try:
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        documento = request.form["documento"]
        direccion = request.form["direccion"]
        rol = request.form["rol"]

        controlador_usuarios.agregar_usuario(nombres, apellidos, email, telefono, documento, direccion, rol)
        flash("Usuario agregado correctamente", "success")
        return redirect(url_for('usuario_bp.menu_man_usuario'))
    except Exception as e:
        flash(f"Error al agregar usuario: {str(e)}", "error")
        return redirect(url_for('usuario_bp.menu_man_usuario'))


# Ruta para modificar un usuario desde la parte del administrador
@usuario_bp.route("/actualizar_usuario_administrador", methods=["POST"])
def actualizar_usuario_administrador():
    try:
        idUsuario = request.form["idUsuario"]
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        documento = request.form["documento"]
        direccion = request.form["direccion"]
        rol = request.form["rol"]

        controlador_usuarios.actualizar_usuario_administrador(nombres, apellidos, email, telefono, documento, direccion, rol, idUsuario)
        flash("Usuario actualizado correctamente", "success")
        return redirect(url_for('usuario_bp.menu_man_usuario'))
    except Exception as e:
        flash(f"Error al actualizar usuario: {str(e)}", "error")
        return redirect(url_for('usuario_bp.menu_man_usuario'))


# Ruta para eliminar un usuario desde el administrador
@usuario_bp.route("/eliminar_administrador/<int:idUsuario>", methods=["POST"])
def eliminar_administrador(idUsuario):
    try:
        controlador_usuarios.eliminar_usuario(idUsuario)
        flash("Usuario eliminado correctamente", "success")
        return redirect(url_for('usuario_bp.menu_man_usuario'))
    except Exception as e:
        flash(f"Error al eliminar usuario: {str(e)}", "error")
        return redirect(url_for('usuario_bp.menu_man_usuario'))


# ==========================
# INICIO DE APIS
# ==========================

# API para listar todos los usuarios en formato JSON
@usuario_bp.route("/api/listarUsuarios", methods=["GET"])
@jwt_required()
def listar_usuarios():
    try:
        usuarios = controlador_usuarios.obtener_usuarios()
        return jsonify({"data": usuarios, "message": "Usuarios obtenidos correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})


# API para listar un usuario por ID en formato JSON
@usuario_bp.route("/api/listarPorId/<int:idUsuario>", methods=["GET"])
@jwt_required()
def listar_usuario_por_id(idUsuario):
    try:
        usuario = controlador_usuarios.obtener_usuario_por_id(idUsuario)
        if usuario:
            # Convertir el objeto Usuario a un diccionario
            usuario_dict = {
                "id": usuario.id,
                "nombres": usuario.nombres,
                "apellidos": usuario.apellidos,
                "email": usuario.email,
                "telefono": usuario.telefono,
                "nroDocIde": usuario.nroDocIde,
                "direccion": usuario.direccion,
                "idRol": usuario.idRol,
            }
            return jsonify({"data": usuario_dict, "message": "Usuario obtenido correctamente", "status": 1})
        else:
            return jsonify({"data": [], "message": "Usuario no encontrado", "status": 0})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})


# API para eliminar un usuario
@usuario_bp.route("/api/eliminarUsuario/<int:idUsuario>", methods=["DELETE"])
@jwt_required()
def eliminar_usuario_api(idUsuario):
    try:
        controlador_usuarios.eliminar_usuario(idUsuario)
        return jsonify({"message": f"Usuario con ID {idUsuario} eliminado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})


# API para actualizar un usuario
@usuario_bp.route("/api/actualizarUsuario/<int:idUsuario>", methods=["PUT"])
@jwt_required()
def actualizar_usuario_ruta(idUsuario):
    try:
        data = request.json
        controlador_usuarios.actualizar_usuario(
            data["nombres"], data["apellidos"], data["email"],
            data["telefono"], data["nroDocIde"], data["contrasena"],
            data["direccion"], idUsuario
        )
        return jsonify({"message": "Usuario actualizado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})


# API para insertar usuario desde JSON
@usuario_bp.route("/api/insertarUsuario", methods=["POST"])
@jwt_required()
def insertar_usuario_desde_json():
    try:
        nombres = request.json["nombres"]
        apellidos = request.json["apellidos"]
        email = request.json["email"]
        telefono = request.json["telefono"]
        nroDocIde = request.json["nroDocIde"]
        contrasena = request.json["contrasena"]
        direccion = request.json["direccion"]
        controlador_usuarios.insertar_usuario(nombres, apellidos, email, telefono, nroDocIde, contrasena, direccion, 2)
        return jsonify({"data": [], "message": "Usuario registrado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})
