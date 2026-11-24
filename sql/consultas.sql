-- 1. Consulta de una tabla
SELECT nombre, codigo_cve, severidad, puntuacion_cvss
FROM vulnerabilidades;

-- 2. Vulnerabilidades con su categoria
SELECT
    v.nombre AS vulnerabilidad,
    c.nombre AS categoria
FROM vulnerabilidades v
INNER JOIN categoria c ON v.id_categoria = c.id;

-- 3. Vulnerabilidades con sus mitigaciones
SELECT
    v.nombre AS vulnerabilidad,
    m.descripcion AS mitigacion
FROM vulnerabilidades v
INNER JOIN mitigaciones m ON v.id = m.id_vulnerabilidad;

-- 4. Logs con el nombre del usuario
SELECT
    l.fecha_hora,
    l.tipo_evento,
    u.nombre_usuario
FROM logs l
INNER JOIN usuarios u ON l.id_usuario = u.id;

-- 5. Logs con la vulnerabilidad o mitigacion consultada
SELECT
    l.fecha_hora,
    l.tipo_evento,
    u.nombre_usuario,
    v.nombre AS vulnerabilidad,
    m.descripcion AS mitigacion
FROM logs l
INNER JOIN usuarios u ON l.id_usuario = u.id
LEFT JOIN vulnerabilidades v ON l.id_vulnerabilidad = v.id
LEFT JOIN mitigaciones m ON l.id_mitigacion = m.id;

-- 6. Ejemplos de INSERT, SELECT, UPDATE y DELETE
-- Los cambios se deshacen al final
BEGIN TRANSACTION;

-- INSERT
INSERT INTO categoria (nombre, descripcion)
VALUES ('Categoria de prueba', 'Registro usado para probar CRUD');

-- SELECT
SELECT *
FROM categoria
WHERE nombre = 'Categoria de prueba';

-- UPDATE
UPDATE categoria
SET descripcion = 'Registro de prueba actualizado'
WHERE nombre = 'Categoria de prueba';

-- DELETE
DELETE FROM categoria
WHERE nombre = 'Categoria de prueba';

-- 7. UPDATE sobre todos los registros de una columna
UPDATE vulnerabilidades
SET version_cvss = version_cvss || '-PRUEBA';

ROLLBACK;

-- 8. Informe tabular de vulnerabilidades
SELECT
    nombre,
    codigo_cve,
    severidad,
    puntuacion_cvss
FROM vulnerabilidades;

-- 9. Informe resumen por categoria
SELECT
    c.nombre AS categoria,
    COUNT(v.id) AS cantidad
FROM categoria c
LEFT JOIN vulnerabilidades v ON c.id = v.id_categoria
GROUP BY c.id, c.nombre;

-- 10. Informe detalle
SELECT
    v.nombre AS vulnerabilidad,
    c.nombre AS categoria,
    m.descripcion AS mitigacion
FROM vulnerabilidades v
INNER JOIN categoria c ON v.id_categoria = c.id
LEFT JOIN mitigaciones m ON v.id = m.id_vulnerabilidad;

-- 11. Informe comparativo por severidad
SELECT
    severidad,
    COUNT(*) AS cantidad,
    ROUND(AVG(puntuacion_cvss), 2) AS promedio_cvss
FROM vulnerabilidades
GROUP BY severidad;
