from bd import obtener_conexion  # Función que devuelve la conexión a la base de datos

def obtener_producto_por_id(id_producto):
    connection = obtener_conexion()
    with connection.cursor() as cursor:
        sql = """
        SELECT p.idProducto, p.nombredeproducto, p.autor, p.precio, p.descuento, p.stock, p.nombredeTienda, p.descripcion, 
               p.caracteristicas, p.imagen, c.nombre AS categoria
        FROM PRODUCTO p
        JOIN CATEGORIA c ON p.idCategoria = c.idCategoria
        WHERE p.idProducto = %s
        """
        cursor.execute(sql, (id_producto,))
        row = cursor.fetchone()
    
    connection.close()
    
    if row:
        # Convertir la tupla a un diccionario
        producto = {
            'idProducto': row[0],
            'nombredeproducto': row[1],
            'autor': row[2],
            'precio': row[3],
            'descuento': row[4],
            'stock': row[5],
            'nombredeTienda': row[6],
            'descripcion': row[7],
            'caracteristicas': row[8],
            'imagen': row[9],
            'categoria': row[10]  # Agregamos la categoría
        }
        return producto
    else:
        return None


