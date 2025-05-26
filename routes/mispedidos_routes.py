from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
import controllers.controlador_mispedidos as controlador_mispedidos

mispedidos_bp = Blueprint('mispedidos_bp', __name__)

# Ruta para ver los pedidos del usuario
@mispedidos_bp.route('/mispedidos')
@login_required
def mis_pedidos():
    # Obtener los pedidos del usuario actual
    pedidos = controlador_mispedidos.obtener_pedidos_usuario(current_user.id)
    return render_template('mispedidos.html', pedidos=pedidos)

# Ruta para ver los detalles de un pedido específico
@mispedidos_bp.route('/mispedidos/detalle/<int:id_pedido>')
@login_required
def detalle_pedido(id_pedido):
    # Verificar que el pedido pertenece al usuario actual
    detalles = controlador_mispedidos.obtener_detalles_pedido(id_pedido)
    if not detalles:
        flash('No tienes permiso para ver este pedido o el pedido no existe.', 'danger')
        return redirect(url_for('mispedidos_bp.mis_pedidos'))
    return render_template('detalle_pedido.html', detalles=detalles, id_pedido=id_pedido)
