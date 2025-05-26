from bd import obtener_conexion

# Controlador para obtener productos de retablos artesanales
def obtener_productos_retablos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Consulta para obtener los productos de retablos con stock disponible
    cursor.execute('''
        SELECT idProducto, nombredeproducto, descripcion, precio, imagen 
        FROM PRODUCTO 
        WHERE idCategoria = 3 AND stock > 0
    ''')
    
    productos = cursor.fetchall()
    conexion.close()
    return productos
