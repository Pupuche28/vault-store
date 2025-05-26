from bd import obtener_conexion

def obtener_pedidos_usuario(id_usuario):
    """
    Obtener los pedidos de un usuario dado su ID.
    """
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        # Obtenemos todos los pedidos y sus estados del usuario
        cursor.execute("""
            SELECT P.idPedido, P.fechainicio, P.fechafinalizado, P.estado, 
                   SUM(DP.cantidad * DP.precio) AS total
            FROM PEDIDO P
            LEFT JOIN DETALLE_PEDIDO DP ON P.idPedido = DP.idPedido
            WHERE P.idUsuario = %s
            GROUP BY P.idPedido
            ORDER BY P.fechainicio DESC
        """, (id_usuario,))
        pedidos = cursor.fetchall()
    conexion.close()
    return pedidos

def obtener_detalles_pedido(id_pedido):
    """
    Obtener los detalles de un pedido específico por su ID.
    """
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT DP.idProducto, DP.cantidad, DP.precio, DP.descuento, DP.igv, DP.subtotal, DP.total, 
                   PR.nombredeproducto
            FROM DETALLE_PEDIDO DP
            JOIN PRODUCTO PR ON DP.idProducto = PR.idProducto
            WHERE DP.idPedido = %s
        """, (id_pedido,))
        detalles = cursor.fetchall()
    conexion.close()
    return detalles
