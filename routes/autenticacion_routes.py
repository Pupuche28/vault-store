from flask import Blueprint, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
import controllers.controlador_autenticacion as controlador_autenticacion
import traceback

# Crear el blueprint para autenticación
autenticacion_bp = Blueprint('autenticacion_bp', __name__)

# Ruta para el inicio de sesión (solo maneja POST)
@autenticacion_bp.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    contrasena = request.form["contrasena"]

    print(f"Intento de inicio de sesión para el correo: {email}")  # Log para ver el correo en la terminal

    try:
        # Verificar las credenciales del usuario
        usuario = controlador_autenticacion.verificar_usuario(email, contrasena)

        if usuario:
            login_user(usuario)
            flash("Has iniciado sesión correctamente", "success")
            print(f"Usuario autenticado correctamente: {usuario.nombres} ({email})")  # Log de éxito en la terminal

            # Verificar si el usuario es Administrador basándonos en el idRol (1 = Administrador)
            if usuario.idRol == 1:
                print(f"Redirigiendo a la página de administración para el usuario: {usuario.nombres} ({email})")
                return redirect(url_for('admin_bp.menu_administrador'))  # Redirigir a 'menuAdministrador.html'

            # Si no es administrador (es cliente), redirigir al home o a la página solicitada
            next_page = request.args.get('next')
            return redirect(next_page or url_for("home"))
        else:
            flash("Correo o contraseña incorrectos", "error")
            print(f"Error: Credenciales incorrectas para {email}")  # Log de error en la terminal
            return redirect(url_for("home"))  # Redirige al home con mensaje de error
    except Exception as e:
        print(f"Error al intentar iniciar sesión para el correo {email}: {str(e)}")
        print(traceback.format_exc())  # Muestra el traceback completo del error en la terminal
        flash("Hubo un error en el sistema. Por favor, intenta nuevamente.", "error")
        return redirect(url_for("home"))

# Ruta para cerrar sesión
@autenticacion_bp.route("/logout")
@login_required
def logout():
    print(f"Usuario {current_user.email} ha cerrado sesión.")  # Log de éxito en la terminal
    logout_user()
    flash("Has cerrado sesión", "success")
    return redirect(url_for("home"))
