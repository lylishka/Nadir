USE nadir;

-- =========================
-- TABLA AVENTURA
-- =========================
CREATE TABLE aventura (
  id_aventura INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion TEXT
);

-- =========================
-- TABLA PERSONAJE
-- =========================
CREATE TABLE personaje (
  id_personaje INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE,
  descripcion TEXT
);

-- =========================
-- TABLA USUARIO
-- ========================

CREATE TABLE usuario (
	id_usuario INT AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(50) NOT NULL UNIQUE,
	password VARCHAR(255) NOT NULL
);

-- =========================
-- TABLA PASO (ESTADO NARRATIVO)
-- =========================
CREATE TABLE paso (
  id_paso INT AUTO_INCREMENT PRIMARY KEY,
  id_aventura INT NULL,
  id_juego INT NULL,
  id_usuario INT NULL,
  id_opcion INT NULL,
  
  fecha_hora DATETIME NULL,
  es_final TINYINT(1) NOT NULL DEFAULT 0,
  
  

  FOREIGN KEY (id_aventura) REFERENCES aventura(id_aventura)
);

-- =========================
-- TABLA PREGUNTA
-- =========================
CREATE TABLE pregunta (
  id_pregunta INT AUTO_INCREMENT PRIMARY KEY,
  texto TEXT NULL
  );

-- =========================
-- TABLA OPCION
-- =========================
CREATE TABLE opcion (
  id_opcion INT AUTO_INCREMENT PRIMARY KEY,

  id_pregunta_base INT NOT NULL,
  id_pregunta_siguiente INT NOT NULL,

  texto VARCHAR(255) NOT NULL,

  -- NULL = opción común
  id_personaje_especifico INT NULL,

  -- Probabilidades (0–100)
  probabilidad_base INT NULL,
  probabilidad_fuera_clase INT NULL,

  FOREIGN KEY (id_pregunta_siguiente) REFERENCES pregunta(id_pregunta),
  FOREIGN KEY (id_pregunta_base) REFERENCES pregunta(id_pregunta),
  FOREIGN KEY (id_personaje_especifico) REFERENCES personaje(id_personaje)
);
 
 -- =========================
-- TABLA PERSONAJE_AVENTURA
-- =========================
 
CREATE TABLE personaje_aventura (
	id_personaje INT,
	id_aventura INT,
	PRIMARY KEY (id_personaje, id_aventura),
	FOREIGN KEY (id_personaje) REFERENCES personaje(id_personaje),
	FOREIGN KEY (id_aventura) REFERENCES aventura(id_aventura)
);

 -- =========================
-- TABLA PREGUNTA_AVENTURA
-- =========================
 
CREATE TABLE pregunta_aventura (
	id_pregunta INT,
	id_aventura INT,
	PRIMARY KEY (id_pregunta, id_aventura),
	FOREIGN KEY (id_pregunta) REFERENCES pregunta(id_pregunta),
	FOREIGN KEY (id_aventura) REFERENCES aventura(id_aventura)
);
-- =========================
-- TABLA JUEGO
-- =========================

CREATE TABLE juego(
  id_juego INT AUTO_INCREMENT PRIMARY KEY,
  id_aventura INT NOT NULL,
  id_personaje INT NOT NULL,
  id_usuario INT NOT NULL,

  FOREIGN KEY (id_aventura) REFERENCES aventura(id_aventura),
  FOREIGN KEY (id_personaje) REFERENCES personaje(id_personaje),
  FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);




