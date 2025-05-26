class DetallePedido:
    def __init__(self, id_pedido, id_producto, cantidad, precio, descuento, igv, subtotal, total, fecha_creacion, fecha_modificacion):
        self.id_pedido = id_pedido
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio = precio
        self.descuento = descuento
        self.igv = igv
        self.subtotal = subtotal
        self.total = total
        self.fecha_creacion = fecha_creacion
        self.fecha_modificacion = fecha_modificacion

    def to_dict(self):
        return {
            "id_pedido": self.id_pedido,
            "id_producto": self.id_producto,
            "cantidad": self.cantidad,
            "precio": self.precio,
            "descuento": self.descuento,
            "igv": self.igv,
            "subtotal": self.subtotal,
            "total": self.total,
            "fecha_creacion": self.fecha_creacion,
            "fecha_modificacion": self.fecha_modificacion
        }
