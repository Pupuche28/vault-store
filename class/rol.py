class clsRol:
    id_rol = 0
    nombre = ""
    dict_rol = dict()

    def __init__(self, id_rol, nombre):
        self.id_rol = id_rol
        self.nombre = nombre

        # Llenar el diccionario
        self.dict_rol["id_rol"] = id_rol
        self.dict_rol["nombre"] = nombre
