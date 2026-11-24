SELECT 'usuarios' AS tabla, COUNT(*) AS cantidad FROM usuarios
UNION ALL
SELECT 'categoria', COUNT(*) FROM categoria
UNION ALL
SELECT 'vulnerabilidades', COUNT(*) FROM vulnerabilidades
UNION ALL
SELECT 'mitigaciones', COUNT(*) FROM mitigaciones
UNION ALL
SELECT 'logs_consulta', COUNT(*) FROM logs_consulta;