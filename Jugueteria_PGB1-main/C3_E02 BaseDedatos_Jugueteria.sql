DROP DATABASE Jugueteria;
CREATE DATABASE Jugueteria;
USE Jugueteria;

CREATE TABLE Municipio (
Id_Municipio INT auto_increment PRIMARY KEY,
Nombre VARCHAR(100) NOT NULL
);

CREATE TABLE Departamento (
Id_Departamento INT AUTO_INCREMENT PRIMARY KEY,
Nombre VARCHAR(100) NOT NULL,
Descripcion VARCHAR(255),
Id_Municipio INT UNIQUE,
FOREIGN KEY (Id_Municipio) REFERENCES Municipio(Id_Municipio)
);

CREATE TABLE Linea_Producto (
Id_Linea INT AUTO_INCREMENT PRIMARY KEY,
Nombre VARCHAR(100) NOT NULL,
Descripcion VARCHAR(255)
);

CREATE TABLE Producto (
    Id_Producto INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion VARCHAR(255),
    Fecha_Vencimiento DATE,
    Cantidad INT,
    Valor_Unitario DECIMAL(10,2),
    Id_Linea INT,
    FOREIGN KEY (Id_Linea) REFERENCES Linea_Producto(Id_Linea)
);

CREATE TABLE Cliente (
    Id_Cliente INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Fecha_Nacimiento DATE,
    Historial_Compras TEXT
);

CREATE TABLE Venta (
    Id_Venta INT AUTO_INCREMENT PRIMARY KEY,
    Descripcion VARCHAR(255),
    Valor_Total DECIMAL(10,2)
);

CREATE TABLE Detalle_Venta (
    Id_Venta INT,
    Id_Producto INT,
    Cantidad_Producto INT,
    PRIMARY KEY (Id_Venta, Id_Producto),
    FOREIGN KEY (Id_Venta) REFERENCES Venta(Id_Venta),
    FOREIGN KEY (Id_Producto) REFERENCES Producto(Id_Producto)
);
CREATE TABLE Compra (
    Id_Cliente INT,
    Id_Producto INT,
    PRIMARY KEY (Id_Cliente, Id_Producto),
    FOREIGN KEY (Id_Cliente) REFERENCES Cliente(Id_Cliente),
    FOREIGN KEY (Id_Producto) REFERENCES Producto(Id_Producto)
);

--- Registro de datos 
INSERT INTO Municipio (Nombre) VALUES
('Bogota'),
('Medellín'),
('Cali'),
('Barranquilla'),
('Cartagena');

INSERT INTO Departamento (Nombre, Descripcion, Id_Municipio) VALUES
('Cundinamarca', 'Departamento central del país', 1),
('Antioquia', 'Departamento del noroccidente', 2),
('Valle del Cauca', 'Departamento del suroccidente', 3),
('Atlántico', 'Departamento costero norte', 4),
('Bolívar', 'Departamento histórico del Caribe', 5);

INSERT INTO Linea_Producto (Nombre, Descripcion) VALUES
('Juguetes Educativos', 'Juguetes que estimulan el aprendizaje'),
('Juguetes Electrónicos', 'Incluyen componentes eléctricos o baterías'),
('Muñecos y Figuras', 'Incluye muñecas, superhéroes,'),
('Juegos de Mesa', 'Juegos familiares o de estrategia'),
('Vehículos', 'Carros, trenes, aviones y similares');

INSERT INTO Producto (Nombre, Descripcion, Fecha_Vencimiento, Cantidad, Valor_Unitario, Id_Linea) VALUES
('Lego Classic', 'Bloques para construir figuras', '2028-12-31', 50, 120000, 1),
('Robot Interactivo', 'Robot que responde a comandos', '2027-05-10', 30, 250000, 2),
('Muñeca Barbie', 'Muñeca articulada con accesorios', '2030-01-01', 40, 80000, 3),
('Ajedrez Profesional', 'Juego de ajedrez con piezas de madera', '2035-06-15', 20, 60000, 4),
('Carro de Bomberos', 'Carro de juguete metálico', '2032-09-01', 60, 45000, 5);

INSERT INTO Cliente (Nombre, Fecha_Nacimiento, Historial_Compras) VALUES
('Laura Gómez', '1990-03-15', 'Compró juguetes educativos en 2023'),
('Carlos Ruiz', '1988-07-22', 'Compró juegos de mesa en 2024'),
('Ana Torres', '1995-11-10', 'Compró muñecas y figuras'),
('Luis Pérez', '2000-02-05', 'Cliente frecuente de juguetes electrónicos'),
('María López', '1993-09-30', 'Ha comprado carros de juguete varias veces');

INSERT INTO Venta (Descripcion, Valor_Total) VALUES
('Venta de productos educativos', 350000),
('Venta de juguetes electrónicos', 500000),
('Venta de muñecas y accesorios', 240000),
('Venta de juegos de mesa', 180000),
('Venta de vehículos de juguete', 300000);

INSERT INTO Detalle_Venta (Id_Venta, Id_Producto, Cantidad_Producto) VALUES
(1, 1, 3),
(2, 2, 2),
(3, 3, 5),
(4, 4, 2),
(5, 5, 4);

INSERT INTO Compra (Id_Cliente, Id_Producto) VALUES
(1, 1),
(1, 4),
(2, 2),
(3, 3),
(4, 2),
(5, 5);

--- Pruebas de datos registrados
SHOW TABLES;

SELECT * FROM Municipio;
SELECT * FROM Departamento;
SELECT * FROM Linea_Producto;
SELECT * FROM Producto;
SELECT * FROM Cliente;
SELECT * FROM Venta;
SELECT * FROM Detalle_Venta;
SELECT * FROM Compra;

