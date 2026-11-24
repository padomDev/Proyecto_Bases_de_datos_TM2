PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
INSERT INTO usuarios (id, nombre_usuario, salt, password_hash) VALUES (1, 'Usuario1', 'f034c2bc97a79eb8eac04adbc562b957', 'pbkdf2_sha256$600000$546d111f29592a37e23a1592dfaa89ceecd633b5ae06d77a6a1e0a3004e667e3');
INSERT INTO usuarios (id, nombre_usuario, salt, password_hash) VALUES (2, 'Usuario2', 'bcabad29c8718ed27758f4739ce58279', 'pbkdf2_sha256$600000$3982ecbdccde08069e4f2b26c50dc89a10e91d79f420a87ba18716ce7eb334d3');
INSERT INTO usuarios (id, nombre_usuario, salt, password_hash) VALUES (3, 'Usuario3', 'cf3ab19c2cfc5308760710e2197d63c3', 'pbkdf2_sha256$600000$47ff2b94dbcd320030c4288e9d03ffdca5803d69ba5bcfe165504836ab535b12');
INSERT INTO usuarios (id, nombre_usuario, salt, password_hash) VALUES (4, 'Usuario4', '0693300a3ae4c3de5c0d82dc787a5e6a', 'pbkdf2_sha256$600000$29ca3502ed835db9f3f872825e0e95c8e0ce7fe0a32756b3fec904db92527f10');
INSERT INTO usuarios (id, nombre_usuario, salt, password_hash) VALUES (5, 'Usuario5', 'e31e83c0b48af97d6dc161a10743b80b', 'pbkdf2_sha256$600000$3bbf8a5db4b106025c7f7164122ad7014efb2b07774126f19262ec45dc4fdc38');
INSERT INTO categoria (id, nombre, descripcion) VALUES (1, 'Ejecucion remota de codigo', 'Fallas que pueden permitir la ejecucion de instrucciones no autorizadas.');
INSERT INTO categoria (id, nombre, descripcion) VALUES (2, 'Denegacion de servicio', 'Fallas que afectan la disponibilidad de un servicio o sistema.');
INSERT INTO categoria (id, nombre, descripcion) VALUES (3, 'Escalada de privilegios', 'Fallas que posibilitan obtener permisos superiores a los previstos.');
INSERT INTO categoria (id, nombre, descripcion) VALUES (4, 'Inyeccion', 'Fallas por tratamiento inseguro de entradas y comandos.');
INSERT INTO categoria (id, nombre, descripcion) VALUES (5, 'Divulgacion de informacion', 'Fallas que pueden exponer informacion sensible.');
INSERT INTO vulnerabilidades (id, nombre, codigo_cve, descripcion, puntuacion_cvss, severidad, fecha_publicacion, version_cvss, id_categoria) VALUES (1, 'Log4Shell', 'CVE-2021-44228', 'Ejecucion remota de codigo asociada a ciertas configuraciones vulnerables de Apache Log4j 2.', 10.0, 'Critica', '2021-12-10', '3.1', 1);
INSERT INTO vulnerabilidades (id, nombre, codigo_cve, descripcion, puntuacion_cvss, severidad, fecha_publicacion, version_cvss, id_categoria) VALUES (2, 'HTTP/2 Rapid Reset', 'CVE-2023-44487', 'Denegacion de servicio mediante reinicio rapido de flujos HTTP/2.', 7.5, 'Alta', '2023-10-10', '3.1', 2);
INSERT INTO vulnerabilidades (id, nombre, codigo_cve, descripcion, puntuacion_cvss, severidad, fecha_publicacion, version_cvss, id_categoria) VALUES (3, 'PrintNightmare', 'CVE-2021-34527', 'Ejecucion remota de codigo en el servicio de impresion de Windows.', 8.8, 'Alta', '2021-07-02', '3.1', 1);
INSERT INTO vulnerabilidades (id, nombre, codigo_cve, descripcion, puntuacion_cvss, severidad, fecha_publicacion, version_cvss, id_categoria) VALUES (4, 'EternalBlue', 'CVE-2017-0144', 'Ejecucion remota de codigo en implementaciones vulnerables de SMBv1 de Windows.', 8.8, 'Alta', '2017-03-14', '3.1', 1);
INSERT INTO vulnerabilidades (id, nombre, codigo_cve, descripcion, puntuacion_cvss, severidad, fecha_publicacion, version_cvss, id_categoria) VALUES (5, 'Spring4Shell', 'CVE-2022-22965', 'Ejecucion remota de codigo bajo condiciones especificas de Spring Framework.', 9.8, 'Critica', '2022-03-31', '3.1', 1);
INSERT INTO mitigaciones (id, descripcion, tipo_mitigacion, prioridad, id_vulnerabilidad) VALUES (1, 'Actualizar Apache Log4j a una version corregida segun el proveedor.', 'Parche', 'Alta', 1);
INSERT INTO mitigaciones (id, descripcion, tipo_mitigacion, prioridad, id_vulnerabilidad) VALUES (2, 'Identificar componentes que incluyen log4j-core y actualizar sus dependencias.', 'Inventario', 'Alta', 1);
INSERT INTO mitigaciones (id, descripcion, tipo_mitigacion, prioridad, id_vulnerabilidad) VALUES (3, 'Actualizar servidores y proxies HTTP/2 con correcciones del fabricante.', 'Parche', 'Alta', 2);
INSERT INTO mitigaciones (id, descripcion, tipo_mitigacion, prioridad, id_vulnerabilidad) VALUES (4, 'Aplicar limites de concurrencia y protecciones de tasa en HTTP/2 cuando corresponda.', 'Configuracion', 'Media', 2);
INSERT INTO mitigaciones (id, descripcion, tipo_mitigacion, prioridad, id_vulnerabilidad) VALUES (5, 'Instalar actualizaciones de seguridad de Windows para el servicio Print Spooler.', 'Parche', 'Alta', 3);
INSERT INTO mitigaciones (id, descripcion, tipo_mitigacion, prioridad, id_vulnerabilidad) VALUES (6, 'Deshabilitar Print Spooler donde no sea necesario.', 'Configuracion', 'Media', 3);
INSERT INTO mitigaciones (id, descripcion, tipo_mitigacion, prioridad, id_vulnerabilidad) VALUES (7, 'Aplicar las actualizaciones de seguridad de Microsoft para SMB.', 'Parche', 'Alta', 4);
INSERT INTO mitigaciones (id, descripcion, tipo_mitigacion, prioridad, id_vulnerabilidad) VALUES (8, 'Deshabilitar SMBv1 en equipos que no lo requieran.', 'Configuracion', 'Alta', 4);
INSERT INTO mitigaciones (id, descripcion, tipo_mitigacion, prioridad, id_vulnerabilidad) VALUES (9, 'Actualizar Spring Framework a una version corregida.', 'Parche', 'Alta', 5);
INSERT INTO mitigaciones (id, descripcion, tipo_mitigacion, prioridad, id_vulnerabilidad) VALUES (10, 'Revisar las condiciones de despliegue afectadas y aplicar las recomendaciones del fabricante.', 'Revision', 'Media', 5);
INSERT INTO logs_consulta (id, fecha_hora, id_usuario, id_vulnerabilidad, id_mitigacion) VALUES (1, '2026-11-05 10:00:00', 1, 1, NULL);
INSERT INTO logs_consulta (id, fecha_hora, id_usuario, id_vulnerabilidad, id_mitigacion) VALUES (2, '2026-11-05 10:05:00', 1, NULL, 1);
INSERT INTO logs_consulta (id, fecha_hora, id_usuario, id_vulnerabilidad, id_mitigacion) VALUES (3, '2026-11-05 11:00:00', 2, 3, NULL);
INSERT INTO logs_consulta (id, fecha_hora, id_usuario, id_vulnerabilidad, id_mitigacion) VALUES (4, '2026-11-05 11:02:00', 2, NULL, 5);
INSERT INTO logs_consulta (id, fecha_hora, id_usuario, id_vulnerabilidad, id_mitigacion) VALUES (5, '2026-11-05 12:30:00', 3, NULL, 8);
INSERT INTO logs_consulta (id, fecha_hora, id_usuario, id_vulnerabilidad, id_mitigacion) VALUES (6, '2026-11-05 13:20:00', 3, 4, NULL);
INSERT INTO logs_consulta (id, fecha_hora, id_usuario, id_vulnerabilidad, id_mitigacion) VALUES (7, '2026-11-05 14:00:00', 4, 5, NULL);
INSERT INTO logs_consulta (id, fecha_hora, id_usuario, id_vulnerabilidad, id_mitigacion) VALUES (8, '2026-11-05 14:15:00', 4, NULL, 9);
INSERT INTO logs_consulta (id, fecha_hora, id_usuario, id_vulnerabilidad, id_mitigacion) VALUES (9, '2026-11-05 16:20:00', 5, 2, NULL);
INSERT INTO logs_consulta (id, fecha_hora, id_usuario, id_vulnerabilidad, id_mitigacion) VALUES (10, '2026-11-05 16:45:00', 5, NULL, 4);
COMMIT;


