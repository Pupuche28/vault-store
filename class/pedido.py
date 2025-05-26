class clsPedido:
    id_pedido = 0
    fecha_inicio = ""
    fecha_finalizado = ""
    estado = ""
    id_usuario = 0
    fecha_creacion = ""
    fecha_modificacion = ""
    dict_pedido = dict()

    def __init__(self, id_pedido, fecha_inicio, fecha_finalizado, estado, id_usuario, fecha_creacion, fecha_modificacion):
        self.id_pedido = id_pedido
        self.fecha_inicio = fecha_inicio
        self.fecha_finalizado = fecha_finalizado
        self.estado = estado
        self.id_usuario = id_usuario
        self.fecha_creacion = fecha_creacion
        self.fecha_modificacion = fecha_modificacion

        # Llenar el diccionario
        self.dict_pedido["id_pedido"] = id_pedido
        self.dict_pedido["fecha_inicio"] = fecha_inicio
        self.dict_pedido["fecha_finalizado"] = fecha_finalizado
        self.dict_pedido["estado"] = estado
        self.dict_pedido["id_usuario"] = id_usuario
        self.dict_pedido["fecha_creacion"] = fecha_creacion
        self.dict_pedido["fecha_modificacion"] = fecha_modificacion
