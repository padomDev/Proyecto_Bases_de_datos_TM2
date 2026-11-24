
-- 1. USUARIOS
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER          PRIMARY KEY AUTOINCREMENT,
    nombre_usuario      VARCHAR(50) NOT NULL UNIQUE,
    salt                VARCHAR(100) NOT NULL,
    password_hash       VARCHAR(255) NOT NULL
);

-- 2. PREGUNTAS
CREATE TABLE IF NOT EXISTS preguntas (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    enunciado           TEXT NOT NULL
);

-- 3. RESPUSTAS
CREATE TABLE IF NOT EXISTS respuestas (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pregunta         INTEGER NOT NULL,
    texto               TEXT NOT NULL,
    es_correcta         INTEGER NOT NULL DEFAULT 0
        CHECK (es_correcta IN (0, 1)),

    FOREIGN KEY (id_pregunta)
        REFERENCES preguntas(id)
);

-- 4. CATEGORIAS
CREATE TABLE IF NOT EXISTS categoria (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre              VARCHAR(100) NOT NULL UNIQUE,
    descripcion         TEXT NOT NULL
);

-- 5. VULNERABILIDADES
CREATE TABLE IF NOT EXISTS vulnerabilidades (
    id INTEGER          PRIMARY KEY AUTOINCREMENT,
    nombre              VARCHAR(100) NOT NULL,
    codigo_cve          VARCHAR(25) NOT NULL UNIQUE,
    descripcion         TEXT NOT NULL,
    puntuacion_cvss     REAL NOT NULL
        CHECK (puntuacion_cvss BETWEEN 0 AND 10),
    severidad           VARCHAR(20) NOT NULL
        CHECK (severidad IN ('Baja', 'Media', 'Alta', 'Critica')),
    fecha_publicacion   DATE,
    version_cvss        VARCHAR(10) NOT NULL,
    id_categoria        INTEGER NOT NULL,

    FOREIGN KEY (id_categoria)
        REFERENCES categoria(id)
);

-- 6. MITIGACIONES
CREATE TABLE IF NOT EXISTS mitigaciones (
    id INTEGER          PRIMARY KEY AUTOINCREMENT,
    descripcion         TEXT NOT NULL,
    tipo_mitigacion     VARCHAR(50) NOT NULL,
    prioridad           VARCHAR(10) NOT NULL
        CHECK (prioridad IN ('Baja', 'Media', 'Alta')),
    id_vulnerabilidad   INTEGER NOT NULL,

    FOREIGN KEY (id_vulnerabilidad)
        REFERENCES vulnerabilidades(id)
);

-- 7. LOGS
CREATE TABLE IF NOT EXISTS logs (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_hora          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo_evento         TEXT NOT NULL
        CHECK (tipo_evento IN ('REGISTRO', 'LOGIN', 'VULNERABILIDAD', 'MITIGACION')),
    id_usuario          INTEGER NOT NULL,
    id_vulnerabilidad   INTEGER,
    id_mitigacion       INTEGER,

    FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id),

    FOREIGN KEY (id_vulnerabilidad)
        REFERENCES vulnerabilidades(id),

    FOREIGN KEY (id_mitigacion)
        REFERENCES mitigaciones(id),

    CHECK (
        (tipo_evento IN ('REGISTRO', 'LOGIN')
            AND id_vulnerabilidad IS NULL
            AND id_mitigacion IS NULL)
        OR
        (tipo_evento = 'VULNERABILIDAD'
            AND id_vulnerabilidad IS NOT NULL
            AND id_mitigacion IS NULL)
        OR
        (tipo_evento = 'MITIGACION'
            AND id_vulnerabilidad IS NULL
            AND id_mitigacion IS NOT NULL)
    )
);