-- ========================================
-- TABLA PREGUNTAS
-- ========================================

INSERT INTO preguntas (id, enunciado)
VALUES
(1, '¿Qué es un firewall?'),
(2, '¿Para qué sirve el hashing de contraseñas?'),
(3, '¿Qué es un salt en hashing de contraseñas?'),
(4, '¿Qué significa phishing?'),
(5, '¿Qué es la autenticación multifactor?');


-- ========================================
-- TABLA RESPUESTAS
-- ========================================

-- Pregunta 1: ¿Qué es un firewall?
-- Respuesta correcta: B

INSERT INTO respuestas (id_pregunta, texto, es_correcta)
VALUES
(1, 'Un programa para editar imágenes', 0),
(1, 'Una barrera que filtra tráfico de red', 1),
(1, 'Un virus informático', 0),
(1, 'Un tipo de memoria RAM', 0);


-- Pregunta 2: ¿Para qué sirve el hashing de contraseñas?
-- Respuesta correcta: B

INSERT INTO respuestas (id_pregunta, texto, es_correcta)
VALUES
(2, 'Para guardar la contraseña en texto claro', 0),
(2, 'Para convertir la contraseña en un valor no reversible', 1),
(2, 'Para hacer la contraseña más corta', 0),
(2, 'Para enviarla por email', 0);


