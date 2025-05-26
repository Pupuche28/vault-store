from flask import render_template
from flask_login import current_user
from bd import obtener_conexion

# Función para cargar el tipo de entrega y la dirección del usuario
def cargar_tipo_entrega():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "SELECT direccion FROM USUARIO WHERE idUsuario = %s"
        cursor.execute(sql, (current_user.id,))  # Cambiar a current_user.id si idUsuario no existe
        resultado = cursor.fetchone()

    conexion.close()

    if resultado:
        usuario = {'direccion': resultado[0]}
    else:
        usuario = None

    return render_template("tipoentrega.html", usuario=usuario)

