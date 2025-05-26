class clsResena:
    id_resena = 0
    descripcion = ""
    id_usuario = 0
    fecha_creacion = ""
    fecha_modificacion = ""
    dict_resena = dict()

    def __init__(self, id_resena, descripcion, id_usuario, fecha_creacion, fecha_modificacion):
        self.id_resena = id_resena
        self.descripcion = descripcion
        self.id_usuario = id_usuario
        self.fecha_creacion = fecha_creacion
        self.fecha_modificacion = fecha_modificacion

        # Llenar el diccionario
        self.dict_resena["id_resena"] = id_resena
        self.dict_resena["descripcion"] = descripcion
        self.dict_resena["id_usuario"] = id_usuario
        self.dict_resena["fecha_creacion"] = fecha_creacion
        self.dict_resena["fecha_modificacion"] = fecha_modificacion
