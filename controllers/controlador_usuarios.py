from bd import obtener_conexion
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import traceback  # Importar para manejo de errores
import hashlib

# Clase Usuario que extiende de UserMixin para trabajar con Flask-Login
class Usuario(UserMixin):
    def __init__(self, id, nombres, apellidos, email, telefono, nroDocIde, direccion, idRol, contrasena=None):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.email = email
        self.telefono = telefono
        self.nroDocIde = nroDocIde
        self.direccion = direccion
        self.idRol = idRol
        self.contrasena = contrasena  


# Función para poder hashear la contraseña
def hashear_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode('utf-8')).hexdigest()

# Función para insertar USUARIO
def insertar_usuario(nombres, apellidos, email, telefono, documento, contrasena, direccion, rol):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Hashear la contraseña con hashlib.sha256
            contrasena_hashed = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()
            sql = """
                INSERT INTO USUARIO (nombres, apellidos, email, telefono, nroDocIde, contrasena, direccion, idRol)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nombres, apellidos, email, telefono, documento, contrasena_hashed, direccion, rol))
        conexion.commit()
        print(f"Usuario {email} registrado correctamente con hash: {contrasena_hashed}")
    except Exception as e:
        print(f"Error al intentar registrar usuario {email}: {str(e)}")
        print(traceback.format_exc())
    finally:
        conexion.close()


# Función para actualizar usuario
def actualizar_usuario(nombres, apellidos, email, telefono, nroDocIde, contrasena, direccion, idUsuario):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Hashear la contraseña si se proporciona una nueva
            if contrasena:
                contrasena_hashed = generate_password_hash(contrasena)
                sql = """
                    UPDATE USUARIO 
                    SET nombres = %s, apellidos = %s, email = %s, telefono = %s, nroDocIde = %s, contrasena = %s, direccion = %s
                    WHERE idUsuario = %s
                """
                cursor.execute(sql, (nombres, apellidos, email, telefono, nroDocIde, contrasena_hashed, direccion, idUsuario))
            else:
                sql = """
                    UPDATE USUARIO 
                    SET nombres = %s, apellidos = %s, email = %s, telefono = %s, nroDocIde = %s, direccion = %s
                    WHERE idUsuario = %s
                """
                cursor.execute(sql, (nombres, apellidos, email, telefono, nroDocIde, direccion, idUsuario))
        conexion.commit()
        print(f"Usuario {email} actualizado correctamente.")  # Mensaje de éxito
    except Exception as e:
        print(f"Error al intentar actualizar usuario {email}: {str(e)}")
        print(traceback.format_exc())  # Muestra el traceback completo del error
    finally:
        conexion.close()

# Función para eliminar usuario
def eliminar_usuario(idUsuario):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM USUARIO WHERE idUsuario = %s", (idUsuario,))
        conexion.commit()
        print(f"Usuario {idUsuario} eliminado correctamente.")  # Mensaje de éxito
    except Exception as e:
        print(f"Error al intentar eliminar usuario {idUsuario}: {str(e)}")
        print(traceback.format_exc())  # Muestra el traceback completo del error
    finally:
        conexion.close()

# Función para OBTENER USUARIOS lista por: ID, NOMBRES, APELLIDOS, EMAIL, TELEFONO, NRODOCIDE, DIRECCION, ROL.
def obtener_usuarios():
    try:
        conexion = obtener_conexion()
        usuarios = []
        with conexion.cursor() as cursor:
            sql = """
                SELECT u.idUsuario, u.nombres, u.apellidos, u.email, u.telefono, 
                       u.nroDocIde, u.direccion, r.nombre AS rol, 
                       u.fechaCreacion, u.fechaModificacion
                FROM USUARIO u
                JOIN ROL r ON u.idRol = r.idRol
            """
            cursor.execute(sql)
            usuarios = cursor.fetchall()
        return usuarios
    except Exception as e:
        print(f"Error al intentar obtener usuarios: {str(e)}")
        print(traceback.format_exc())
        return []
    finally:
        conexion.close()

# Función para OBTENER USUARIOS por ID
# Esta función devuelve un objeto Usuario compatible con Flask-Login
def obtener_usuario_por_id(idUsuario):
    conexion = obtener_conexion()
    usuario = None
    try:
        with conexion.cursor() as cursor:
            sql = """
                SELECT u.idUsuario, u.nombres, u.apellidos, u.email, u.telefono, u.nroDocIde, u.direccion, u.idRol
                FROM USUARIO u
                WHERE u.idUsuario = %s
            """
            cursor.execute(sql, (idUsuario,))
            usuario_db = cursor.fetchone()

        # Verificar si se encontró el usuario y devolver un objeto de la clase Usuario
        if usuario_db:
            return Usuario(
                usuario_db[0],  # idUsuario
                usuario_db[1],  # nombres
                usuario_db[2],  # apellidos
                usuario_db[3],  # email
                usuario_db[4],  # telefono
                usuario_db[5],  # nroDocIde
                usuario_db[6],  # direccion
                usuario_db[7]   # idRol
            )
    except Exception as e:
        print(f"Error al intentar obtener usuario por ID: {str(e)}")
        print(traceback.format_exc())
    finally:
        conexion.close()

    return None

# Para obtener un listado de usuarios para listarlos en la parte de Administración USUARIO
def obtener_todos_los_usuarios():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = """
                SELECT idUsuario, nombres, apellidos, email, telefono, nroDocIde, 
                       direccion, idRol, fechaCreacion, fechaModificacion
                FROM USUARIO
            """
            cursor.execute(sql)
            usuarios = cursor.fetchall()
        return usuarios
    except Exception as e:
        print(f"Error al obtener usuarios: {str(e)}")
        return []
    finally:
        conexion.close()

# ELiminar USUARIO MODO ADMINISTRADOR
def eliminar_usuario(idUsuario):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "DELETE FROM USUARIO WHERE idUsuario = %s"
            cursor.execute(sql, (idUsuario,))
        conexion.commit()
        conexion.close()
        print(f"Usuario con ID {idUsuario} eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar usuario: {str(e)}")

# MODIFICAR USUARIO MODO ADMINISTRADOR
def actualizar_usuario_administrador(nombres, apellidos, email, telefono, documento, direccion, rol, idUsuario):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = """
            UPDATE USUARIO 
            SET nombres = %s, apellidos = %s, email = %s, telefono = %s, nroDocIde = %s, direccion = %s, idRol = %s
            WHERE idUsuario = %s
            """
            cursor.execute(sql, (nombres, apellidos, email, telefono, documento, direccion, rol, idUsuario))
        conexion.commit()
    except Exception as e:
        print(f"Error al actualizar usuario: {str(e)}")
    finally:
        conexion.close()

# AGREGAR USUARIO MODO ADMINISTRADOR
def agregar_usuario(nombres, apellidos, email, telefono, documento, direccion, rol):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = """
            INSERT INTO USUARIO (nombres, apellidos, email, telefono, nroDocIde, direccion, idRol)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nombres, apellidos, email, telefono, documento, direccion, rol))
        conexion.commit()
    except Exception as e:
        print(f"Error al agregar usuario: {str(e)}")
    finally:
        conexion.close()


# Función para obtener un usuario por su email
def obtener_usuario_por_email(email):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = """
                SELECT idUsuario, nombres, apellidos, email, telefono, nroDocIde, direccion, idRol, contrasena
                FROM USUARIO
                WHERE email = %s
            """
            cursor.execute(sql, (email,))
            usuario_db = cursor.fetchone()

        if usuario_db:
            # Devuelve el objeto Usuario con todos los atributos, incluida la contraseña
            return Usuario(
                usuario_db[0],  # idUsuario
                usuario_db[1],  # nombres
                usuario_db[2],  # apellidos
                usuario_db[3],  # email
                usuario_db[4],  # telefono
                usuario_db[5],  # nroDocIde
                usuario_db[6],  # direccion
                usuario_db[7],  # idRol
                usuario_db[8]   # contrasena
            )
    except Exception as e:
        print(f"Error al obtener usuario por email {email}: {str(e)}")
        print(traceback.format_exc())
    finally:
        conexion.close()

    return None
