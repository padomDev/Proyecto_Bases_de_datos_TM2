PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- Usuarios de demostracion.
-- Credenciales de prueba:
--   DemoUser1 / ClaveDemo1!
--   DemoUser2 / ClaveDemo2!
--   DemoUser3 / ClaveDemo3!
--   DemoUser4 / ClaveDemo4!
--   DemoUser5 / ClaveDemo5!
-- Los hashes fueron generados con hash_casero_16_bytes_login usando el salt
-- almacenado en cada fila. INSERT OR IGNORE evita sobrescribir usuarios que
-- ya existan con el mismo nombre.
INSERT OR IGNORE INTO usuarios (nombre_usuario, salt, password_hash) VALUES
('DemoUser1', 'DemoSalt00000001', '1783cf49cfbf99bccf1e6dbc0b5aa9df'),
('DemoUser2', 'DemoSalt00000002', '5e11a46532698af44ee47a10a63cd236'),
('DemoUser3', 'DemoSalt00000003', 'a59f798195137b2ccdaa8764411efb8d'),
('DemoUser4', 'DemoSalt00000004', 'ec2d4e9df8bd6c644c7094b8dc0024e4'),
('DemoUser5', 'DemoSalt00000005', '33bb23b95b675d9ccb36a10c77e24d3b');

-- Datos iniciales del catalogo.

INSERT OR IGNORE INTO categoria (id, nombre, descripcion) VALUES
(1, 'Ejecucion remota de codigo', 'Fallas que pueden permitir la ejecucion de instrucciones no autorizadas.'),
(2, 'Denegacion de servicio', 'Fallas que afectan la disponibilidad de un servicio o sistema.'),
(3, 'Escalada de privilegios', 'Fallas que posibilitan obtener permisos superiores a los previstos.'),
(4, 'Inyeccion', 'Fallas por tratamiento inseguro de entradas y comandos.'),
(5, 'Divulgacion de informacion', 'Fallas que pueden exponer informacion sensible.');

INSERT OR IGNORE INTO vulnerabilidades (
    id, nombre, codigo_cve, descripcion, puntuacion_cvss, severidad,
    fecha_publicacion, version_cvss, id_categoria
) VALUES
(1, 'Log4Shell', 'CVE-2021-44228', 'Ejecucion remota de codigo asociada a ciertas configuraciones vulnerables de Apache Log4j 2.', 10.0, 'Critica', '2021-12-10', '3.1', 1),
(2, 'HTTP/2 Rapid Reset', 'CVE-2023-44487', 'Denegacion de servicio mediante reinicio rapido de flujos HTTP/2.', 7.5, 'Alta', '2023-10-10', '3.1', 2),
(3, 'PrintNightmare', 'CVE-2021-34527', 'Ejecucion remota de codigo en el servicio de impresion de Windows.', 8.8, 'Alta', '2021-07-02', '3.1', 1),
(4, 'EternalBlue', 'CVE-2017-0144', 'Ejecucion remota de codigo en implementaciones vulnerables de SMBv1 de Windows.', 8.8, 'Alta', '2017-03-14', '3.1', 1),
(5, 'Spring4Shell', 'CVE-2022-22965', 'Ejecucion remota de codigo bajo condiciones especificas de Spring Framework.', 9.8, 'Critica', '2022-03-31', '3.1', 1);

INSERT OR IGNORE INTO mitigaciones (
    id, descripcion, tipo_mitigacion, prioridad, id_vulnerabilidad
) VALUES
(1, 'Actualizar Apache Log4j a una version corregida segun el proveedor.', 'Parche', 'Alta', 1),
(2, 'Identificar componentes que incluyen log4j-core y actualizar sus dependencias.', 'Inventario', 'Alta', 1),
(3, 'Actualizar servidores y proxies HTTP/2 con correcciones del fabricante.', 'Parche', 'Alta', 2),
(4, 'Aplicar limites de concurrencia y protecciones de tasa en HTTP/2 cuando corresponda.', 'Configuracion', 'Media', 2),
(5, 'Instalar actualizaciones de seguridad de Windows para el servicio Print Spooler.', 'Parche', 'Alta', 3),
(6, 'Deshabilitar Print Spooler donde no sea necesario.', 'Configuracion', 'Media', 3),
(7, 'Aplicar las actualizaciones de seguridad de Microsoft para SMB.', 'Parche', 'Alta', 4),
(8, 'Deshabilitar SMBv1 en equipos que no lo requieran.', 'Configuracion', 'Alta', 4),
(9, 'Actualizar Spring Framework a una version corregida.', 'Parche', 'Alta', 5),
(10, 'Revisar las condiciones de despliegue afectadas y aplicar las recomendaciones del fabricante.', 'Revision', 'Media', 5);

INSERT OR IGNORE INTO preguntas (id, enunciado) VALUES
(1, '¿Qué es un firewall?'),
(2, '¿Para qué sirve el hashing de contraseñas?'),
(3, '¿Qué es un salt en hashing de contraseñas?'),
(4, '¿Qué significa phishing?'),
(5, '¿Qué es la autenticación multifactor?');

