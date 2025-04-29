-- Creación de la base de datos
-- CREATE DATABASE biblioteca_cendi;

-- Conexión a la base de datos
-- \c biblioteca_cendi

-- Tabla para Ciclos Escolares
CREATE TABLE ciclos_escolares (
    id_ciclo SERIAL PRIMARY KEY,
    nombre_ciclo VARCHAR(50) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL
);

-- Tabla para Alumnos
CREATE TABLE alumnos (
    id_alumno SERIAL PRIMARY KEY,
    codigo_alumno VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50) NOT NULL,
    escuela VARCHAR(100) NOT NULL DEFAULT 'CENDI IPN',
    id_ciclo INTEGER NOT NULL REFERENCES ciclos_escolares(id_ciclo)
);

-- Tabla para Editoriales
CREATE TABLE editoriales (
    id_editorial SERIAL PRIMARY KEY,
    codigo_editorial VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    direccion TEXT,
    telefono VARCHAR(20)
);

-- Tabla para Autores
CREATE TABLE autores (
    id_autor SERIAL PRIMARY KEY,
    codigo_autor VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50),
    apellido_materno VARCHAR(50),
    email VARCHAR(100)
);

-- Tabla para Especialidades
CREATE TABLE especialidades (
    id_especialidad SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Tabla para Libros
CREATE TABLE libros (
    id_libro SERIAL PRIMARY KEY,
    codigo_libro VARCHAR(20) UNIQUE NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    numero_paginas INTEGER NOT NULL,
    id_especialidad INTEGER NOT NULL REFERENCES especialidades(id_especialidad),
    id_editorial INTEGER NOT NULL REFERENCES editoriales(id_editorial)
);

-- Tabla para relación muchos a muchos entre Libros y Autores
CREATE TABLE libros_autores (
    id_libro INTEGER REFERENCES libros(id_libro),
    id_autor INTEGER REFERENCES autores(id_autor),
    PRIMARY KEY (id_libro, id_autor)
);

-- Tabla para Préstamos
CREATE TABLE prestamos (
    id_prestamo SERIAL PRIMARY KEY,
    id_alumno INTEGER REFERENCES alumnos(id_alumno),
    id_libro INTEGER REFERENCES libros(id_libro),
    fecha_prestamo DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_devolucion DATE,
    devuelto BOOLEAN DEFAULT FALSE,
    UNIQUE (id_alumno, id_libro, fecha_prestamo)
);

-- Índices para mejorar el rendimiento de búsquedas frecuentes
CREATE INDEX idx_alumno_codigo ON alumnos(codigo_alumno);
CREATE INDEX idx_libro_codigo ON libros(codigo_libro);
CREATE INDEX idx_autor_codigo ON autores(codigo_autor);
CREATE INDEX idx_editorial_codigo ON editoriales(codigo_editorial);
CREATE INDEX idx_prestamos_fechas ON prestamos(fecha_prestamo, fecha_devolucion);

-- Restricciones y reglas adicionales

-- Verificar que la fecha de devolución sea posterior a la fecha de préstamo
ALTER TABLE prestamos ADD CONSTRAINT fecha_devolucion_valida 
    CHECK (fecha_devolucion IS NULL OR fecha_devolucion >= fecha_prestamo);

-- Verificar que el número de páginas sea positivo
ALTER TABLE libros ADD CONSTRAINT paginas_positivas 
    CHECK (numero_paginas > 0);

-- Verificar que las fechas del ciclo escolar sean coherentes
ALTER TABLE ciclos_escolares ADD CONSTRAINT fechas_ciclo_validas 
    CHECK (fecha_fin >= fecha_inicio);