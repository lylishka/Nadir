USE nadir;

-- ===========================================
-- AVENTURAS
-- ===========================================
INSERT INTO aventura (id_aventura, nombre, descripcion) VALUES
(1, 'Curtain Call: Zero', 'Terror surrealista en un teatro infinito donde la identidad y la percepción se fragmentan.'),
(2, 'Protocolo Epsilon', 'Ciencia ficción psicológica a bordo de una nave controlada por una IA ambigua.');

-- ===========================================
-- PERSONAJES
-- ===========================================
INSERT INTO personaje (id_personaje, nombre, descripcion) VALUES
-- Curtain Call
(1, 'El Actor', 'Engaño social, máscaras, imitación.'),
(2, 'La Violinista', 'Oído absoluto, sigilo y control del ritmo.'),
(3, 'El Escenógrafo', 'Mecanismos, fuerza y estructuras.'),
-- Protocolo Epsilon
(4, 'Ingeniero', 'Reparaciones técnicas y sistemas.'),
(5, 'Médico', 'Curación y análisis biológico.'),
(6, 'Soldado', 'Combate y seguridad.');

-- ===========================================
-- PREGUNTAS
-- ===========================================
-- Curtain Call: Zero
INSERT INTO pregunta (texto) VALUES
('La máscara oprime tu rostro. ¿Qué decides hacer para sobrevivir al teatro?'),
('Los maniquíes te imitan. ¿Cómo reaccionas ante su movimiento sincronizado?'),
('Un maniquí se acerca lentamente. ¿Qué acción tomas?'),
('El Director ofrece un pacto misterioso. ¿Aceptas sus términos?'),
('El escenario se despliega a tu alrededor. ¿Cómo lo enfrentas?'),
('El caos alcanza su punto máximo, tu destino se sella.'),
('El teatro colapsa y tú decides tu última acción.');

-- Protocolo Epsilon
INSERT INTO pregunta (texto) VALUES
('Las luces fallan y la IA solicita una decisión crítica. ¿Cómo procedes?'),
('La IA bloquea los sistemas de navegación. ¿Qué haces?'),
('Un miembro de la tripulación cuestiona tus órdenes. ¿Cómo respondes?'),
('La nave enfrenta un dilema ético. ¿Confías en la IA o actúas por tu cuenta?'),
('Se aproxima un salto al hiperespacio. ¿Qué decisión tomas?'),
('El salto se completa o fracasa según tu elección.'),
('Tu destino final queda sellado en el vacío del espacio.');

-- ===========================================
-- OPCIONES
-- ===========================================
-- Curtain Call: Zero
INSERT INTO opcion
(id_opcion, id_pregunta_base, id_pregunta_siguiente, texto, id_personaje_especifico, probabilidad_base, probabilidad_fuera_clase)
VALUES
(NULL, 1, 2, 'Imitar a los maniquíes', 1, 80, 30),
(NULL, 1, 2, 'Seguir el ritmo del público', 2, 90, 20),
(NULL, 1, 2, 'Manipular el decorado para crear distracción', 3, 85, 10),
(NULL, 1, 3, 'Permanecer inmóvil', NULL, NULL, NULL),
(NULL, 1, 3, 'Avanzar con cautela hacia la salida', NULL, NULL, NULL),
(NULL, 2, 4, 'Moverte cuando los maniquíes se detienen', NULL, NULL, NULL),
(NULL, 2, 5, 'Provocar un error en la coreografía', NULL, NULL, NULL),
(NULL, 3, 6, 'Colapsar el escenario a tu favor', NULL, NULL, NULL),
(NULL, 3, 7, 'Esconderte entre bastidores', NULL, NULL, NULL),
(NULL, 4, 6, 'Aceptar la máscara dorada', NULL, NULL, NULL),
(NULL, 5, 7, 'Forzar tu despertar', NULL, NULL, NULL);

-- Protocolo Epsilon
INSERT INTO opcion
(id_pregunta_base, id_pregunta_siguiente, texto, id_personaje_especifico, probabilidad_base, probabilidad_fuera_clase)
VALUES
(8, 9, 'Seguir protocolos de ingeniería', 4, 90, 30),
(8, 9, 'Analizar signos vitales de la tripulación', 5, 85, 25),
(8, 9, 'Asegurar la nave por la fuerza', 6, 90, 40),
(8, 10, 'Ignorar a la IA y actuar por tu cuenta', NULL, NULL, NULL),
(8, 10, 'Intentar negociar con la IA', NULL, NULL, NULL),
(9, 11, 'Acceder al núcleo de control', NULL, NULL, NULL),
(9, 12, 'Redirigir energía a los sistemas vitales', NULL, NULL, NULL),
(10, 12, 'Seguir las órdenes parcialmente', NULL, NULL, NULL),
(10, 13, 'Desactivar los sensores de la IA', NULL, NULL, NULL),
(11, 12, 'Confiar completamente en la IA', NULL, NULL, NULL),
(12, 13, 'Forzar un apagado de emergencia', NULL, NULL, NULL);

-- ===========================================
-- PERSONAJE_AVENTURA
-- ===========================================
INSERT INTO personaje_aventura (id_personaje, id_aventura) VALUES
(1, 1),(2, 1),(3, 1),
(4, 2),(5, 2),(6, 2);


-- ===========================================
-- PREGUNTA_AVENTURA
-- ===========================================
INSERT INTO pregunta_aventura (id_pregunta, id_aventura) VALUES
(1, 1),
(8, 2);