INSERT OR IGNORE INTO respuestas (id, id_pregunta, texto, es_correcta) VALUES
(1, 1, 'Un programa para editar imágenes', 0),
(2, 1, 'Una barrera que filtra tráfico de red', 1),
(3, 1, 'Un virus informático', 0),
(4, 1, 'Un tipo de memoria RAM', 0),
(5, 2, 'Para guardar la contraseña en texto claro', 0),
(6, 2, 'Para convertir la contraseña en un valor no reversible', 1),
(7, 2, 'Para hacer la contraseña más corta', 0),
(8, 2, 'Para enviarla por email', 0),
(9, 3, 'Un dato aleatorio que se suma antes de hashear', 1),
(10, 3, 'Una contraseña temporal', 0),
(11, 3, 'Un tipo de virus', 0),
(12, 3, 'Una copia de seguridad', 0),
(13, 4, 'Un ataque para engañar al usuario y robar información', 1),
(14, 4, 'Un tipo de antivirus', 0),
(15, 4, 'Una forma de comprimir archivos', 0),
(16, 4, 'Un protocolo de red', 0),
(17, 5, 'Utilizar varias contraseñas para una misma cuenta', 0),
(18, 5, 'Cambiar la contraseña periódicamente', 0),
(19, 5, 'Verificar la identidad mediante dos o más factores diferentes', 1),
(20, 5, 'Iniciar sesión desde varios dispositivos simultáneamente', 0);

-- Logs de demostracion. Como logs no posee una restriccion UNIQUE que permita
-- descartar duplicados por si sola, cada INSERT OR IGNORE se complementa con
-- NOT EXISTS. De esta forma el script puede ejecutarse repetidamente sin
-- duplicar los eventos ni sobrescribir informacion existente.
INSERT OR IGNORE INTO logs (fecha_hora, tipo_evento, id_usuario)
SELECT '2026-11-20 09:00:00', 'REGISTRO', u.id
FROM usuarios AS u
WHERE u.nombre_usuario = 'DemoUser1'
  AND NOT EXISTS (
      SELECT 1 FROM logs AS l
      WHERE l.fecha_hora = '2026-11-20 09:00:00'
        AND l.tipo_evento = 'REGISTRO'
        AND l.id_usuario = u.id
  );

INSERT OR IGNORE INTO logs (fecha_hora, tipo_evento, id_usuario)
SELECT '2026-11-20 09:05:00', 'REGISTRO', u.id
FROM usuarios AS u
WHERE u.nombre_usuario = 'DemoUser2'
  AND NOT EXISTS (
      SELECT 1 FROM logs AS l
      WHERE l.fecha_hora = '2026-11-20 09:05:00'
        AND l.tipo_evento = 'REGISTRO'
        AND l.id_usuario = u.id
  );

INSERT OR IGNORE INTO logs (fecha_hora, tipo_evento, id_usuario)
SELECT '2026-11-20 09:10:00', 'REGISTRO', u.id
FROM usuarios AS u
WHERE u.nombre_usuario = 'DemoUser3'
  AND NOT EXISTS (
      SELECT 1 FROM logs AS l
      WHERE l.fecha_hora = '2026-11-20 09:10:00'
        AND l.tipo_evento = 'REGISTRO'
        AND l.id_usuario = u.id
  );

INSERT OR IGNORE INTO logs (fecha_hora, tipo_evento, id_usuario)
SELECT '2026-11-20 09:15:00', 'REGISTRO', u.id
FROM usuarios AS u
WHERE u.nombre_usuario = 'DemoUser4'
  AND NOT EXISTS (
      SELECT 1 FROM logs AS l
      WHERE l.fecha_hora = '2026-11-20 09:15:00'
        AND l.tipo_evento = 'REGISTRO'
        AND l.id_usuario = u.id
  );

INSERT OR IGNORE INTO logs (fecha_hora, tipo_evento, id_usuario)
SELECT '2026-11-20 09:20:00', 'REGISTRO', u.id
FROM usuarios AS u
WHERE u.nombre_usuario = 'DemoUser5'
  AND NOT EXISTS (
      SELECT 1 FROM logs AS l
      WHERE l.fecha_hora = '2026-11-20 09:20:00'
        AND l.tipo_evento = 'REGISTRO'
        AND l.id_usuario = u.id
  );

INSERT OR IGNORE INTO logs (fecha_hora, tipo_evento, id_usuario)
SELECT '2026-11-20 10:00:00', 'LOGIN', u.id
FROM usuarios AS u
WHERE u.nombre_usuario = 'DemoUser1'
  AND NOT EXISTS (
      SELECT 1 FROM logs AS l
      WHERE l.fecha_hora = '2026-11-20 10:00:00'
        AND l.tipo_evento = 'LOGIN'
        AND l.id_usuario = u.id
  );

INSERT OR IGNORE INTO logs (
    fecha_hora, tipo_evento, id_usuario, id_vulnerabilidad
)
SELECT '2026-11-20 10:05:00', 'VULNERABILIDAD', u.id, v.id
FROM usuarios AS u
JOIN vulnerabilidades AS v ON v.codigo_cve = 'CVE-2021-44228'
WHERE u.nombre_usuario = 'DemoUser2'
  AND NOT EXISTS (
      SELECT 1 FROM logs AS l
      WHERE l.fecha_hora = '2026-11-20 10:05:00'
        AND l.tipo_evento = 'VULNERABILIDAD'
        AND l.id_usuario = u.id
        AND l.id_vulnerabilidad = v.id
  );

INSERT OR IGNORE INTO logs (
    fecha_hora, tipo_evento, id_usuario, id_mitigacion
)
SELECT '2026-11-20 10:10:00', 'MITIGACION', u.id, m.id
FROM usuarios AS u
JOIN mitigaciones AS m
    ON m.id = 1
WHERE u.nombre_usuario = 'DemoUser3'
  AND NOT EXISTS (
      SELECT 1 FROM logs AS l
      WHERE l.fecha_hora = '2026-11-20 10:10:00'
        AND l.tipo_evento = 'MITIGACION'
        AND l.id_usuario = u.id
        AND l.id_mitigacion = m.id
  );

COMMIT;
