class clsCategoria:
    id_categoria = 0
    nombre = ""
    fecha_creacion = ""
    fecha_modificacion = ""
    dict_categoria = dict()

    def __init__(self, id_categoria, nombre, fecha_creacion, fecha_modificacion):
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.fecha_creacion = fecha_creacion
        self.fecha_modificacion = fecha_modificacion

        # Llenar el diccionario
        self.dict_categoria["id_categoria"] = id_categoria
        self.dict_categoria["nombre"] = nombre
        self.dict_categoria["fecha_creacion"] = fecha_creacion
        self.dict_categoria["fecha_modificacion"] = fecha_modificacion
