from functools import wraps
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_required, current_user
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from routes.usuario_routes import usuario_bp
from routes.autenticacion_routes import autenticacion_bp
from routes.admin_routes import admin_bp
from routes.rol_routes import rol_bp
from routes.resenas_routes import resena_bp
from routes.categoria_routes import categoria_bp
from routes.producto_routes import producto_bp
from routes.ceramica_routes import ceramica_bp
from routes.joyeria_routes import joyeria_bp
from routes.retablos_routes import retablos_bp
from routes.textiles_routes import textiles_bp
from routes.detalleproducto_routes import detalle_producto_bp
from routes.carrito_routes import carrito_bp
from routes.tipoentrega_routes import tipo_entrega_bp
from routes.tipopago_routes import tipopago_bp
from routes.mispedidos_routes import mispedidos_bp
from routes.tarjetasAdmin_routes import tarjetaAdmin_bp
from routes.pedido_routes import pedido_bp
from routes.pago_routes import pago_bp
from routes.detalleAdmin_routes import detalleAdmin_bp
from routes.archivos_routes import archivos_bp

from controllers.controlador_ceramica import obtener_productos_ceramica
import controllers.controlador_tipoentrega as controlador_tipoentrega
from controllers.controlador_detalleproducto import obtener_producto_por_id
import controllers.controlador_resenas as controlador_resenas
import controllers.controlador_usuarios as controlador_usuarios
import hashlib
from controllers.controlador_usuarios import obtener_usuario_por_email
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Agregar una clave secreta para las sesiones
app.secret_key = 'rodrigho'

