from bd import obtener_conexion
from datetime import datetime
from decimal import Decimal

# Función para agregar tarjeta
def agregar_tarjeta(nombre, nro_tarjeta, fecha, ccv, id_usuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO TARJETA (nombre, nroTarjeta, fecha, ccv, idUsuario)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, nro_tarjeta, fecha, ccv, id_usuario))
    conexion.commit()
    conexion.close()

# Función para obtener tarjetas
def obtener_tarjetas(id_usuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        consulta = "SELECT idTarjeta, nombre, nroTarjeta, fecha FROM TARJETA WHERE idUsuario = %s"
        cursor.execute(consulta, (id_usuario,))
        tarjetas = cursor.fetchall()
    conexion.close()
    
    # Verificación temporal
    print(f"Tarjetas obtenidas para el usuario {id_usuario}: {tarjetas}")
    
    return tarjetas

# Función para crear un nuevo pedido
def crear_pedido(conexion, id_usuario):
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO PEDIDO (fechainicio, estado, idUsuario)
            VALUES (%s, %s, %s)
        """, (datetime.now(), 'Pendiente de Entrega', id_usuario))
        cursor.execute("SELECT LAST_INSERT_ID()")
        id_pedido = cursor.fetchone()[0]
    return id_pedido

# Función para registrar el pago
def registrar_pago(conexion, id_pedido, monto, id_tarjeta):
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO PAGO (fechapago, monto, metodopago, idPedido, idTarjeta)
            VALUES (%s, %s, %s, %s, %s)
        """, (datetime.now(), monto, 'Tarjeta de Débito', id_pedido, id_tarjeta))

# Función para registrar los detalles del pedido
def registrar_detalle_pedido(conexion, id_pedido, carrito):
    with conexion.cursor() as cursor:
        for item in carrito:
            nombre_producto = item['name']
            cantidad = item['quantity']
            cursor.execute("SELECT idProducto, precio, descuento, stock FROM PRODUCTO WHERE nombredeproducto = %s", (nombre_producto,))
            result = cursor.fetchone()
            if result:
                id_producto = result[0]
                precio = Decimal(result[1])
                descuento = Decimal(result[2])
                stock_actual = result[3]
                print(f"Producto encontrado: {nombre_producto}, Precio: {precio}, Descuento: {descuento}, Stock: {stock_actual}")
            else:
                raise Exception(f"No se encontró el producto con nombre: {nombre_producto}")

            if cantidad > stock_actual:
                raise Exception(f"No hay suficiente stock disponible para {nombre_producto}")

            igv = calcular_igv(precio * cantidad)
            subtotal = precio * cantidad
            total = subtotal

            cursor.execute("""
                INSERT INTO DETALLE_PEDIDO (idPedido, idProducto, cantidad, precio, descuento, igv, subtotal, total)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_pedido, id_producto, cantidad, precio, descuento, igv, subtotal, total))

            nuevo_stock = stock_actual - cantidad
            cursor.execute("""
                UPDATE PRODUCTO
                SET stock = %s
                WHERE idProducto = %s
            """, (nuevo_stock, id_producto))
            print(f"Stock actualizado para {nombre_producto}: {nuevo_stock} unidades restantes.")

# Función para calcular el IGV
def calcular_igv(subtotal, porcentaje=Decimal('0.18')):
    return subtotal * porcentaje
