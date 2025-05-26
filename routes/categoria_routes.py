from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import controllers.controlador_categorias as controlador_categorias  # Importa el controlador de categorías
import controllers.controlador_productos as controlador_productos  # Importa el controlador de productos

# Crear el Blueprint para categorías
categoria_bp = Blueprint('categoria_bp', __name__)

# ==========================
# Funcionalidades para la página
# ==========================

# Ruta para mostrar la página de gestión de categorías
@categoria_bp.route('/menu_man_categoria', methods=["GET"])
def menu_man_categoria():
    categorias = controlador_categorias.obtener_todas_categorias()  # Llama al controlador para obtener categorías
    return render_template('menuManCategoria.html', categorias=categorias)

# Ruta para agregar una nueva categoría
@categoria_bp.route('/agregar_categoria', methods=["POST"])
def agregar_categoria():
    nombre = request.form.get('nombre')
    if not nombre:
        flash("El nombre de la categoría es obligatorio", "error")
        return redirect(url_for('categoria_bp.menu_man_categoria'))

    controlador_categorias.agregar_categoria(nombre)  # Llama al controlador para agregar la categoría
    flash("Categoría agregada exitosamente", "success")
    return redirect(url_for('categoria_bp.menu_man_categoria'))

# Ruta para actualizar una categoría
@categoria_bp.route('/actualizar_categoria', methods=["POST"])
def actualizar_categoria():
    idCategoria = request.form.get('idCategoria')
    nombre = request.form.get('nombre')
    if not idCategoria or not nombre:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for('categoria_bp.menu_man_categoria'))

    controlador_categorias.actualizar_categoria(idCategoria, nombre)  # Llama al controlador para actualizar la categoría
    flash("Categoría actualizada exitosamente", "success")
    return redirect(url_for('categoria_bp.menu_man_categoria'))

# Ruta para eliminar una categoría desde el administrador
@categoria_bp.route("/eliminar_administrador/<int:idCategoria>", methods=["POST"])
def eliminar_categoria(idCategoria):
    try:
        # Eliminamos la categoría y la BD se encarga de eliminar los productos asociados (CASCADE)
        controlador_categorias.eliminar_categoria(idCategoria)
        flash("Categoría eliminada correctamente junto con sus productos asociados", "success")
    except Exception as e:
        flash(f"Error al eliminar la categoría: {str(e)}", "error")
    return redirect(url_for('categoria_bp.menu_man_categoria'))

# Ruta para verificar si una categoría tiene productos asociados
@categoria_bp.route('/verificar_productos/<int:idCategoria>', methods=['GET'])
def verificar_productos(idCategoria):
    try:
        # Verificamos si la categoría tiene productos asociados
        tiene_productos = controlador_productos.categoria_tiene_productos(idCategoria)
        return jsonify({"tiene_productos": tiene_productos})  # Retorna True o False
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================
# INICIO DE APIS
# ==========================

# API para listar todas las categorías en formato JSON
@categoria_bp.route("/api/listarCategorias", methods=["GET"])
def listar_categorias():
    try:
        categorias = controlador_categorias.obtener_todas_categorias()
        return jsonify({"data": categorias, "message": "Categorías obtenidas correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para listar una categoría por ID en formato JSON
@categoria_bp.route("/api/listarCategoriaPorId/<int:idCategoria>", methods=["GET"])
def listar_categoria_por_id(idCategoria):
    try:
        categoria = controlador_categorias.obtener_categoria_por_id(idCategoria)
        if categoria:
            return jsonify({"data": categoria, "message": "Categoría obtenida correctamente", "status": 1})
        else:
            return jsonify({"data": [], "message": "Categoría no encontrada", "status": 0})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para agregar una nueva categoría
@categoria_bp.route("/api/insertarCategoria", methods=["POST"])
def insertar_categoria():
    try:
        data = request.json
        nombre = data.get("nombre")
        if not nombre:
            return jsonify({"data": [], "message": "El nombre de la categoría es obligatorio", "status": -1})
        controlador_categorias.agregar_categoria(nombre)
        return jsonify({"message": "Categoría agregada correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})

# API para actualizar una categoría
@categoria_bp.route("/api/actualizarCategoria/<int:idCategoria>", methods=["PUT"])
def actualizar_categoria_api(idCategoria):
    try:
        data = request.json
        nombre = data.get("nombre")
        if not nombre:
            return jsonify({"data": [], "message": "El nombre de la categoría es obligatorio", "status": -1})
        controlador_categorias.actualizar_categoria(idCategoria, nombre)
        return jsonify({"message": "Categoría actualizada correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})

# API para eliminar una categoría
@categoria_bp.route("/api/eliminarCategoria/<int:idCategoria>", methods=["DELETE"])
def eliminar_categoria_api(idCategoria):
    try:
        controlador_categorias.eliminar_categoria(idCategoria)
        return jsonify({"message": f"Categoría con ID {idCategoria} eliminada correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})
