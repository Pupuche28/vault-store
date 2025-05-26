from bd import obtener_conexion

def obtener_todas_categorias():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT idCategoria, nombre, fechaCreacion, fechaModificacion FROM CATEGORIA")
    categorias = cursor.fetchall()
    conexion.close()
    return categorias


def obtener_categoria_por_id(idCategoria):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM CATEGORIA WHERE idCategoria = %s", (idCategoria,))
    categoria = cursor.fetchone()
    conexion.close()  # Cerrar la conexión después de la operación
    return categoria

def agregar_categoria(nombre):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO CATEGORIA (nombre) VALUES (%s)", (nombre,))
    conexion.commit()  # Guardar los cambios en la base de datos
    conexion.close()  # Cerrar la conexión

def actualizar_categoria(idCategoria, nombre):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("UPDATE CATEGORIA SET nombre = %s WHERE idCategoria = %s", (nombre, idCategoria))
    conexion.commit()  # Guardar los cambios en la base de datos
    conexion.close()  # Cerrar la conexión

def eliminar_categoria(idCategoria):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM CATEGORIA WHERE idCategoria = %s", (idCategoria,))
    conexion.commit()  # Guardar los cambios en la base de datos
    conexion.close()  # Cerrar la conexión