-- Pregunta 3: ¿Qué es un salt en hashing de contraseñas?
-- Respuesta correcta: A

INSERT INTO respuestas (id_pregunta, texto, es_correcta)
VALUES
(3, 'Un dato aleatorio que se suma antes de hashear', 1),
(3, 'Una contraseña temporal', 0),
(3, 'Un tipo de virus', 0),
(3, 'Una copia de seguridad', 0);


-- Pregunta 4: ¿Qué significa phishing?
-- Respuesta correcta: A

INSERT INTO respuestas (id_pregunta, texto, es_correcta)
VALUES
(4, 'Un ataque para engañar al usuario y robar información', 1),
(4, 'Un tipo de antivirus', 0),
(4, 'Una forma de comprimir archivos', 0),
(4, 'Un protocolo de red', 0);

-- PREGUNTA 5 :¿Qué es la autenticación multifactor?
-- Respuesta correcta: C

INSERT INTO respuestas (id_pregunta, texto, es_correcta)
VALUES
(5, 'Utilizar varias contraseñas para una misma cuenta', 0),
(5, 'Cambiar la contraseña periódicamente', 0),
(5, 'Verificar la identidad mediante dos o más factores diferentes', 1),
(5, 'Iniciar sesión desde varios dispositivos simultáneamente', 0);