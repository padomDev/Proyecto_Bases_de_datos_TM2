from config.conexion import conectar_db, cerrar_conexion

def get_vulnerabilidades_repo():
    conexion = conectar_db()

    try:
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vulnerabilidades")

        vulnerabilidades = cursor.fetchall()

        return [dict(fila) for fila in vulnerabilidades]

    finally:
        cerrar_conexion(conexion)

def get_mitigaciones_repo(id_vulnerabilidad):
    conexion = conectar_db()

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM mitigaciones WHERE id_vulnerabilidad = ?",
            (id_vulnerabilidad,)
        )

        mitigaciones = cursor.fetchall()

        return [dict(fila) for fila in mitigaciones]

    finally:
        cerrar_conexion(conexion)
