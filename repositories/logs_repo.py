from config.conexion import conectar_db, cerrar_conexion

def get_logs_repo(dias):
    conexion = conectar_db()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
                        SELECT * 
                        FROM logs 
                        WHERE fecha_hora >= datetime('now', ?)
                        ORDER BY fecha_hora DESC
                        """,
                        (f"-{dias} days",)
                        )

        logs = cursor.fetchall()

        return [dict(fila) for fila in logs]

    finally:
        cerrar_conexion(conexion)

def log_login_repo(id_usuario):
    conexion = conectar_db()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
                        INSERT INTO logs (tipo_evento, id_usuario)
                        VALUES ('LOGIN', ?)
                        """,
                        (id_usuario,)
                        )

        conexion.commit()

        return cursor.lastrowid

    finally:
        cerrar_conexion(conexion)

def log_registro_repo(id_usuario):
    conexion = conectar_db()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
                        INSERT INTO logs (tipo_evento, id_usuario)
                        VALUES ('REGISTRO', ?)
                        """,
                        (id_usuario,)
                        )
                        
        conexion.commit()

        return cursor.lastrowid

    finally:
        cerrar_conexion(conexion)        

def log_vulnerabilidad_repo(id_usuario, id_vulnerabilidad):
    conexion = conectar_db()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
                        INSERT INTO logs (tipo_evento, id_usuario, id_vulnerabilidad)
                        VALUES ('VULNERABILIDAD', ?, ?)
                        """,
                        (id_usuario, id_vulnerabilidad),
                        )
                        
        conexion.commit()

        return cursor.lastrowid

    finally:
        cerrar_conexion(conexion)

def log_mitigacion_repo(id_usuario, id_mitigacion):
    conexion = conectar_db()

    try:
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO logs (tipo_evento, id_usuario, id_mitigacion)
            VALUES ('MITIGACION', ?, ?)
            """,
            (id_usuario, id_mitigacion)
        )

        conexion.commit()

        return cursor.lastrowid

    finally:
        cerrar_conexion(conexion)
