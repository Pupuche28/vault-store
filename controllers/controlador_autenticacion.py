import hashlib
from bd import obtener_conexion
from flask_login import UserMixin
import traceback

# Clase Usuario que extiende de UserMixin para trabajar con Flask-Login
class Usuario(UserMixin):
    def __init__(self, idUsuario, nombres, apellidos, email, idRol):
        self.id = idUsuario  # Flask-Login usa 'id' por defecto
        self.nombres = nombres
        self.apellidos = apellidos
        self.email = email
        self.idRol = idRol

# Función para hashear contraseñas
def hashear_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode('utf-8')).hexdigest()

# Verificar usuario por email y contraseña
def verificar_usuario(email, contrasena):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Consulta para obtener el usuario desde la base de datos
            sql = "SELECT idUsuario, nombres, apellidos, email, contrasena, idRol FROM USUARIO WHERE email = %s"
            cursor.execute(sql, (email,))
            usuario_db = cursor.fetchone()
        conexion.close()

        # Verificar si el usuario fue encontrado
        if not usuario_db:
            print(f"Usuario no encontrado para el correo {email}")
            return None

        # Hashear la contraseña ingresada y compararla con la almacenada
        contrasena_hashed = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()
        print(f"Contraseña ingresada: {contrasena}")
        print(f"Hash calculado: {contrasena_hashed}")
        print(f"Hash almacenado: {usuario_db[4]}")

        if usuario_db[4] == contrasena_hashed:
            print(f"Usuario autenticado correctamente: {usuario_db[1]} {usuario_db[2]}")
            return Usuario(usuario_db[0], usuario_db[1], usuario_db[2], usuario_db[3], usuario_db[5])
        else:
            print(f"Contraseña incorrecta para el usuario {email}")
            return None
    except Exception as e:
        print(f"Error al autenticar usuario: {str(e)}")
        print(traceback.format_exc())
        return None
