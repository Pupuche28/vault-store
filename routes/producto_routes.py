import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import controllers.controlador_productos as controlador_productos

from flask_jwt_extended import jwt_required, get_jwt_identity

# Crear el Blueprint para productos
producto_bp = Blueprint('producto_bp', __name__)

# Directorio donde se guardarán las imágenes
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'webp'}

# Configurar el directorio de subida de archivos
producto_bp.config = {}
producto_bp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Verificar si la carpeta existe, y si no, crearla
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta para mostrar la página de gestión de productos
@producto_bp.route('/menu_man_producto', methods=["GET"])
def menu_man_producto():
    productos = controlador_productos.obtener_todos_productos()
    categorias = controlador_productos.obtener_todas_categorias()
    return render_template('menuManProducto.html', productos=productos, categorias=categorias)

# Ruta para agregar un nuevo producto con imagen
@producto_bp.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    nombredeproducto = request.form['nombredeproducto']
    autor = request.form.get('autor')
    precio = request.form['precio']
    descuento = request.form.get('descuento')
    stock = request.form['stock']
    nombredeTienda = request.form['nombredeTienda']
    descripcion = request.form['descripcion']
    caracteristicas = request.form['caracteristicas']
    idCategoria = request.form['idCategoria']
    
    # Manejo de la imagen
    if 'imagen' not in request.files:
        flash('No se subió ningún archivo', 'error')
        return redirect(request.url)
    
    file = request.files['imagen']
    
    if file and allowed_file(file.filename):
        # Asegurarse de que el nombre del archivo es seguro
        filename = secure_filename(file.filename)
        
        # Guardar la imagen en la carpeta de uploads (static/img)
        file.save(os.path.join(producto_bp.config['UPLOAD_FOLDER'], filename))
        
        # Registrar el producto en la base de datos, almacenando la ruta de la imagen
        controlador_productos.agregar_producto(
            nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, filename
        )
        
        flash('Producto registrado exitosamente', 'success')
        return redirect(url_for('producto_bp.menu_man_producto'))
    else:
        flash('Formato de archivo no permitido. Solo se permiten archivos .webp', 'error')
        return redirect(request.url)

# Ruta para actualizar un producto
@producto_bp.route('/actualizar_producto', methods=["POST"])
def actualizar_producto():
    idProducto = request.form.get('idProducto')
    nombredeproducto = request.form.get('nombredeproducto')
    autor = request.form.get('autor')
    precio = request.form.get('precio')
    descuento = request.form.get('descuento')
    stock = request.form.get('stock')
    nombredeTienda = request.form.get('nombredeTienda')
    descripcion = request.form.get('descripcion')
    caracteristicas = request.form.get('caracteristicas')
    idCategoria = request.form.get('idCategoria')

    # Obtener la imagen actual del producto
    producto = controlador_productos.obtener_producto_por_id(idProducto)
    imagen_actual = producto[10]  # El índice correcto para la imagen en la tupla

    # Manejo de la nueva imagen (si se subió una nueva)
    if 'imagen' in request.files:
        file = request.files['imagen']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(producto_bp.config['UPLOAD_FOLDER'], filename))
        else:
            filename = imagen_actual  # Mantener la imagen actual si no se subió una nueva imagen
    else:
        filename = imagen_actual

    try:
        controlador_productos.actualizar_producto(idProducto, nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, filename)
        flash("Producto actualizado exitosamente", "success")
    except Exception as e:
        flash(f"Error al actualizar producto: {str(e)}", "error")

    return redirect(url_for('producto_bp.menu_man_producto'))


# Ruta para eliminar un producto
@producto_bp.route('/eliminar_producto/<int:idProducto>', methods=["POST"])
def eliminar_producto(idProducto):
    try:
        controlador_productos.eliminar_producto(idProducto)
        flash("Producto eliminado exitosamente", "success")
    except Exception as e:
        flash(f"Error al eliminar producto: {str(e)}", "error")
    
    return redirect(url_for('producto_bp.menu_man_producto'))


# ==========================
# INICIO DE APIS PARA PRODUCTOS
# ==========================

# API para listar todos los productos
@producto_bp.route("/api/listarProductos", methods=["GET"])
@jwt_required()
def listar_productos():
    try:
        productos = controlador_productos.obtener_todos_productos()
        return jsonify({"data": productos, "message": "Productos obtenidos correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para listar un producto por ID
@producto_bp.route("/api/listarProductoPorId/<int:idProducto>", methods=["GET"])
@jwt_required()
def listar_producto_por_id(idProducto):
    try:
        producto = controlador_productos.obtener_producto_por_id(idProducto)
        if producto:
            # Convertir los valores a un diccionario
            producto_dict = {
                "idProducto": producto[0],
                "nombredeproducto": producto[1],
                "autor": producto[2],
                "precio": producto[3],
                "descuento": producto[4],
                "stock": producto[5],
                "nombredeTienda": producto[6],
                "descripcion": producto[7],
                "caracteristicas": producto[8],
                "idCategoria": producto[9],
                "imagen": producto[10],
                "fechaCreacion": producto[11],
                "fechaModificacion": producto[12]
            }
            return jsonify({"data": producto_dict, "message": "Producto obtenido correctamente", "status": 1})
        else:
            return jsonify({"data": [], "message": "Producto no encontrado", "status": 0})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para insertar un nuevo producto desde JSON
@producto_bp.route("/api/insertarProducto", methods=["POST"])
@jwt_required()
def insertar_producto_desde_json():
    try:
        data = request.json
        nombredeproducto = data["nombredeproducto"]
        autor = data["autor"]
        precio = data["precio"]
        descuento = data["descuento"]
        stock = data["stock"]
        nombredeTienda = data["nombredeTienda"]
        descripcion = data["descripcion"]
        caracteristicas = data["caracteristicas"]
        idCategoria = data["idCategoria"]
        imagen = data["imagen"]
        
        # Validación de datos
        if not nombredeproducto or not autor or not precio or not stock or not nombredeTienda:
            return jsonify({"data": [], "message": "Todos los campos son obligatorios", "status": 0})

        controlador_productos.agregar_producto(nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
        return jsonify({"data": [], "message": "Producto registrado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})
    

# API para actualizar un producto
@producto_bp.route("/api/actualizarProducto/<int:idProducto>", methods=["PUT"])
@jwt_required()
def actualizar_producto_ruta(idProducto):
    try:
        data = request.json
        controlador_productos.actualizar_producto(
            idProducto, data["nombredeproducto"], data["autor"], data["precio"], data["descuento"], 
            data["stock"], data["nombredeTienda"], data["descripcion"], data["caracteristicas"], 
            data["idCategoria"], data["imagen"]
        )
        return jsonify({"message": "Producto actualizado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})


# API para eliminar un producto
@producto_bp.route("/api/eliminarProducto/<int:idProducto>", methods=["DELETE"])
@jwt_required()
def eliminar_producto_api(idProducto):
    try:
        controlador_productos.eliminar_producto(idProducto)
        return jsonify({"message": f"Producto con ID {idProducto} eliminado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})
