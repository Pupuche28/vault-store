from flask import Blueprint, render_template, request
from bd import obtener_conexion

# Crear el Blueprint para retablos
retablos_bp = Blueprint('retablos_bp', __name__)

@retablos_bp.route('/retablos', methods=['GET'])
def mostrar_retablos():
    # Obtener el valor del filtro de precio (si existe) con un valor predeterminado de 1000
    precio_max = request.args.get('precio', type=int, default=1000)
    
    # Obtener los productos de retablos filtrados por precio máximo
    productos_retablos = obtener_productos_retablos_filtrados(precio_max)
    
    # Renderizar la plantilla con los productos filtrados
    return render_template('retablos.html', productos=productos_retablos)

# Función para obtener productos de retablos filtrados por precio
def obtener_productos_retablos_filtrados(precio_max):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Consulta SQL para obtener productos de retablos con un precio <= precio_max y que tienen stock disponible
    query = '''
        SELECT idProducto, nombredeproducto, descripcion, precio, imagen 
        FROM PRODUCTO 
        WHERE idCategoria = 3 AND stock > 0 AND precio <= %s
    '''
    cursor.execute(query, (precio_max,))
    productos = cursor.fetchall()
    conexion.close()
    return productos
