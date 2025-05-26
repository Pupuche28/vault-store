import hashlib
from bd import obtener_conexion

def rehash_contrasenas():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Seleccionar todas las contraseñas de los usuarios
            cursor.execute("SELECT idUsuario, contrasena FROM USUARIO")
            usuarios = cursor.fetchall()

            for usuario in usuarios:
                idUsuario = usuario[0]
                contrasena_actual = usuario[1]

                # Verificar si la contraseña ya está hasheada con sha256 (longitud fija de 64 caracteres)
                if len(contrasena_actual) != 64 or not contrasena_actual.isalnum():
                    # Rehash la contraseña actual con hashlib.sha256
                    nueva_contrasena = hashlib.sha256(contrasena_actual.encode('utf-8')).hexdigest()
                    cursor.execute(
                        "UPDATE USUARIO SET contrasena = %s WHERE idUsuario = %s",
                        (nueva_contrasena, idUsuario)
                    )
                    print(f"Contraseña actualizada para el usuario ID {idUsuario}")
            
            conexion.commit()
            print("Rehash completado para todas las contraseñas.")
    except Exception as e:
        print(f"Error al rehashear contraseñas: {str(e)}")
    finally:
        conexion.close()

if __name__ == "__main__":
    rehash_contrasenas()
