
CREATE DATABASE IF NOT EXISTS kiosco;
USE kiosco;

CREATE TABLE sucursal (
    id_sucursal INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    direccion VARCHAR(100)
);

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
    extraccion DECIMAL(10,2),
    monto_cierre DECIMAL(10,2),
    id_empleado INT,
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
);

CREATE TABLE metodo_pago (
    id_metodo INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL  -- Efectivo, Tarjeta, Transferencia, etc.
);

CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    telefono VARCHAR(20),
    direccion VARCHAR(150)
);

CREATE TABLE venta (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    id_empleado INT,
    id_caja INT,
    id_metodo INT,
    id_cliente INT,
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado),
    FOREIGN KEY (id_caja) REFERENCES caja(id_caja),
    FOREIGN KEY (id_metodo) REFERENCES metodo_pago(id_metodo),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);


CREATE TABLE detalle_venta (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    FOREIGN KEY (id_venta) REFERENCES venta(id_venta) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
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
    FOREIGN KEY (id_caja) REFERENCES caja(id_caja)
);

CREATE TABLE inventario_movimiento (
    id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT,
    tipo_movimiento VARCHAR(20), -- Entrada o Salida
    cantidad INT,
    fecha DATETIME,
    id_empleado INT,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
);

INSERT INTO metodo_pago (tipo) VALUES ('Efectivo'), ('Tarjeta'), ('Transferencia');

INSERT INTO cliente (nombre, telefono, direccion) VALUES
('Cliente genérico', '0000-0000', 'Sin dirección');
