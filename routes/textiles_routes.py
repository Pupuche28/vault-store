from flask import Blueprint, render_template, request
from bd import obtener_conexion

# Crear el Blueprint para textiles
textiles_bp = Blueprint('textiles_bp', __name__)

@textiles_bp.route('/textiles', methods=['GET'])
def mostrar_textiles():
    # Obtener el valor del filtro de precio (si existe) con un valor predeterminado de 1000
    precio_max = request.args.get('precio', type=int, default=1000)
    
    # Obtener los productos de textiles filtrados por precio máximo
    productos_textiles = obtener_productos_textiles_filtrados(precio_max)
    
    # Renderizar la plantilla con los productos filtrados
    return render_template('textiles.html', productos=productos_textiles)

# Función para obtener productos de textiles filtrados por precio
def obtener_productos_textiles_filtrados(precio_max):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Consulta SQL para obtener productos de textiles con un precio <= precio_max y que tienen stock disponible
    query = '''
        SELECT idProducto, nombredeproducto, descripcion, precio, imagen 
        FROM PRODUCTO 
        WHERE idCategoria = 4 AND stock > 0 AND precio <= %s
    '''
    cursor.execute(query, (precio_max,))
    productos = cursor.fetchall()
    conexion.close()
    return productos
