use valerecuperacion;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    municipio VARCHAR(100),
    sexo VARCHAR(10), 
	edad VARCHAR(20)
);

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio_compra DECIMAL(10, 2) NOT NULL,
    precio_venta DECIMAL(10, 2) NOT NULL,
    descripcion TEXT,
    stock INT NOT NULL,
    valoracion INT
);

CREATE TABLE ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_venta DATE NOT NULL,
    cantidad INT NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    producto_id INT,
    cliente_nombre VARCHAR(100) NOT NULL,
    cliente_email VARCHAR(100) NOT NULL,
    forma_pago VARCHAR(50) NOT NULL,
    direccion_entrega VARCHAR(200) NOT NULL,
    ciudad_entrega VARCHAR(100) NOT NULL,
    estado_entrega VARCHAR(100) NOT NULL,
    codigo_postal VARCHAR(10) NOT NULL,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);
drop table ventas;
select * from productos;
select * from ventas;

drop table categorias;
drop table productos;
select * from usuarios;

drop table usuarios;
