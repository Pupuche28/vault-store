class clsTarjeta:
    id_tarjeta = 0
    nombre = ""
    nro_tarjeta = ""
    fecha = ""
    ccv = ""
    id_usuario = 0
    fecha_creacion = ""
    fecha_modificacion = ""
    dict_tarjeta = dict()

    def __init__(self, id_tarjeta, nombre, nro_tarjeta, fecha, ccv, id_usuario, fecha_creacion, fecha_modificacion):
        self.id_tarjeta = id_tarjeta
        self.nombre = nombre
        self.nro_tarjeta = nro_tarjeta
        self.fecha = fecha
        self.ccv = ccv
        self.id_usuario = id_usuario
        self.fecha_creacion = fecha_creacion
        self.fecha_modificacion = fecha_modificacion

        # Llenar el diccionario
        self.dict_tarjeta["id_tarjeta"] = id_tarjeta
        self.dict_tarjeta["nombre"] = nombre
        self.dict_tarjeta["nro_tarjeta"] = nro_tarjeta
        self.dict_tarjeta["fecha"] = fecha
        self.dict_tarjeta["ccv"] = ccv
        self.dict_tarjeta["id_usuario"] = id_usuario
        self.dict_tarjeta["fecha_creacion"] = fecha_creacion
        self.dict_tarjeta["fecha_modificacion"] = fecha_modificacion
