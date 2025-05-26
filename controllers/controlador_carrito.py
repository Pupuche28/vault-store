from flask import session
from bd import obtener_conexion

def agregar_al_carrito(producto_id, cantidad):
    # Conectar a la base de datos para obtener la información del producto
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idProducto, nombredeproducto, precio, imagen FROM PRODUCTO WHERE idProducto = %s", (producto_id,))
        producto = cursor.fetchone()

    if not producto:
        raise Exception("Producto no encontrado")

    # Obtener el carrito de la sesión
    carrito = session.get('carrito', [])

    # Verificar si el producto ya está en el carrito
    for item in carrito:
        if item['idProducto'] == producto_id:
            item['cantidad'] += cantidad
            break
    else:
        # Si no está en el carrito, lo agregamos
        carrito.append({
            'idProducto': producto['idProducto'],
            'nombredeproducto': producto['nombredeproducto'],
            'precio': producto['precio'],
            'cantidad': cantidad,
            'imagen': producto['imagen']
        })

    # Guardar el carrito actualizado en la sesión
    session['carrito'] = carrito

def obtener_carrito():
    return session.get('carrito', [])

def eliminar_del_carrito(producto_id):
    carrito = session.get('carrito', [])
    carrito = [item for item in carrito if item['idProducto'] != producto_id]
    session['carrito'] = carrito
