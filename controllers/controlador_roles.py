from bd import obtener_conexion

# Función para obtener todos los roles
def obtener_roles():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT idRol, nombre FROM ROL")
            roles = cursor.fetchall()
        return roles
    except Exception as e:
        print(f"Error al obtener roles: {str(e)}")
        return []
    finally:
        conexion.close()

# Función para agregar un nuevo rol
def agregar_rol(nombre):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO ROL (nombre) VALUES (%s)", (nombre,))
        conexion.commit()
    except Exception as e:
        print(f"Error al agregar rol: {str(e)}")
    finally:
        conexion.close()

# Función para obtener un rol por ID
def obtener_rol_por_id(idRol):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT idRol, nombre FROM ROL WHERE idRol = %s", (idRol,))
            rol = cursor.fetchone()  # Usamos fetchone porque esperamos solo un resultado
        return rol
    except Exception as e:
        print(f"Error al obtener rol por ID: {str(e)}")
        return None
    finally:
        conexion.close()

# Función para actualizar un rol
def actualizar_rol(idRol, nombre):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE ROL SET nombre = %s WHERE idRol = %s", (nombre, idRol))
        conexion.commit()
    except Exception as e:
        print(f"Error al actualizar rol: {str(e)}")
    finally:
        conexion.close()

# Función para eliminar un rol
def eliminar_rol(idRol):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM ROL WHERE idRol = %s", (idRol,))
        conexion.commit()
    except Exception as e:
        print(f"Error al eliminar rol: {str(e)}")
    finally:
        conexion.close()
