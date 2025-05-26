from bd import obtener_conexion

def obtener_todas_resenas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT R.idResena, R.descripcion, U.nombres, R.idUsuario, R.fechaCreacion, R.fechaModificacion
        FROM RESENA R 
        JOIN USUARIO U ON R.idUsuario = U.idUsuario
        ORDER BY R.idResena ASC
    """)
    resenas = cursor.fetchall()
    conexion.close()
    return resenas


def obtener_resena_por_id(idResena):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM RESENA WHERE idResena = %s", (idResena,))
    resena = cursor.fetchone()
    conexion.close()
    print(f"Reseña obtenida por ID {idResena}: {resena}")
    return resena


def agregar_resena(descripcion, idUsuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO RESENA (descripcion, idUsuario) VALUES (%s, %s)", (descripcion, idUsuario))
    conexion.commit()
    if cursor.rowcount > 0:
        print(f"Reseña agregada: Descripción = {descripcion}, ID Usuario = {idUsuario}")
    else:
        print("Error: No se pudo agregar la reseña.")
    conexion.close()


def actualizar_resena(idResena, descripcion, idUsuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("UPDATE RESENA SET descripcion = %s, idUsuario = %s WHERE idResena = %s", 
                   (descripcion, idUsuario, idResena))
    conexion.commit()
    if cursor.rowcount > 0:
        print(f"Reseña actualizada: ID = {idResena}, Nueva Descripción = {descripcion}, Nuevo ID Usuario = {idUsuario}")
    else:
        print(f"Error: No se pudo actualizar la reseña con ID {idResena}.")
    conexion.close()


def eliminar_resena(idResena):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM RESENA WHERE idResena = %s", (idResena,))
    conexion.commit()
    if cursor.rowcount > 0:
        print(f"Reseña eliminada: ID = {idResena}")
    else:
        print(f"Error: No se pudo eliminar la reseña con ID {idResena}.")
    conexion.close()


def obtener_todos_usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT idUsuario, nombres FROM USUARIO")
    usuarios = cursor.fetchall()
    conexion.close()
    print(f"Usuarios obtenidos: {usuarios}")
    return usuarios


# Función para verificar si el usuario tiene reseñas
def usuario_tiene_resenas(id_usuario):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM RESENA WHERE idUsuario = %s"
            cursor.execute(sql, (id_usuario,))
            resultado = cursor.fetchone()
            return resultado[0] > 0  # Retorna True si tiene reseñas activas
    except Exception as e:
        print(f"Error al verificar reseñas del usuario {id_usuario}: {str(e)}")
        return False
