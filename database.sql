-- ========================================================
-- SISTEMA BIBLIOTECARIO PCA - SCRIPT DE BASE DE DATOS
-- Motor: MySQL 8.0+
-- Caracteres: UTF-8 (utf8mb4)
-- ========================================================

CREATE DATABASE IF NOT EXISTS biblioteca_pca DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE biblioteca_pca;

-- Eliminar tablas si existen (orden inverso a FKs)
DROP TABLE IF EXISTS prestamos;
DROP TABLE IF EXISTS libros;
DROP TABLE IF EXISTS estudiantes;
DROP TABLE IF EXISTS autores;

-- ========================================================
-- DDL - ESTRUCTURA DE TABLAS
-- ========================================================

-- TABLA: autores
CREATE TABLE autores (
    id CHAR(36) NOT NULL,
    documento_identidad VARCHAR(50) NOT NULL,
    nombre_completo VARCHAR(150) NOT NULL,
    correo VARCHAR(100) NULL,
    telefono VARCHAR(20) NULL,
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_autores_documento (documento_identidad),
    UNIQUE KEY uk_autores_correo (correo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TABLA: estudiantes
CREATE TABLE estudiantes (
    id CHAR(36) NOT NULL,
    documento_identidad VARCHAR(50) NOT NULL,
    nombre_completo VARCHAR(150) NOT NULL,
    correo_institucional VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NULL,
    carrera VARCHAR(100) NOT NULL,
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_estudiantes_documento (documento_identidad),
    UNIQUE KEY uk_estudiantes_correo (correo_institucional)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TABLA: libros
CREATE TABLE libros (
    id CHAR(36) NOT NULL,
    isbn VARCHAR(20) NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    autor_id CHAR(36) NOT NULL,
    editorial VARCHAR(100) NOT NULL,
    anio_publicacion INT NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    cantidad_total INT NOT NULL DEFAULT 0,
    cantidad_disponible INT NOT NULL DEFAULT 0,
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_libros_isbn (isbn),
    KEY idx_libros_autor (autor_id),
    CONSTRAINT fk_libros_autores FOREIGN KEY (autor_id) REFERENCES autores (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_libros_total CHECK (cantidad_total >= 0),
    CONSTRAINT chk_libros_disponible CHECK (cantidad_disponible >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TABLA: prestamos
CREATE TABLE prestamos (
    id CHAR(36) NOT NULL,
    estudiante_id CHAR(36) NOT NULL,
    libro_id CHAR(36) NOT NULL,
    fecha_salida DATETIME NOT NULL,
    fecha_pactada DATETIME NOT NULL,
    fecha_real DATETIME NULL,
    estado_prestamo ENUM('Activo', 'Devuelto', 'Atrasado') NOT NULL DEFAULT 'Activo',
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_prestamos_estudiante (estudiante_id),
    KEY idx_prestamos_libro (libro_id),
    KEY idx_prestamos_estado (estado_prestamo),
    CONSTRAINT fk_prestamos_estudiantes FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_prestamos_libros FOREIGN KEY (libro_id) REFERENCES libros (id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================================================
-- DML - INSERT DE DATOS DE PRUEBA (30 REGISTROS POR ENTIDAD)
-- ========================================================

-- INSERT 30 AUTORES
INSERT INTO autores (id, documento_identidad, nombre_completo, correo, telefono, estado) VALUES
('a0000000-0000-0000-0000-000000000001', 'AUT-DOC-1001', 'Gabriel García Márquez', 'gabriel.garcia@autores.com', '+57 3001234501', TRUE),
('a0000000-0000-0000-0000-000000000002', 'AUT-DOC-1002', 'Isabel Allende', 'isabel.allende@autores.com', '+56 912345602', TRUE),
('a0000000-0000-0000-0000-000000000003', 'AUT-DOC-1003', 'Mario Vargas Llosa', 'mario.vargas@autores.com', '+51 987654303', TRUE),
('a0000000-0000-0000-0000-000000000004', 'AUT-DOC-1004', 'Jorge Luis Borges', 'jorge.borges@autores.com', '+54 911234504', TRUE),
('a0000000-0000-0000-0000-000000000005', 'AUT-DOC-1005', 'Julio Cortázar', 'julio.cortazar@autores.com', '+54 911234505', TRUE),
('a0000000-0000-0000-0000-000000000006', 'AUT-DOC-1006', 'Miguel de Cervantes', 'miguel.cervantes@autores.com', '+34 600123406', TRUE),
('a0000000-0000-0000-0000-000000000007', 'AUT-DOC-1007', 'Pablo Neruda', 'pablo.neruda@autores.com', '+56 912345607', TRUE),
('a0000000-0000-0000-0000-000000000008', 'AUT-DOC-1008', 'Gabriela Mistral', 'gabriela.mistral@autores.com', '+56 912345608', TRUE),
('a0000000-0000-0000-0000-000000000009', 'AUT-DOC-1009', 'Octavio Paz', 'octavio.paz@autores.com', '+52 5512345609', TRUE),
('a0000000-0000-0000-0000-000000000010', 'AUT-DOC-1010', 'Juan Rulfo', 'juan.rulfo@autores.com', '+52 5512345610', TRUE),
('a0000000-0000-0000-0000-000000000011', 'AUT-DOC-1011', 'Laura Esquivel', 'laura.esquivel@autores.com', '+52 5512345611', TRUE),
('a0000000-0000-0000-0000-000000000012', 'AUT-DOC-1012', 'Carlos Fuentes', 'carlos.fuentes@autores.com', '+52 5512345612', TRUE),
('a0000000-0000-0000-0000-000000000013', 'AUT-DOC-1013', 'Mario Benedetti', 'mario.benedetti@autores.com', '+598 99123413', TRUE),
('a0000000-0000-0000-0000-000000000014', 'AUT-DOC-1014', 'Eduardo Galeano', 'eduardo.galeano@autores.com', '+598 99123414', TRUE),
('a0000000-0000-0000-0000-000000000015', 'AUT-DOC-1015', 'Ernesto Sabato', 'ernesto.sabato@autores.com', '+54 911234515', TRUE),
('a0000000-0000-0000-0000-000000000016', 'AUT-DOC-1016', 'Horacio Quiroga', 'horacio.quiroga@autores.com', '+598 99123416', TRUE),
('a0000000-0000-0000-0000-000000000017', 'AUT-DOC-1017', 'César Vallejo', 'cesar.vallejo@autores.com', '+51 987654317', TRUE),
('a0000000-0000-0000-0000-000000000018', 'AUT-DOC-1018', 'José Martí', 'jose.marti@autores.com', '+53 51234518', TRUE),
('a0000000-0000-0000-0000-000000000019', 'AUT-DOC-1019', 'Alejo Carpentier', 'alejo.carpentier@autores.com', '+53 51234519', TRUE),
('a0000000-0000-0000-0000-000000000020', 'AUT-DOC-1020', 'José Saramago', 'jose.saramago@autores.com', '+351 912345620', TRUE),
('a0000000-0000-0000-0000-000000000021', 'AUT-DOC-1021', 'Fernando Pessoa', 'fernando.pessoa@autores.com', '+351 912345621', TRUE),
('a0000000-0000-0000-0000-000000000022', 'AUT-DOC-1022', 'Arturo Pérez-Reverte', 'arturo.perez@autores.com', '+34 600123422', TRUE),
('a0000000-0000-0000-0000-000000000023', 'AUT-DOC-1023', 'Javier Marías', 'javier.marias@autores.com', '+34 600123423', TRUE),
('a0000000-0000-0000-0000-000000000024', 'AUT-DOC-1024', 'Rosa Montero', 'rosa.montero@autores.com', '+34 600123424', TRUE),
('a0000000-0000-0000-0000-000000000025', 'AUT-DOC-1025', 'Carlos Ruiz Zafón', 'carlos.ruiz@autores.com', '+34 600123425', TRUE),
('a0000000-0000-0000-0000-000000000026', 'AUT-DOC-1026', 'Jorge Amado', 'jorge.amado@autores.com', '+55 219123426', TRUE),
('a0000000-0000-0000-0000-000000000027', 'AUT-DOC-1027', 'Clarice Lispector', 'clarice.lispector@autores.com', '+55 219123427', TRUE),
('a0000000-0000-0000-0000-000000000028', 'AUT-DOC-1028', 'Paulo Coelho', 'paulo.coelho@autores.com', '+55 219123428', TRUE),
('a0000000-0000-0000-0000-000000000029', 'AUT-DOC-1029', 'Roberto Bolaño', 'roberto.bolano@autores.com', '+56 912345629', TRUE),
('a0000000-0000-0000-0000-000000000030', 'AUT-DOC-1030', 'Álvaro Mutis', 'alvaro.mutis@autores.com', '+57 3001234530', TRUE);

-- INSERT 30 ESTUDIANTES
INSERT INTO estudiantes (id, documento_identidad, nombre_completo, correo_institucional, telefono, carrera, estado) VALUES
('e0000000-0000-0000-0000-000000000001', '1001234001', 'Carlos Andrés Mendoza', 'carlos.mendoza1@pca.edu.co', '+57 3100000001', 'Ingeniería de Sistemas', TRUE),
('e0000000-0000-0000-0000-000000000002', '1001234002', 'María Fernanda Gómez', 'maría.gómez2@pca.edu.co', '+57 3100000002', 'Administración de Empresas', TRUE),
('e0000000-0000-0000-0000-000000000003', '1001234003', 'Juan David Rodríguez', 'juan.rodríguez3@pca.edu.co', '+57 3100000003', 'Derecho', TRUE),
('e0000000-0000-0000-0000-000000000004', '1001234004', 'Ana Lucía Martínez', 'ana.martínez4@pca.edu.co', '+57 3100000004', 'Psicología', TRUE),
('e0000000-0000-0000-0000-000000000005', '1001234005', 'Santiago José López', 'santiago.lópez5@pca.edu.co', '+57 3100000005', 'Contaduría Pública', TRUE),
('e0000000-0000-0000-0000-000000000006', '1001234006', 'Valentina Torres', 'valentina.torres6@pca.edu.co', '+57 3100000006', 'Ingeniería Industrial', TRUE),
('e0000000-0000-0000-0000-000000000007', '1001234007', 'Sebastián Castro', 'sebastián.castro7@pca.edu.co', '+57 3100000007', 'Diseño Gráfico', TRUE),
('e0000000-0000-0000-0000-000000000008', '1001234008', 'Daniela Ramírez', 'daniela.ramírez8@pca.edu.co', '+57 3100000008', 'Negocios Internacionales', TRUE),
('e0000000-0000-0000-0000-000000000009', '1001234009', 'Mateo Fernández', 'mateo.fernández9@pca.edu.co', '+57 3100000009', 'Ingeniería de Sistemas', TRUE),
('e0000000-0000-0000-0000-000000000010', '1001234010', 'Camila Morales', 'camila.morales10@pca.edu.co', '+57 3100000010', 'Administración de Empresas', TRUE),
('e0000000-0000-0000-0000-000000000011', '1001234011', 'Alejandro Ruiz', 'alejandro.ruiz11@pca.edu.co', '+57 3100000011', 'Derecho', TRUE),
('e0000000-0000-0000-0000-000000000012', '1001234012', 'Sofía Navarro', 'sofía.navarro12@pca.edu.co', '+57 3100000012', 'Psicología', TRUE),
('e0000000-0000-0000-0000-000000000013', '1001234013', 'Diego Armando Silva', 'diego.silva13@pca.edu.co', '+57 3100000013', 'Contaduría Pública', TRUE),
('e0000000-0000-0000-0000-000000000014', '1001234014', 'Mariana Vargas', 'mariana.vargas14@pca.edu.co', '+57 3100000014', 'Ingeniería Industrial', TRUE),
('e0000000-0000-0000-0000-000000000015', '1001234015', 'Nicolás Benítez', 'nicolás.benítez15@pca.edu.co', '+57 3100000015', 'Diseño Gráfico', TRUE),
('e0000000-0000-0000-0000-000000000016', '1001234016', 'Paula Andrea Herrera', 'paula.herrera16@pca.edu.co', '+57 3100000016', 'Negocios Internacionales', TRUE),
('e0000000-0000-0000-0000-000000000017', '1001234017', 'Felipe Gutiérrez', 'felipe.gutiérrez17@pca.edu.co', '+57 3100000017', 'Ingeniería de Sistemas', TRUE),
('e0000000-0000-0000-0000-000000000018', '1001234018', 'Isabella Medina', 'isabella.medina18@pca.edu.co', '+57 3100000018', 'Administración de Empresas', TRUE),
('e0000000-0000-0000-0000-000000000019', '1001234019', 'Samuel Rojas', 'samuel.rojas19@pca.edu.co', '+57 3100000019', 'Derecho', TRUE),
('e0000000-0000-0000-0000-000000000020', '1001234020', 'Gabriela Suárez', 'gabriela.suárez20@pca.edu.co', '+57 3100000020', 'Psicología', TRUE),
('e0000000-0000-0000-0000-000000000021', '1001234021', 'Lucas Delgado', 'lucas.delgado21@pca.edu.co', '+57 3100000021', 'Contaduría Pública', TRUE),
('e0000000-0000-0000-0000-000000000022', '1001234022', 'Valeria Ríos', 'valeria.ríos22@pca.edu.co', '+57 3100000022', 'Ingeniería Industrial', TRUE),
('e0000000-0000-0000-0000-000000000023', '1001234023', 'Tomás Guerrero', 'tomás.guerrero23@pca.edu.co', '+57 3100000023', 'Diseño Gráfico', TRUE),
('e0000000-0000-0000-0000-000000000024', '1001234024', 'Elena Paredes', 'elena.paredes24@pca.edu.co', '+57 3100000024', 'Negocios Internacionales', TRUE),
('e0000000-0000-0000-0000-000000000025', '1001234025', 'Andrés Felipe Franco', 'andrés.franco25@pca.edu.co', '+57 3100000025', 'Ingeniería de Sistemas', TRUE),
('e0000000-0000-0000-0000-000000000026', '1001234026', 'Natalia Acosta', 'natalia.acosta26@pca.edu.co', '+57 3100000026', 'Administración de Empresas', TRUE),
('e0000000-0000-0000-0000-000000000027', '1001234027', 'Julián Cárdenas', 'julián.cárdenas27@pca.edu.co', '+57 3100000027', 'Derecho', TRUE),
('e0000000-0000-0000-0000-000000000028', '1001234028', 'Carolina Ortiz', 'carolina.ortiz28@pca.edu.co', '+57 3100000028', 'Psicología', TRUE),
('e0000000-0000-0000-0000-000000000029', '1001234029', 'Esteban Silva', 'esteban.silva29@pca.edu.co', '+57 3100000029', 'Contaduría Pública', FALSE),
('e0000000-0000-0000-0000-000000000030', '1001234030', 'Laura Camila Salazar', 'laura.salazar30@pca.edu.co', '+57 3100000030', 'Ingeniería Industrial', FALSE);

-- INSERT 30 LIBROS
INSERT INTO libros (id, isbn, titulo, autor_id, editorial, anio_publicacion, categoria, cantidad_total, cantidad_disponible, estado) VALUES
('b0000000-0000-0000-0000-000000000001', '978-958-42-0100-1', 'Cien años de soledad', 'a0000000-0000-0000-0000-000000000001', 'Editorial Sudamericana', 1967, 'Realismo Mágico', 5, 3, TRUE),
('b0000000-0000-0000-0000-000000000002', '978-958-42-0100-2', 'La casa de los espíritus', 'a0000000-0000-0000-0000-000000000002', 'Plaza & Janés', 1982, 'Novela', 4, 2, TRUE),
('b0000000-0000-0000-0000-000000000003', '978-958-42-0100-3', 'La ciudad y los perros', 'a0000000-0000-0000-0000-000000000003', 'Seix Barral', 1963, 'Novela', 3, 1, TRUE),
('b0000000-0000-0000-0000-000000000004', '978-958-42-0100-4', 'Ficciones', 'a0000000-0000-0000-0000-000000000004', 'Editorial Sur', 1944, 'Cuento', 6, 4, TRUE),
('b0000000-0000-0000-0000-000000000005', '978-958-42-0100-5', 'Rayuela', 'a0000000-0000-0000-0000-000000000005', 'Editorial Sudamericana', 1963, 'Novela', 4, 2, TRUE),
('b0000000-0000-0000-0000-000000000006', '978-958-42-0100-6', 'Don Quijote de la Mancha', 'a0000000-0000-0000-0000-000000000006', 'Juan de la Cuesta', 1605, 'Clásico', 5, 5, TRUE),
('b0000000-0000-0000-0000-000000000007', '978-958-42-0100-7', 'Twenty Love Poems', 'a0000000-0000-0000-0000-000000000007', 'Editorial Nascimento', 1924, 'Poesía', 3, 3, TRUE),
('b0000000-0000-0000-0000-000000000008', '978-958-42-0100-8', 'Desolación', 'a0000000-0000-0000-0000-000000000008', 'Instituto de las Españas', 1922, 'Poesía', 2, 1, TRUE),
('b0000000-0000-0000-0000-000000000009', '978-958-42-0100-9', 'El laberinto de la soledad', 'a0000000-0000-0000-0000-000000000009', 'Cuadernos Americanos', 1950, 'Ensayo', 4, 3, TRUE),
('b0000000-0000-0000-0000-000000000010', '978-958-42-0100-10', 'Pedro Páramo', 'a0000000-0000-0000-0000-000000000010', 'Fondo de Cultura Económica', 1955, 'Novela', 5, 2, TRUE),
('b0000000-0000-0000-0000-000000000011', '978-958-42-0100-11', 'Como agua para chocolate', 'a0000000-0000-0000-0000-000000000011', 'Muguerza', 1989, 'Realismo Mágico', 4, 4, TRUE),
('b0000000-0000-0000-0000-000000000012', '978-958-42-0100-12', 'La muerte de Artemio Cruz', 'a0000000-0000-0000-0000-000000000012', 'Fondo de Cultura Económica', 1962, 'Novela', 3, 2, TRUE),
('b0000000-0000-0000-0000-000000000013', '978-958-42-0100-13', 'La tregua', 'a0000000-0000-0000-0000-000000000013', 'Alfa', 1960, 'Novela', 4, 1, TRUE),
('b0000000-0000-0000-0000-000000000014', '978-958-42-0100-14', 'Las venas abiertas de América Latina', 'a0000000-0000-0000-0000-000000000014', 'Universidad de la República', 1971, 'Ensayo', 5, 3, TRUE),
('b0000000-0000-0000-0000-000000000015', '978-958-42-0100-15', 'El túnel', 'a0000000-0000-0000-0000-000000000015', 'Sur', 1948, 'Novela Psicológica', 4, 3, TRUE),
('b0000000-0000-0000-0000-000000000016', '978-958-42-0100-16', 'Cuentos de la selva', 'a0000000-0000-0000-0000-000000000016', 'Sociedad Cooperativa Editorial', 1918, 'Infantil / Cuento', 3, 3, TRUE),
('b0000000-0000-0000-0000-000000000017', '978-958-42-0100-17', 'Los heraldos negros', 'a0000000-0000-0000-0000-000000000017', 'Imprenta del Estado', 1919, 'Poesía', 2, 2, TRUE),
('b0000000-0000-0000-0000-000000000018', '978-958-42-0100-18', 'Ismaelillo', 'a0000000-0000-0000-0000-000000000018', 'Thompson & Moreau', 1882, 'Poesía', 3, 2, TRUE),
('b0000000-0000-0000-0000-000000000019', '978-958-42-0100-19', 'El siglo de las luces', 'a0000000-0000-0000-0000-000000000019', 'Seix Barral', 1962, 'Novela Histórica', 4, 4, TRUE),
('b0000000-0000-0000-0000-000000000020', '978-958-42-0100-20', 'Ensayo sobre la ceguera', 'a0000000-0000-0000-0000-000000000020', 'Caminho', 1995, 'Novela', 5, 1, TRUE),
('b0000000-0000-0000-0000-000000000021', '978-958-42-0100-21', 'El libro de las desasosiegos', 'a0000000-0000-0000-0000-000000000021', 'Ática', 1982, 'Poesía / Ensayo', 3, 2, TRUE),
('b0000000-0000-0000-0000-000000000022', '978-958-42-0100-22', 'El capitán Alatriste', 'a0000000-0000-0000-0000-000000000022', 'Alfaguara', 1996, 'Novela Histórica', 4, 3, TRUE),
('b0000000-0000-0000-0000-000000000023', '978-958-42-0100-23', 'Corazón tan blanco', 'a0000000-0000-0000-0000-000000000023', 'Anagrama', 1992, 'Novela', 3, 2, TRUE),
('b0000000-0000-0000-0000-000000000024', '978-958-42-0100-24', 'La loca de la casa', 'a0000000-0000-0000-0000-000000000024', 'Alfaguara', 2003, 'Ensayo / Novela', 2, 1, TRUE),
('b0000000-0000-0000-0000-000000000025', '978-958-42-0100-25', 'La sombra del viento', 'a0000000-0000-0000-0000-000000000025', 'Planeta', 2001, 'Novela MISTERIO', 6, 4, TRUE),
('b0000000-0000-0000-0000-000000000026', '978-958-42-0100-26', 'Capitanes de la arena', 'a0000000-0000-0000-0000-000000000026', 'José Olympio', 1937, 'Novela', 3, 2, TRUE),
('b0000000-0000-0000-0000-000000000027', '978-958-42-0100-27', 'La hora de la estrella', 'a0000000-0000-0000-0000-000000000027', 'Livraria José Olympio Editora', 1977, 'Novela', 3, 3, TRUE),
('b0000000-0000-0000-0000-000000000028', '978-958-42-0100-28', 'El alquimista', 'a0000000-0000-0000-0000-000000000028', 'Rocco', 1988, 'Ficción / Filosofía', 5, 2, TRUE),
('b0000000-0000-0000-0000-000000000029', '978-958-42-0100-29', 'Los detectives salvajes', 'a0000000-0000-0000-0000-000000000029', 'Anagrama', 1998, 'Novela', 4, 1, TRUE),
('b0000000-0000-0000-0000-000000000030', '978-958-42-0100-30', 'La nieve del almirante', 'a0000000-0000-0000-0000-000000000030', 'Alianza Editorial', 1986, 'Novela', 3, 2, FALSE);

-- INSERT 30 PRÉSTAMOS
INSERT INTO prestamos (id, estudiante_id, libro_id, fecha_salida, fecha_pactada, fecha_real, estado_prestamo, estado) VALUES
('p0000000-0000-0000-0000-000000000001', 'e0000000-0000-0000-0000-000000000001', 'b0000000-0000-0000-0000-000000000001', '2026-09-001 10:00:00', '2026-09-16 18:00:00', NULL, 'Activo', TRUE),
('p0000000-0000-0000-0000-000000000002', 'e0000000-0000-0000-0000-000000000002', 'b0000000-0000-0000-0000-000000000002', '2026-09-002 10:00:00', '2026-09-17 18:00:00', NULL, 'Activo', TRUE),
('p0000000-0000-0000-0000-000000000003', 'e0000000-0000-0000-0000-000000000003', 'b0000000-0000-0000-0000-000000000003', '2026-09-003 10:00:00', '2026-09-18 18:00:00', NULL, 'Activo', TRUE),
('p0000000-0000-0000-0000-000000000004', 'e0000000-0000-0000-0000-000000000004', 'b0000000-0000-0000-0000-000000000004', '2026-09-004 10:00:00', '2026-09-19 18:00:00', NULL, 'Activo', TRUE),
('p0000000-0000-0000-0000-000000000005', 'e0000000-0000-0000-0000-000000000005', 'b0000000-0000-0000-0000-000000000005', '2026-09-005 10:00:00', '2026-09-20 18:00:00', NULL, 'Activo', TRUE),
('p0000000-0000-0000-0000-000000000006', 'e0000000-0000-0000-0000-000000000006', 'b0000000-0000-0000-0000-000000000006', '2026-09-006 10:00:00', '2026-09-21 18:00:00', NULL, 'Activo', TRUE),
('p0000000-0000-0000-0000-000000000007', 'e0000000-0000-0000-0000-000000000007', 'b0000000-0000-0000-0000-000000000007', '2026-09-007 10:00:00', '2026-09-22 18:00:00', NULL, 'Activo', TRUE),
('p0000000-0000-0000-0000-000000000008', 'e0000000-0000-0000-0000-000000000008', 'b0000000-0000-0000-0000-000000000008', '2026-09-008 10:00:00', '2026-09-23 18:00:00', NULL, 'Activo', TRUE),
('p0000000-0000-0000-0000-000000000009', 'e0000000-0000-0000-0000-000000000009', 'b0000000-0000-0000-0000-000000000009', '2026-09-008 10:00:00', '2026-09-24 18:00:00', NULL, 'Activo', TRUE),
('p0000000-0000-0000-0000-000000000010', 'e0000000-0000-0000-0000-000000000010', 'b0000000-0000-0000-0000-000000000010', '2026-09-008 10:00:00', '2026-09-25 18:00:00', NULL, 'Activo', TRUE),
('p0000000-0000-0000-0000-000000000011', 'e0000000-0000-0000-0000-000000000011', 'b0000000-0000-0000-0000-000000000011', '2026-08-01 09:00:00', '2026-08-09 17:00:00', '2026-08-07 15:30:00', 'Devuelto', TRUE),
('p0000000-0000-0000-0000-000000000012', 'e0000000-0000-0000-0000-000000000012', 'b0000000-0000-0000-0000-000000000012', '2026-08-02 09:00:00', '2026-08-10 17:00:00', '2026-08-08 15:30:00', 'Devuelto', TRUE),
('p0000000-0000-0000-0000-000000000013', 'e0000000-0000-0000-0000-000000000013', 'b0000000-0000-0000-0000-000000000013', '2026-08-03 09:00:00', '2026-08-11 17:00:00', '2026-08-09 15:30:00', 'Devuelto', TRUE),
('p0000000-0000-0000-0000-000000000014', 'e0000000-0000-0000-0000-000000000014', 'b0000000-0000-0000-0000-000000000014', '2026-08-04 09:00:00', '2026-08-12 17:00:00', '2026-08-10 15:30:00', 'Devuelto', TRUE),
('p0000000-0000-0000-0000-000000000015', 'e0000000-0000-0000-0000-000000000015', 'b0000000-0000-0000-0000-000000000015', '2026-08-05 09:00:00', '2026-08-13 17:00:00', '2026-08-11 15:30:00', 'Devuelto', TRUE),
('p0000000-0000-0000-0000-000000000016', 'e0000000-0000-0000-0000-000000000016', 'b0000000-0000-0000-0000-000000000016', '2026-08-06 09:00:00', '2026-08-14 17:00:00', '2026-08-12 15:30:00', 'Devuelto', TRUE),
('p0000000-0000-0000-0000-000000000017', 'e0000000-0000-0000-0000-000000000017', 'b0000000-0000-0000-0000-000000000017', '2026-08-07 09:00:00', '2026-08-15 17:00:00', '2026-08-13 15:30:00', 'Devuelto', TRUE),
('p0000000-0000-0000-0000-000000000018', 'e0000000-0000-0000-0000-000000000018', 'b0000000-0000-0000-0000-000000000018', '2026-08-08 09:00:00', '2026-08-16 17:00:00', '2026-08-14 15:30:00', 'Devuelto', TRUE),
('p0000000-0000-0000-0000-000000000019', 'e0000000-0000-0000-0000-000000000019', 'b0000000-0000-0000-0000-000000000019', '2026-08-09 09:00:00', '2026-08-17 17:00:00', '2026-08-15 15:30:00', 'Devuelto', TRUE),
('p0000000-0000-0000-0000-000000000020', 'e0000000-0000-0000-0000-000000000020', 'b0000000-0000-0000-0000-000000000020', '2026-08-10 09:00:00', '2026-08-18 17:00:00', '2026-08-16 15:30:00', 'Devuelto', TRUE),
('p0000000-0000-0000-0000-000000000021', 'e0000000-0000-0000-0000-000000000021', 'b0000000-0000-0000-0000-000000000021', '2026-08-11 09:00:00', '2026-08-19 17:00:00', '2026-08-17 15:30:00', 'Devuelto', TRUE),
('p0000000-0000-0000-0000-000000000022', 'e0000000-0000-0000-0000-000000000022', 'b0000000-0000-0000-0000-000000000022', '2026-08-12 09:00:00', '2026-08-20 17:00:00', '2026-08-18 15:30:00', 'Devuelto', TRUE),
('p0000000-0000-0000-0000-000000000023', 'e0000000-0000-0000-0000-000000000023', 'b0000000-0000-0000-0000-000000000023', '2026-08-01 08:30:00', '2026-08-08 17:00:00', NULL, 'Atrasado', TRUE),
('p0000000-0000-0000-0000-000000000024', 'e0000000-0000-0000-0000-000000000024', 'b0000000-0000-0000-0000-000000000024', '2026-08-01 08:30:00', '2026-08-09 17:00:00', NULL, 'Atrasado', TRUE),
('p0000000-0000-0000-0000-000000000025', 'e0000000-0000-0000-0000-000000000025', 'b0000000-0000-0000-0000-000000000025', '2026-08-01 08:30:00', '2026-08-10 17:00:00', NULL, 'Atrasado', TRUE),
('p0000000-0000-0000-0000-000000000026', 'e0000000-0000-0000-0000-000000000026', 'b0000000-0000-0000-0000-000000000026', '2026-08-01 08:30:00', '2026-08-11 17:00:00', NULL, 'Atrasado', TRUE),
('p0000000-0000-0000-0000-000000000027', 'e0000000-0000-0000-0000-000000000027', 'b0000000-0000-0000-0000-000000000027', '2026-08-01 08:30:00', '2026-08-12 17:00:00', NULL, 'Atrasado', TRUE),
('p0000000-0000-0000-0000-000000000028', 'e0000000-0000-0000-0000-000000000028', 'b0000000-0000-0000-0000-000000000028', '2026-08-01 08:30:00', '2026-08-13 17:00:00', NULL, 'Atrasado', TRUE),
('p0000000-0000-0000-0000-000000000029', 'e0000000-0000-0000-0000-000000000029', 'b0000000-0000-0000-0000-000000000029', '2026-08-01 08:30:00', '2026-08-14 17:00:00', NULL, 'Atrasado', TRUE),
('p0000000-0000-0000-0000-000000000030', 'e0000000-0000-0000-0000-000000000030', 'b0000000-0000-0000-0000-000000000030', '2026-08-01 08:30:00', '2026-08-15 17:00:00', NULL, 'Atrasado', TRUE);
