-- Crear tabla ROL primero
CREATE TABLE ROL (
    idRol INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Crear la tabla USUARIO
CREATE TABLE USUARIO (
    idUsuario INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefono CHAR(9) NOT NULL,
    nroDocIde VARCHAR(20) NOT NULL UNIQUE,
    contrasena VARCHAR(64) NOT NULL,
    direccion VARCHAR(100),
    idRol INT NOT NULL,
    fechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fechaModificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (idRol) REFERENCES ROL(idRol)
);

-- Tabla CATEGORIA
CREATE TABLE CATEGORIA (
    idCategoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fechaModificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla RESEÑA
CREATE TABLE RESENA (
    idResena INT AUTO_INCREMENT PRIMARY KEY,
    descripcion TEXT NOT NULL,
    idUsuario INT NOT NULL,
    fechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fechaModificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (idUsuario) REFERENCES USUARIO(idUsuario) ON DELETE CASCADE
);

-- Tabla PRODUCTO
CREATE TABLE PRODUCTO (
    idProducto INT AUTO_INCREMENT PRIMARY KEY,
    nombredeproducto VARCHAR(100) NOT NULL,
    autor VARCHAR(100),
    precio DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(10,2),
    stock INT NOT NULL,
    nombredeTienda VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    caracteristicas TEXT NOT NULL,
    idCategoria INT NOT NULL,
    imagen VARCHAR(255),
    fechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fechaModificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (idCategoria) REFERENCES CATEGORIA(idCategoria) ON DELETE CASCADE
);

-- Tabla TARJETA
CREATE TABLE TARJETA (
    idTarjeta INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    nroTarjeta VARCHAR(16),
    fecha DATE,
    ccv VARCHAR(3),
    idUsuario INT,
    fechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fechaModificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (idUsuario) REFERENCES USUARIO(idUsuario) ON DELETE CASCADE
);

-- Tabla PEDIDO
CREATE TABLE PEDIDO (
    idPedido INT AUTO_INCREMENT PRIMARY KEY,
    fechainicio DATE,
    fechafinalizado DATE,
    estado VARCHAR(50),
    idUsuario INT,
    fechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fechaModificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (idUsuario) REFERENCES USUARIO(idUsuario) ON DELETE CASCADE
);

-- Tabla PAGO
CREATE TABLE PAGO (
    idPago INT AUTO_INCREMENT PRIMARY KEY,
    fechapago DATE,
    monto DECIMAL(10,2),
    metodopago VARCHAR(50),
    idPedido INT,
    idTarjeta INT,
    fechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fechaModificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (idPedido) REFERENCES PEDIDO(idPedido) ON DELETE CASCADE,
    FOREIGN KEY (idTarjeta) REFERENCES TARJETA(idTarjeta) ON DELETE CASCADE
);

-- Tabla DETALLE_PEDIDO
CREATE TABLE DETALLE_PEDIDO (
    idPedido INT,
    idProducto INT,
    cantidad INT,
    precio DECIMAL(10,2),
    descuento DECIMAL(5,2),
    igv DECIMAL(5,2),
    subtotal DECIMAL(10,2),
    total DECIMAL(10,2),
    fechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fechaModificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (idPedido, idProducto),
    FOREIGN KEY (idPedido) REFERENCES PEDIDO(idPedido) ON DELETE CASCADE,
    FOREIGN KEY (idProducto) REFERENCES PRODUCTO(idProducto) ON DELETE CASCADE
);



-- Insertar roles iniciales en la tabla ROL
INSERT INTO ROL (nombre) VALUES ('Administrador');
INSERT INTO ROL (nombre) VALUES ('Cliente');

-- Insertar usuarios de ejemplo en la tabla USUARIO
INSERT INTO USUARIO (nombres, apellidos, email, telefono, nroDocIde, contrasena, direccion, idRol) 
VALUES ('Kheinner', 'Sosa', 'sosa@gmail.com', '981339485', '75062816', 'admin123', 'Sta Cruz de Pachacutec 294', 1);

INSERT INTO USUARIO (nombres, apellidos, email, telefono, nroDocIde, contrasena, direccion, idRol) 
VALUES ('Rodrigho', 'Pupuche', 'rodrigho@gmail.com', '987654321', '87654321', 'cliente123', 'JLO Girasoles 123', 2);

-- Insertar categorías iniciales en la tabla CATEGORIA
INSERT INTO CATEGORIA (nombre) VALUES ('Celulares');
INSERT INTO CATEGORIA (nombre) VALUES ('Laptops');
INSERT INTO CATEGORIA (nombre) VALUES ('Tablets');
INSERT INTO CATEGORIA (nombre) VALUES ('Televisores');

-- Inserts de productos para la categoría 'Celulares'
INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Honor 7 Lite', 'Honor', 1500.00, 100.00, 50, 'MarketCell', 'Smartphone con buen rendimiento y diseño moderno.', 'Pantalla HD, cámara dual, batería duradera', 1, 'celular_honor.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Huawei Pura 70', 'Huawei', 4000.00, 400.00, 30, 'MarketCell', 'Celular potente y elegante.', 'Cámara avanzada, carga rápida, pantalla OLED', 1, 'celular_huawei.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('iPhone 16 Pro Max', 'Apple', 5000.00, 200.00, 20, 'MarketCell', 'iPhone de última generación con alto rendimiento.', 'Chip A18, Face ID, cámara triple', 1, 'celular_iphone.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Moto G75', 'Motorola', 950.00, 150.00, 25, 'MarketCell', 'Teléfono accesible con buen desempeño.', 'Pantalla grande, buena batería, cámara doble', 1, 'celular_motorola.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Samsung S24 Ultra', 'Samsung', 3500.00, 200.00, 15, 'MarketCell', 'Celular premium con tecnología avanzada.', 'S Pen, cámara de alta resolución, pantalla AMOLED', 1, 'celular_samsung.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Poco X7 Pro', 'Xiaomi', 1400.00, 140.00, 10, 'MarketCell', 'Smartphone con buen rendimiento a bajo costo.', 'Procesador rápido, pantalla fluida, buena batería', 1, 'celular_xiaomi.webp');


-- Inserts de productos para la categoría 'Laptops'
INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Laptop Acer Core i7', 'Acer', 3000.00, 300.00, 40, 'GameStore', 'Laptop potente ideal para trabajo y estudio.', 'Procesador Intel Core i7, 16GB RAM, SSD 512GB', 2, 'laptop_acer.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('MacBook Air 13 Chip M4', 'Apple', 4000.00, 100.00, 60, 'GameStore', 'Laptop ligera y eficiente para uso diario.', 'Chip M4, pantalla Retina, batería de larga duración', 2, 'laptop_apple.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Laptop TUF Gaming F15', 'Asus', 2499.00, 50.00, 20, 'GameStore', 'Laptop gamer con alto rendimiento.', 'Pantalla 144Hz, RTX 3050, teclado retroiluminado', 2, 'laptop_asus.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Laptop Dell', 'Dell', 1399.00, 100.00, 25, 'GameStore', 'Laptop confiable para tareas diarias.', 'Procesador Intel, 8GB RAM, disco SSD', 2, 'laptop_dell.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Laptop HP', 'HP', 1800.00, 150.00, 30, 'GameStore', 'Portátil eficiente con diseño moderno.', 'Pantalla Full HD, buen rendimiento, teclado cómodo', 2, 'laptop_hp.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Laptop MSI', 'MSI', 5200.00, 450.00, 15, 'GameStore', 'Laptop de alto rendimiento para gaming y diseño.', 'Gráfica potente, gran capacidad de almacenamiento, refrigeración avanzada', 2, 'laptop_msi.webp');


-- Inserts de productos para la categoría 'Tablets'
INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Tablet Advance', 'Advance', 599.00, 40.00, 10, 'TechZone', 'Tablet básica para uso diario.', 'Pantalla táctil, Wi-Fi, buena duración de batería', 3, 'tablet_advance.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('iPad Quinta Generación', 'Apple', 1499.00, 50.00, 8, 'iStore', 'iPad rápido y ligero.', 'Pantalla Retina, chip A13, sistema iPadOS', 3, 'tablet_apple.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Tablet Huawei', 'Huawei', 1469.00, 35.00, 12, 'Huawei Center', 'Tablet eficiente y moderna.', 'Pantalla Full HD, buen rendimiento, cámara frontal', 3, 'tablet_huawei.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Tablet Lenovo', 'Lenovo', 999.00, 45.00, 10, 'Digital World', 'Tablet compacta ideal para entretenimiento.', 'Altavoces estéreo, buena batería, Android', 3, 'tablet_lenovo.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Tablet Samsung', 'Samsung', 1899.00, 40.00, 9, 'Samsung Shop', 'Tablet de alto rendimiento con gran pantalla.', 'Pantalla AMOLED, S Pen, gran capacidad', 3, 'tablet_samsung.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Tablet Xiaomi', 'Xiaomi', 599.00, 50.00, 7, 'Mi Store', 'Tablet accesible con buen diseño.', 'Procesador rápido, pantalla HD, batería duradera', 3, 'tablet_xiaomi.webp');


-- Inserts de productos para la categoría 'Televisores'
INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Smart TV CAIXUN 43"', 'Caixun', 899.00, 100.00, 50, 'TechZone', 'Smart TV con buena calidad de imagen.', 'Pantalla LED Full HD, entradas HDMI y USB', 4, 'televisor_caixun.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Smart TV Samsung 50"', 'LG', 1599.00, 200.00, 30, 'VisionStore', 'Smart TV con excelente resolución y sonido.', '4K UHD, HDR10+, sistema Tizen', 4, 'televisor_lg.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Smart TV Samsung 65"', 'Samsung', 2299.00, 250.00, 20, 'MegaTech', 'Televisor grande con imagen nítida.', '4K UHD, Smart Hub, control por voz', 4, 'televisor_samsung.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Smart TV Sony 55"', 'Sony', 1999.00, 180.00, 40, 'ElectroCity', 'Smart TV con tecnología avanzada.', '4K UHD, Android TV, sonido envolvente', 4, 'televisor_sony.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Smart TV TCL 50"', 'TCL', 1399.00, 150.00, 15, 'TechnoWorld', 'TV inteligente con buena relación calidad-precio.', 'Roku TV integrado, HDR, múltiples puertos', 4, 'televisor_tcl.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Smart TV Xiaomi 85"', 'Xiaomi', 2699.00, 300.00, 50, 'DigitalPlaza', 'Pantalla gigante con resolución impresionante.', '4K UHD, Dolby Vision, sistema PatchWall', 4, 'televisor_xiaomi.webp');


-- Insertar reseñas de ejemplo en la tabla RESEÑA
INSERT INTO RESENA (descripcion, idUsuario) 
VALUES ('Reseña del producto 1 por el cliente', 2);

INSERT INTO RESENA (descripcion, idUsuario) 
VALUES ('Reseña del producto 2 por el cliente', 2);

INSERT INTO RESENA (descripcion, idUsuario) 
VALUES ('Reseña del producto 3 por el cliente', 2);