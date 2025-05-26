from bd import obtener_conexion

# Obtener un pago por su ID
def obtener_pago_por_id(idPago):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM PAGO WHERE idPago = %s', (idPago,))
    pago = cursor.fetchone()
    conexion.close()
    return pago

# Actualizar un pago
def actualizar_pago(idPago, fechapago, monto, metodopago, idPedido, idTarjeta):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        UPDATE PAGO 
        SET fechapago = %s, monto = %s, metodopago = %s, idPedido = %s, idTarjeta = %s
        WHERE idPago = %s
    ''', (fechapago, monto, metodopago, idPedido, idTarjeta, idPago))
    conexion.commit()
    conexion.close()

# Insertar un pago
def insertar_pago(fechapago, monto, metodopago, idPedido, idTarjeta):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO PAGO (fechapago, monto, metodopago, idPedido, idTarjeta)
        VALUES (%s, %s, %s, %s, %s)
    ''', (fechapago, monto, metodopago, idPedido, idTarjeta))
    conexion.commit()
    conexion.close()


# Función para obtener todos los pagos
def obtener_pagos():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT P.idPago, P.fechapago, P.monto, P.metodopago, U.nombres AS usuario, T.nroTarjeta
                FROM PAGO P
                LEFT JOIN PEDIDO D ON P.idPedido = D.idPedido
                LEFT JOIN USUARIO U ON D.idUsuario = U.idUsuario
                LEFT JOIN TARJETA T ON P.idTarjeta = T.idTarjeta
            """)
            pagos = cursor.fetchall()
        return pagos
    except Exception as e:
        print(f"Error al obtener pagos: {str(e)}")
        return []
    finally:
        conexion.close()

# Función para eliminar un pago
def eliminar_pago(idPago):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM PAGO WHERE idPago = %s", (idPago,))
        conexion.commit()
    except Exception as e:
        print(f"Error al eliminar pago: {str(e)}")
    finally:
        conexion.close()
