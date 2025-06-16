from flask import Blueprint, render_template, request
from bd import obtener_conexion

# Crear el Blueprint
ceramica_bp = Blueprint('ceramica_bp', __name__)

@ceramica_bp.route('/ceramica', methods=['GET'])
def mostrar_ceramica():
    # Obtener el valor del filtro de precio (si existe)
    precio_max = request.args.get('precio', type=int, default=1000)
    
    # Obtener los productos de cerámica filtrados por precio máximo
    productos_ceramica = obtener_productos_ceramica_filtrados(precio_max)
    
    # Renderizar la plantilla con los productos filtrados
    return render_template('ceramica.html', productos=productos_ceramica)

# Función para obtener productos de cerámica filtrados
def obtener_productos_ceramica_filtrados(precio_max):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Consulta SQL para obtener productos de cerámica con un precio <= precio_max y que tienen stock disponible
    query = '''
        SELECT idProducto, nombredeproducto, descripcion, precio, imagen 
        FROM PRODUCTO 
        WHERE idCategoria = 1 AND stock > 0 AND precio <= %s
    '''
    cursor.execute(query, (precio_max,))
    productos = cursor.fetchall()
    conexion.close()
    return productos
