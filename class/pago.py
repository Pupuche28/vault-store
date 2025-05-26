class clsPago:
    id_pago = 0
    fecha_pago = ""
    monto = 0.0
    metodo_pago = ""
    id_pedido = 0
    id_tarjeta = 0
    fecha_creacion = ""
    fecha_modificacion = ""
    dict_pago = dict()

    def __init__(self, id_pago, fecha_pago, monto, metodo_pago, id_pedido, id_tarjeta, fecha_creacion, fecha_modificacion):
        self.id_pago = id_pago
        self.fecha_pago = fecha_pago
        self.monto = monto
        self.metodo_pago = metodo_pago
        self.id_pedido = id_pedido
        self.id_tarjeta = id_tarjeta
        self.fecha_creacion = fecha_creacion
        self.fecha_modificacion = fecha_modificacion

        # Llenar el diccionario
        self.dict_pago["id_pago"] = id_pago
        self.dict_pago["fecha_pago"] = fecha_pago
        self.dict_pago["monto"] = monto
        self.dict_pago["metodo_pago"] = metodo_pago
        self.dict_pago["id_pedido"] = id_pedido
        self.dict_pago["id_tarjeta"] = id_tarjeta
        self.dict_pago["fecha_creacion"] = fecha_creacion
        self.dict_pago["fecha_modificacion"] = fecha_modificacion
