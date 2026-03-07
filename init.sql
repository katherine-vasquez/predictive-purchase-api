USE predictive_purchase;

-- Tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
);

INSERT INTO productos (id, nombre, precio, stock) VALUES
(1,'Laptop Lenovo',3200,15),
(2,'Mouse Logitech',80.5,50),
(3,'Teclado Mecánico Redragon',250.99,30),
(4,'Monitor Samsung 24"',900,20),
(5,'Audífonos Sony',450.75,25),
(6,'Disco Duro Externo 1TB',300.4,40),
(7,'Memoria USB 64GB',45.99,100),
(8,'Silla Gamer',1200,10),
(9,'Webcam HD',150,35),
(10,'Impresora HP',650,12),
(11,'Tablet Samsung',1800,18),
(12,'Smartphone Xiaomi',1400,22),
(13,'Router TP-Link',210.3,28),
(14,'Cable HDMI',25,200),
(15,'Power Bank 20000mAh',130,45),
(16,'Laptop HP',3500,8),
(17,'Monitor LG 27"',1100,14),
(18,'Teclado Inalámbrico',130,50),
(19,'Mouse Pad Gamer',35,150),
(20,'Parlante Bluetooth JBL',500,19),
(21,'Cámara Web Pro',200,30),
(22,'Auriculares Gaming',180,40),
(23,'Dock USB-C',95,25),
(24,'SSD Externo 512GB',220,20),
(25,'Hub USB 4 Puertos',40,80),
(26,'Micrófono Streaming',160,15),
(27,'Luces LED Monitor',70,60);

-- Tabla para entrenamiento del modelo
CREATE TABLE IF NOT EXISTS registros_compra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tiempo_pagina INT,
    productos_vistos INT,
    compra INT
);

-- 50 registros de entrenamiento
INSERT INTO registros_compra (tiempo_pagina, productos_vistos, compra) VALUES
(1,0,0),(1,2,0),(1,4,0),(2,1,0),(2,3,0),
(2,5,0),(3,0,0),(3,2,0),(3,4,1),(4,1,0),
(4,3,1),(4,5,1),(5,2,0),(5,4,1),(5,6,1),
(6,1,0),(6,3,1),(6,5,1),(7,2,1),(7,4,1),
(7,6,1),(8,3,1),(8,5,1),(8,7,1),(9,4,1),
(9,6,1),(9,8,1),(10,5,1),(10,7,1),(10,9,1),
(11,4,1),(11,6,1),(11,8,1),(12,5,1),(12,7,1),
(12,9,1),(13,6,1),(13,8,1),(13,10,1),(14,7,1),
(14,9,1),(14,10,1),(15,8,1),(15,10,1),(16,7,1),
(16,9,1),(17,8,1),(18,9,1),(19,10,1),(20,10,1);