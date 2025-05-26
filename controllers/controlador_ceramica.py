from bd import obtener_conexion

# controlador_productos.py o controlador_ceramica.py
def obtener_productos_ceramica():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Consulta para obtener los productos de cerámica con stock disponible
    cursor.execute('''
        SELECT idProducto, nombredeproducto, descripcion, precio, imagen 
        FROM PRODUCTO 
        WHERE idCategoria = 1 AND stock > 0
    ''')
    
    productos = cursor.fetchall()
    conexion.close()
    return productos

