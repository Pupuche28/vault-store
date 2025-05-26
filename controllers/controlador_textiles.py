from bd import obtener_conexion

# Controlador para obtener productos de textiles artesanales
def obtener_productos_textiles():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Consulta para obtener los productos de textiles con stock disponible
    cursor.execute('''
        SELECT idProducto, nombredeproducto, descripcion, precio, imagen 
        FROM PRODUCTO 
        WHERE idCategoria = 4 AND stock > 0
    ''')
    
    productos = cursor.fetchall()
    conexion.close()
    return productos
