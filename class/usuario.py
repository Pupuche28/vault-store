class clsUsuario:
    id_usuario = 0
    nombres = ""
    apellidos = ""
    email = ""
    telefono = ""
    nro_doc_ide = ""
    contrasena = ""
    direccion = ""
    id_rol = 0
    fecha_creacion = ""
    fecha_modificacion = ""
    dict_usuario = dict()

    def __init__(self, id_usuario, nombres, apellidos, email, telefono, nro_doc_ide, contrasena, direccion, id_rol, fecha_creacion, fecha_modificacion):
        self.id_usuario = id_usuario
        self.nombres = nombres
        self.apellidos = apellidos
        self.email = email
        self.telefono = telefono
        self.nro_doc_ide = nro_doc_ide
        self.contrasena = contrasena
        self.direccion = direccion
        self.id_rol = id_rol
        self.fecha_creacion = fecha_creacion
        self.fecha_modificacion = fecha_modificacion

        # Llenar el diccionario
        self.dict_usuario["id_usuario"] = id_usuario
        self.dict_usuario["nombres"] = nombres
        self.dict_usuario["apellidos"] = apellidos
        self.dict_usuario["email"] = email
        self.dict_usuario["telefono"] = telefono
        self.dict_usuario["nro_doc_ide"] = nro_doc_ide
        self.dict_usuario["contrasena"] = contrasena
        self.dict_usuario["direccion"] = direccion
        self.dict_usuario["id_rol"] = id_rol
        self.dict_usuario["fecha_creacion"] = fecha_creacion
        self.dict_usuario["fecha_modificacion"] = fecha_modificacion
