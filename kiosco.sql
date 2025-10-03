CREATE DATABASE kiosco;
USE kiosco;

CREATE TABLE sucursal (
Id_empresa INT AUTO_INCREMENT PRIMARY KEY,
Nombre VARCHAR(100),
Direccion VARCHAR(100)
);
DROP TABLE empresa;
CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    contraseña VARCHAR(100) NOT NULL,
    nombre VARCHAR(100),
    tipo VARCHAR(20) -- 'admin', 'empleado'
    
);
CREATE TABLE admin (
    id_admin INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);


CREATE TABLE empleado (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    rol VARCHAR(50),
    dni VARCHAR(20) UNIQUE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE proveedor (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    contacto VARCHAR(100),
    telefono VARCHAR(20),
    direccion TEXT
);
CREATE TABLE producto (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    precio DECIMAL(10,2),
    id_proveedor INT,
    FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor)
);
CREATE TABLE stock (
    id_stock INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT,
    cantidad INT,
    fecha_actualizacion DATE,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

CREATE TABLE turno (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    nombre_turno VARCHAR(50),
    hora_inicio TIME,
    hora_fin TIME
);


CREATE TABLE turno_empleado (
    id_turno_empleado INT AUTO_INCREMENT PRIMARY KEY,
    id_empleado INT,
    id_turno INT,
    fecha DATE,
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado),
    FOREIGN KEY (id_turno) REFERENCES turno(id_turno)
);


CREATE TABLE caja (
    id_caja INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    monto_apertura DECIMAL(10,2),
    extraccion DECIMAL (10,2),
    monto_cierre DECIMAL(10,2),
    id_empleado INT,
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
);


CREATE TABLE venta (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME,
    id_empleado INT,
    id_usuario INT,
    id_caja INT,
    total DECIMAL(10,2),
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_caja) REFERENCES caja(id_caja)
);


CREATE TABLE detalle_venta (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT,
    id_producto INT,
    cantidad INT,
    precio_unitario DECIMAL(10,2),
    subtotal DECIMAL(10,2),
    FOREIGN KEY (id_venta) REFERENCES venta(id_venta),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);


CREATE TABLE metodo_pago (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT,
    tipo_pago VARCHAR(50),
    monto DECIMAL(10,2),
    FOREIGN KEY (id_venta) REFERENCES venta(id_venta)
);


CREATE TABLE historial_precio (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT,
    precio DECIMAL(10,2),
    fecha_inicio DATE,
    fecha_fin DATE,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

CREATE TABLE gasto (
    id_gasto INT AUTO_INCREMENT PRIMARY KEY,
    descripcion TEXT,
    monto DECIMAL(10,2),
    fecha DATE,
    id_empleado INT,
    id_caja INT,
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado),
    FOREIGN KEY (id_caja) REFERENCES caja (id_caja)
);

 CREATE TABLE inventario_movimiento (
   id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
  id_producto INT,
 tipo_movimiento VARCHAR(20), 
 cantidad INT,
 fecha DATETIME,
 id_empleado INT,
 FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
 FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
 );
 
 
 
