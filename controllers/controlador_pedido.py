from bd import obtener_conexion

def obtener_todos_pedidos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT P.idPedido, P.fechainicio, P.fechafinalizado, P.estado, U.nombres, P.idUsuario,
               P.fechaCreacion, P.fechaModificacion
        FROM PEDIDO P
        JOIN USUARIO U ON P.idUsuario = U.idUsuario
        ORDER BY P.idPedido ASC
    """)
    pedidos = cursor.fetchall()
    conexion.close()
    print(f"Pedidos obtenidos: {pedidos}")
    return pedidos


def obtener_todos_usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT idUsuario, nombres FROM USUARIO")
    usuarios = cursor.fetchall()
    conexion.close()
    print(f"Usuarios obtenidos: {usuarios}")
    return usuarios

def obtener_pedido_por_id(idPedido):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM PEDIDO WHERE idPedido = %s", (idPedido,))
    pedido = cursor.fetchone()
    conexion.close()
    print(f"Pedido obtenido por ID {idPedido}: {pedido}")
    return pedido


def agregar_pedido(fechainicio, idUsuario, estado='Pendiente de Entrega'):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO PEDIDO (fechainicio, estado, idUsuario) VALUES (%s, %s, %s)", (fechainicio, estado, idUsuario))
    conexion.commit()
    if cursor.rowcount > 0:
        print(f"Pedido agregado: Fecha Inicio = {fechainicio}, Estado = {estado}, ID Usuario = {idUsuario}")
    else:
        print("Error: No se pudo agregar el pedido.")
    conexion.close()


def actualizar_pedido(idPedido, fechainicio, fechafinalizado, estado, idUsuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE PEDIDO 
        SET fechainicio = %s, fechafinalizado = %s, estado = %s, idUsuario = %s 
        WHERE idPedido = %s
    """, (fechainicio, fechafinalizado, estado, idUsuario, idPedido))
    conexion.commit()
    if cursor.rowcount > 0:
        print(f"Pedido actualizado: ID = {idPedido}, Nuevo Estado = {estado}")
    else:
        print(f"Error: No se pudo actualizar el pedido con ID {idPedido}.")
    conexion.close()


def eliminar_pedido(idPedido):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM PEDIDO WHERE idPedido = %s", (idPedido,))
    conexion.commit()
    if cursor.rowcount > 0:
        print(f"Pedido eliminado: ID = {idPedido}")
    else:
        print(f"Error: No se pudo eliminar el pedido con ID {idPedido}.")
    conexion.close()
