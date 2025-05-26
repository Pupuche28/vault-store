from bd import obtener_conexion

# Obtener todos los productos
def obtener_todos_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT p.idProducto, p.nombredeproducto, p.autor, p.precio, p.descuento, p.stock, 
               p.nombredeTienda, p.descripcion, p.caracteristicas, c.nombre, p.imagen,
               p.fechaCreacion, p.fechaModificacion
        FROM PRODUCTO p 
        JOIN CATEGORIA c ON p.idCategoria = c.idCategoria
        ORDER BY p.idProducto ASC
    ''')
    productos = cursor.fetchall()
    conexion.close()
    return productos



# Obtener todas las categorías (para el dropdown de categorías)
def obtener_todas_categorias():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('SELECT idCategoria, nombre FROM CATEGORIA')
    categorias = cursor.fetchall()
    conexion.close()
    return categorias

# Registrar un nuevo producto
def agregar_producto(nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Insertar el nuevo producto junto con la imagen
    query = '''
    INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    
    cursor.execute(query, (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen))
    conexion.commit()
    conexion.close()

# Actualizar un producto existente
def actualizar_producto(idProducto, nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        UPDATE PRODUCTO 
        SET nombredeproducto = %s, autor = %s, precio = %s, descuento = %s, stock = %s, nombredeTienda = %s, 
            descripcion = %s, caracteristicas = %s, idCategoria = %s, imagen = %s
        WHERE idProducto = %s
    ''', (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen, idProducto))
    conexion.commit()
    conexion.close()

# Eliminar un producto
def eliminar_producto(idProducto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM PRODUCTO WHERE idProducto = %s', (idProducto,))
    conexion.commit()
    conexion.close()

# Obtener un producto por su ID
def obtener_producto_por_id(idProducto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM PRODUCTO WHERE idProducto = %s', (idProducto,))
    producto = cursor.fetchone()
    conexion.close()
    return producto

# Verificar si una categoría tiene productos asociados
def categoria_tiene_productos(idCategoria):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        # Consulta para verificar si hay productos asociados a la categoría
        query = "SELECT COUNT(*) FROM PRODUCTO WHERE idCategoria = %s"
        cursor.execute(query, (idCategoria,))
        resultado = cursor.fetchone()
        return resultado[0] > 0  # Retorna True si hay productos asociados
    except Exception as e:
        print(f"Error al verificar productos de la categoría {idCategoria}: {str(e)}")
        return False
    finally:
        conexion.close()
