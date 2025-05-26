class clsProducto:
    id_producto = 0
    nombre = ""
    autor = ""
    precio = 0.0
    descuento = 0.0
    stock = 0
    nombre_tienda = ""
    descripcion = ""
    caracteristicas = ""
    id_categoria = 0
    imagen = ""
    fecha_creacion = ""
    fecha_modificacion = ""
    dict_producto = dict()

    def __init__(self, id_producto, nombre, autor, precio, descuento, stock, nombre_tienda, descripcion, caracteristicas, id_categoria, imagen, fecha_creacion, fecha_modificacion):
        self.id_producto = id_producto
        self.nombre = nombre
        self.autor = autor
        self.precio = precio
        self.descuento = descuento
        self.stock = stock
        self.nombre_tienda = nombre_tienda
        self.descripcion = descripcion
        self.caracteristicas = caracteristicas
        self.id_categoria = id_categoria
        self.imagen = imagen
        self.fecha_creacion = fecha_creacion
        self.fecha_modificacion = fecha_modificacion

        # Llenar el diccionario
        self.dict_producto["id_producto"] = id_producto
        self.dict_producto["nombre"] = nombre
        self.dict_producto["autor"] = autor
        self.dict_producto["precio"] = precio
        self.dict_producto["descuento"] = descuento
        self.dict_producto["stock"] = stock
        self.dict_producto["nombre_tienda"] = nombre_tienda
        self.dict_producto["descripcion"] = descripcion
        self.dict_producto["caracteristicas"] = caracteristicas
        self.dict_producto["id_categoria"] = id_categoria
        self.dict_producto["imagen"] = imagen
        self.dict_producto["fecha_creacion"] = fecha_creacion
        self.dict_producto["fecha_modificacion"] = fecha_modificacion
