from flask_login import current_user
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
import controllers.controlador_tipopago as controlador_tipopago
from bd import obtener_conexion

tipopago_bp = Blueprint('tipopago_bp', __name__)

@tipopago_bp.route('/finalizar_compra', methods=["POST"])
def finalizar_compra():
    if not current_user.is_authenticated:
        return jsonify({"error": "Usuario no autenticado"}), 403

    id_usuario = current_user.id
    data = request.json
    id_tarjeta = data.get('idTarjeta')
    carrito = data.get('carrito')

    if not carrito or len(carrito) == 0:
        return jsonify({"error": "El carrito está vacío"}), 400

    conexion = obtener_conexion()
    try:
        conexion.begin()
        id_pedido = controlador_tipopago.crear_pedido(conexion, id_usuario)
        total_monto = sum(item['price'] * item['quantity'] for item in carrito)
        controlador_tipopago.registrar_pago(conexion, id_pedido, total_monto, id_tarjeta)
        controlador_tipopago.registrar_detalle_pedido(conexion, id_pedido, carrito)
        conexion.commit()

        return jsonify({"mensaje": "Compra finalizada exitosamente", "idPedido": id_pedido}), 200
    
    except Exception as e:
        conexion.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        conexion.close()

@tipopago_bp.route('/tipopago', methods=["GET"])
def mostrar_tipo_pago():
    return cargar_pagina_tipo_pago()

@tipopago_bp.route('/tarjetas', methods=["GET"])
def mostrar_tarjetas():
    return cargar_pagina_tipo_pago()

@tipopago_bp.route('/tarjetas/agregar', methods=['POST'])
def agregar_tarjeta_route():
    nombre = request.form.get('nombre')
    nro_tarjeta = request.form.get('nro_tarjeta')
    fecha = request.form.get('fecha')
    ccv = request.form.get('ccv')

    if not nombre or not nro_tarjeta or not fecha or not ccv:
        flash('Todos los campos son obligatorios', 'danger')
        return redirect(url_for('tipopago_bp.mostrar_tarjetas'))

    controlador_tipopago.agregar_tarjeta(nombre, nro_tarjeta, fecha, ccv, current_user.id)
    flash('Tarjeta agregada exitosamente', 'success')
    return redirect(url_for('tipopago_bp.mostrar_tipo_pago'))

def cargar_pagina_tipo_pago():
    if not current_user.is_authenticated:
        flash('Por favor inicia sesión para continuar.', 'error')
        return redirect(url_for('autenticacion_bp.login'))

    id_usuario = current_user.id
    tarjetas = controlador_tipopago.obtener_tarjetas(id_usuario)

    return render_template('tipopago.html', tarjetas=tarjetas)
