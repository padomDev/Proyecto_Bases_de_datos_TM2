
PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- ======================================
-- 1. USUARIOS
-- ======================================
-- Credenciales ficticias para probar la BD.
-- Los hashes y salts NO sirven para iniciar sesión.

INSERT INTO usuarios
(id, nombre_usuario, salt, password_hash)
VALUES
(1, 'Usuario1', 'salt_prueba_01', 'hash_prueba_01'),
(2, 'Usuario2', 'salt_prueba_02', 'hash_prueba_02'),
(3, 'Usuario3', 'salt_prueba_03', 'hash_prueba_03'),
(4, 'Usuario4', 'salt_prueba_04', 'hash_prueba_04'),
(5, 'Usuario5', 'salt_prueba_05', 'hash_prueba_05');


-- ======================================
-- 2. CATEGORIAS
-- ======================================

INSERT INTO categoria
(id, nombre, descripcion)
VALUES
(1, 'Ejecucion remota',
 'Permite ejecutar codigo en un sistema vulnerable.'),

(2, 'Denegacion de servicio',
 'Afecta la disponibilidad de un servicio.'),

(3, 'Escalada de privilegios',
 'Permite obtener permisos superiores.'),

(4, 'Inyeccion',
 'Permite introducir entradas maliciosas.'),

(5, 'Divulgacion de informacion',
 'Puede exponer informacion sensible.');


-- ======================================
-- 3. VULNERABILIDADES
-- ======================================
-- CVE reales con valores de prueba ilustrativos.
-- Las puntuaciones deben verificarse antes
-- de usar estos datos como referencia tecnica.

INSERT INTO vulnerabilidades
(id, nombre, codigo_cve, descripcion,
 puntuacion_cvss, severidad,
 fecha_publicacion, version_cvss, id_categoria)
VALUES
(1, 'Log4Shell', 'CVE-2021-44228',
 'Ejecucion remota de codigo en Apache Log4j.',
 10.0, 'Critica', '2021-12-10', '3.1', 1),

(2, 'HTTP2 Rapid Reset', 'CVE-2023-44487',
 'Denegacion de servicio mediante solicitudes HTTP2.',
 7.5, 'Alta', '2023-10-10', '3.1', 2),

(3, 'PrintNightmare', 'CVE-2021-34527',
 'Ejecucion remota de codigo en Windows Print Spooler.',
 8.8, 'Alta', NULL, '3.1', 1),

(4, 'EternalBlue', 'CVE-2017-0144',
 'Vulnerabilidad de ejecucion remota mediante SMB.',
 8.1, 'Alta', NULL, '3.1', 1),

(5, 'Spring4Shell', 'CVE-2022-22965',
 'Ejecucion remota de codigo en Spring Framework.',
 9.8, 'Critica', NULL, '3.1', 1);


-- ======================================
-- 4. MITIGACIONES
-- ======================================

INSERT INTO mitigaciones
(id, descripcion, tipo_mitigacion,
 prioridad, id_vulnerabilidad)
VALUES
(1, 'Actualizar Apache Log4j a una version corregida.',
 'Parche', 'Alta', 1),

(2, 'Actualizar los servidores HTTP2 vulnerables.',
 'Parche', 'Alta', 2),

(3, 'Instalar las actualizaciones de seguridad de Windows.',
 'Parche', 'Alta', 3),

(4, 'Aplicar parches de SMB y deshabilitar SMBv1.',
 'Configuracion', 'Alta', 4),

(5, 'Actualizar Spring Framework a una version corregida.',
 'Parche', 'Alta', 5);


-- ======================================
-- 5. LOGS_CONSULTA
-- ======================================

INSERT INTO logs_consulta
(id, id_usuario, id_vulnerabilidad,
 id_mitigacion, fecha_hora)
VALUES
(1, 1, 1, NULL, '2026-11-05 10:00:00'),
(2, 1, NULL, 1, '2026-11-05 10:05:00'),
(3, 2, 3, NULL, '2026-11-05 11:00:00'),
(4, 3, NULL, 4, '2026-11-05 12:30:00'),
(5, 4, 5, NULL, '2026-11-05 14:00:00');

COMMIT;