# Configuración para Flask-JWT-Extended
app.config['JWT_SECRET_KEY'] = 'mi_clave_secreta_super_segura'
jwt = JWTManager(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'autenticacion_bp.login'

# Función para cargar usuario desde el ID de sesión
@login_manager.user_loader
def load_user(user_id):
    return controlador_usuarios.obtener_usuario_por_id(user_id)

# Context processor: Hacer disponible `current_user` en todas las plantillas
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# Registrar los blueprints
app.register_blueprint(usuario_bp, url_prefix="/usuario")
app.register_blueprint(autenticacion_bp, url_prefix="/auth")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(rol_bp, url_prefix="/rol")
app.register_blueprint(categoria_bp, url_prefix="/categoria")
app.register_blueprint(resena_bp, url_prefix="/resena")
app.register_blueprint(producto_bp, url_prefix='/producto')
app.register_blueprint(ceramica_bp)
app.register_blueprint(joyeria_bp)
app.register_blueprint(retablos_bp)
app.register_blueprint(textiles_bp)
app.register_blueprint(detalle_producto_bp)
app.register_blueprint(carrito_bp, url_prefix='/carrito')
app.register_blueprint(tipo_entrega_bp)
app.register_blueprint(tipopago_bp)
app.register_blueprint(mispedidos_bp)
app.register_blueprint(tarjetaAdmin_bp, url_prefix='/tarjetasAdmin')
app.register_blueprint(pedido_bp, url_prefix='/pedidos')
app.register_blueprint(pago_bp, url_prefix='/pago')
app.register_blueprint(detalleAdmin_bp, url_prefix='/detallePedido')
app.register_blueprint(archivos_bp, url_prefix='/archivos')

# Decorador para verificar que el usuario es administrador
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.idRol == 1:  # 1 es el idRol para "administrador"
            return f(*args, **kwargs)
        else:
            flash("Acceso denegado. Solo los administradores pueden acceder a esta página.", "danger")
            return redirect(url_for("home"))
    return decorated_function

# Rutas para el home
@app.route("/")
def home():
    if current_user.is_authenticated:
        if current_user.idRol == 1:
            return render_template("menuAdministrador.html")
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")

# Rutas protegidas para administradores
@app.route("/admin")
@admin_required
def admin_home():
    return render_template("menuAdministrador.html")

@app.route("/producto/menu_man_producto")
@admin_required
def menu_man_producto():
    return render_template("menu_man_producto.html")

@app.route("/usuario/menu_man_usuario")
@admin_required
def menu_man_usuario():
    return render_template("menu_man_usuario.html")

@app.route("/rol/menu_man_rol")
@admin_required
def menu_man_rol():
    return render_template("menu_man_rol.html")

@app.route("/categoria/menu_man_categoria")
@admin_required
def menu_man_categoria():
    return render_template("menu_man_categoria.html")

@app.route("/resena/menu_man_resena")
@admin_required
def menu_man_resena():
    return render_template("menu_man_resena.html")

@app.route("/tarjetasAdmin/menu_man_tarjeta")
@admin_required
def menu_man_tarjeta():
    return render_template("menu_man_tarjeta.html")

@app.route("/pedidos/menu_man_pedido")
@admin_required
def menu_man_pedido():
    return render_template("menu_man_pedido.html")

@app.route("/pago/menu_man_pago")
@admin_required
def menu_man_pago():
    return render_template("menu_man_pago.html")

@app.route("/admin/menu_administrador")
@admin_required
def menu_administrador():
    return render_template("menu_administrador.html")


# Ruta para el login y la autenticación
@app.route('/obtener_tokem', methods=['POST'])
def login():
    try:
        email = request.json.get('email', None)
        contrasena = request.json.get('contrasena', None)

        if not email or not contrasena:
            return jsonify({"message": "Correo y contraseña son obligatorios"}), 400

        usuario = obtener_usuario_por_email(email)
        if usuario:
            if usuario.idRol != 1:
                return jsonify({"message": "Acceso denegado. Solo los administradores pueden generar tokens."}), 403

            contrasena_hashed = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()
            if usuario.contrasena == contrasena_hashed:
                access_token = create_access_token(identity=str(usuario.id))
                return jsonify({"token": access_token, "usuario": {"id": usuario.id, "nombres": usuario.nombres}}), 200
            else:
                return jsonify({"message": "Contraseña incorrecta"}), 401
        else:
            return jsonify({"message": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"message": "Error interno del servidor", "error": str(e)}), 500

# Rutas protegidas con autenticación
@app.route("/cambios")
def cambios():
    return render_template("cambios.html")

@app.route("/carrito")
@login_required
def carrito():
    return render_template("carrito.html")

@app.route('/ceramica')
def ceramica():
    productos_ceramica = obtener_productos_ceramica()
    return render_template('ceramica.html', productos=productos_ceramica)

@app.route("/contactos")
def contactos():
    return render_template("contactos.html")

@app.route("/joyeria")
def joyeria():
    return render_template("joyeria.html")

@app.route("/legales")
def legales():
    return render_template("legales.html")

@app.route("/nosotros")
def nosotros():
    resenas = controlador_resenas.obtener_todas_resenas()
    return render_template("nosotros.html", resenas=resenas)

@app.route("/politicas")
def politicas():
    return render_template("politicas.html")

@app.route("/preguntas")
def preguntas():
    return render_template("preguntas.html")

@app.route('/producto/<int:id_producto>')
def productodetalle(id_producto):
    producto = obtener_producto_por_id(id_producto)
    if producto:
        return render_template('productodetalle.html', producto=producto)
    else:
        return "Producto no encontrado", 404

@app.route("/registrate")
def registrate():
    return render_template("registrate.html")

@app.route("/retablos")
def retablos():
    return render_template("retablos.html")

@app.route("/terminos")
def terminos():
    return render_template("terminos.html")

@app.route("/textiles")
def textiles():
    return render_template("textiles.html")

@app.route("/subir-archivo")
@login_required
def subir_archivo():
    return render_template("subir_archivo.html")

@app.route("/tipoentrega")
@login_required
def tipoentrega():
    direccion = controlador_tipoentrega.obtener_direccion_usuario(current_user.id)
    return render_template("tipoentrega.html", direccion=direccion)

@app.route("/tipopago")
def tipopago():
    return render_template("tipopago.html")

@app.route("/poncho-personalizado")
def poncho_personalizado():
    return render_template("poncho_personalizado.html")

# Manejar el caso de rutas no autorizadas
@login_manager.unauthorized_handler
def unauthorized():
    flash("Debes iniciar sesión para acceder a esta página.", "warning")
    return redirect(url_for("home"))

UPLOAD_FOLDER = os.path.join('static', 'img', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload_personalizacion', methods=['POST'])
def upload_personalizacion():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Si ya existe, renombrar
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(save_path):
            filename = f"{base}_{counter}{ext}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            counter += 1
        file.save(save_path)
        url = f"/static/img/uploads/{filename}"
        return jsonify({'url': url}), 200
    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
