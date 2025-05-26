from bd import obtener_conexion

# Controlador para obtener productos de joyería artesanal
def obtener_productos_joyeria():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Consulta para obtener los productos de joyería con stock disponible
    cursor.execute('''
        SELECT idProducto, nombredeproducto, descripcion, precio, imagen 
        FROM PRODUCTO 
        WHERE idCategoria = 2 AND stock > 0
    ''')
    
    productos = cursor.fetchall()
    conexion.close()
    return productos

