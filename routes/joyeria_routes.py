from flask import Blueprint, render_template, request
from bd import obtener_conexion

# Crear el Blueprint para joyería
joyeria_bp = Blueprint('joyeria_bp', __name__)

@joyeria_bp.route('/joyeria', methods=['GET'])
def mostrar_joyeria():
    # Obtener el valor del filtro de precio (si existe) con un valor predeterminado de 1000
    precio_max = request.args.get('precio', type=int, default=1000)
    
    # Obtener los productos de joyería filtrados por precio máximo
    productos_joyeria = obtener_productos_joyeria_filtrados(precio_max)
    
    # Renderizar la plantilla con los productos filtrados
    return render_template('joyeria.html', productos=productos_joyeria)
# Función para obtener productos de joyería filtrados por precio
def obtener_productos_joyeria_filtrados(precio_max):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Consulta SQL para obtener productos de joyería con un precio <= precio_max y que tienen stock disponible
    query = '''
        SELECT idProducto, nombredeproducto, descripcion, precio, imagen 
        FROM PRODUCTO 
        WHERE idCategoria = 2 AND stock > 0 AND precio <= %s
    '''
    cursor.execute(query, (precio_max,))
    productos = cursor.fetchall()
    conexion.close()
    return productos
