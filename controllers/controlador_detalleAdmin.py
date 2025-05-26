from bd import obtener_conexion

# Obtener todos los detalles de los pedidos
def obtener_detalles_pedido():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT dp.idPedido, dp.idProducto, dp.cantidad, dp.precio, dp.descuento, dp.igv, dp.subtotal, dp.total, p.nombredeproducto
        FROM DETALLE_PEDIDO dp
        JOIN PRODUCTO p ON dp.idProducto = p.idProducto
    ''')
    detalles = cursor.fetchall()
    conexion.close()
    return detalles

# Obtener detalle de pedido por idPedido
def obtener_detalle_por_pedido(idPedido):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT dp.idPedido, dp.idProducto, dp.cantidad, dp.precio, dp.descuento, dp.igv, dp.subtotal, dp.total, p.nombredeproducto
        FROM DETALLE_PEDIDO dp
        JOIN PRODUCTO p ON dp.idProducto = p.idProducto
        WHERE dp.idPedido = %s
    ''', (idPedido,))
    detalles = cursor.fetchall()
    conexion.close()
    return detalles

# Insertar un detalle de pedido
def insertar_detalle_pedido(idPedido, idProducto, cantidad, precio, descuento, igv, subtotal, total):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO DETALLE_PEDIDO (idPedido, idProducto, cantidad, precio, descuento, igv, subtotal, total)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (idPedido, idProducto, cantidad, precio, descuento, igv, subtotal, total))
    conexion.commit()
    conexion.close()

# Actualizar un detalle de pedido
def actualizar_detalle_pedido(idPedido, idProducto, cantidad, precio, descuento, igv, subtotal, total):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        UPDATE DETALLE_PEDIDO
        SET cantidad = %s, precio = %s, descuento = %s, igv = %s, subtotal = %s, total = %s
        WHERE idPedido = %s AND idProducto = %s
    ''', (cantidad, precio, descuento, igv, subtotal, total, idPedido, idProducto))
    conexion.commit()
    conexion.close()

# Eliminar un detalle de pedido
def eliminar_detalle_pedido(idPedido, idProducto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM DETALLE_PEDIDO WHERE idPedido = %s AND idProducto = %s', (idPedido, idProducto))
    conexion.commit()
    conexion.close()
