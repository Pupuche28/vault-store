from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import controllers.controlador_resenas as controlador_resenas

from flask_jwt_extended import jwt_required, get_jwt_identity

# Crear el Blueprint para reseñas
resena_bp = Blueprint('resena_bp', __name__)

# Ruta para mostrar la página de gestión de reseñas
@resena_bp.route('/menu_man_resena', methods=["GET"])
def menu_man_resena():
    resenas = controlador_resenas.obtener_todas_resenas()
    usuarios = controlador_resenas.obtener_todos_usuarios()
    return render_template('menuManResena.html', resenas=resenas, usuarios=usuarios)

# Ruta para agregar una nueva reseña
@resena_bp.route('/agregar_resena', methods=["POST"])
def agregar_resena():
    descripcion = request.form.get('descripcion')
    idUsuario = request.form.get('idUsuario')
    
    if not descripcion or not idUsuario:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for('resena_bp.menu_man_resena'))

    try:
        controlador_resenas.agregar_resena(descripcion, idUsuario)
        flash("Reseña agregada exitosamente", "success")
    except Exception as e:
        flash(f"Error al agregar reseña: {str(e)}", "error")
    
    return redirect(url_for('resena_bp.menu_man_resena'))

# Ruta para actualizar una reseña
@resena_bp.route('/actualizar_resena', methods=["POST"])
def actualizar_resena():
    idResena = request.form.get('idResena')  # Asegúrate de recibir este ID
    descripcion = request.form.get('descripcion')
    idUsuario = request.form.get('idUsuario')  # Asegúrate de recibir el idUsuario
    
    if not idResena or not descripcion or not idUsuario:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for('resena_bp.menu_man_resena'))

    try:
        controlador_resenas.actualizar_resena(idResena, descripcion, idUsuario)  # Llamar con los tres parámetros
        flash("Reseña actualizada exitosamente", "success")
    except Exception as e:
        flash(f"Error al actualizar reseña: {str(e)}", "error")

    return redirect(url_for('resena_bp.menu_man_resena'))

# Ruta para eliminar una reseña
@resena_bp.route('/eliminar_resena/<int:idResena>', methods=["POST"])
def eliminar_resena(idResena):
    try:
        controlador_resenas.eliminar_resena(idResena)
        flash("Reseña eliminada exitosamente", "success")
    except Exception as e:
        flash(f"Error al eliminar reseña: {str(e)}", "error")
    
    return redirect(url_for('resena_bp.menu_man_resena'))


# ==========================
# INICIO DE APIS PARA RESEÑAS
# ==========================

# API para listar todas las reseñas en formato JSON
@resena_bp.route("/api/listarResenas", methods=["GET"])
@jwt_required()
def listar_resenas():
    try:
        resenas = controlador_resenas.obtener_todas_resenas()
        return jsonify({"data": resenas, "message": "Reseñas obtenidas correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para listar una reseña por ID en formato JSON
@resena_bp.route("/api/listarResenaPorId/<int:idResena>", methods=["GET"])
@jwt_required()
def listar_resena_por_id(idResena):
    try:
        resena = controlador_resenas.obtener_resena_por_id(idResena)
        if resena:
            # Acceder a los valores por índice
            resena_dict = {
                "id": resena[0],  # Ahora accedes al primer valor (idResena)
                "descripcion": resena[1],  # Descripción
                "idUsuario": resena[2],  # idUsuario
            }
            return jsonify({"data": resena_dict, "message": "Reseña obtenida correctamente", "status": 1})
        else:
            return jsonify({"data": [], "message": "Reseña no encontrada", "status": 0})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})


# API para eliminar una reseña
@resena_bp.route("/api/eliminarResena/<int:idResena>", methods=["DELETE"])
@jwt_required()
def eliminar_resena_api(idResena):
    try:
        controlador_resenas.eliminar_resena(idResena)
        return jsonify({"message": f"Reseña con ID {idResena} eliminada correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})

# API para actualizar una reseña
@resena_bp.route("/api/actualizarResena/<int:idResena>", methods=["PUT"])
@jwt_required()
def actualizar_resena_ruta(idResena):
    try:
        data = request.json
        controlador_resenas.actualizar_resena(
            idResena, data["descripcion"], data["idUsuario"]
        )
        return jsonify({"message": "Reseña actualizada correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})

# API para insertar reseña desde JSON
@resena_bp.route("/api/insertarResena", methods=["POST"])
@jwt_required()
def insertar_resena_desde_json():
    try:
        data = request.json
        descripcion = data["descripcion"]
        idUsuario = data["idUsuario"]  # El ID de usuario proviene de la solicitud
        
        # Validación de datos
        if not descripcion or not idUsuario:
            return jsonify({"data": [], "message": "Todos los campos son obligatorios", "status": 0})

        controlador_resenas.agregar_resena(descripcion, idUsuario)
        return jsonify({"data": [], "message": "Reseña registrada correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})
