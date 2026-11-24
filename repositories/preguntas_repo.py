from config.conexion import conectar_db, cerrar_conexion


def obtener_pregunta_aleatoria_repo():
    conexion = conectar_db()

    try:
        cursor = conexion.cursor()

        # Obtener una pregunta aleatoria
        cursor.execute("""
            SELECT id, enunciado
            FROM preguntas
            ORDER BY RANDOM()
            LIMIT 1
        """)

        pregunta = cursor.fetchone()

        if pregunta is None:
            return None

        # Obtener las respuestas de esa pregunta
        cursor.execute("""
            SELECT id, texto
            FROM respuestas
            WHERE id_pregunta = ?
            ORDER BY id
            """, 
            (pregunta["id"],)
            )

        respuestas = cursor.fetchall()

        return {
            "id": pregunta["id"],
            "pregunta": pregunta["enunciado"],
            "respuestas": [dict(respuesta) for respuesta in respuestas]
        }

    finally:
        cerrar_conexion(conexion)

def verificar_respuesta_repo(id_pregunta, id_respuesta):
    conexion = conectar_db()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT es_correcta
            FROM respuestas
            WHERE id_pregunta = ? AND id = ?
            """,
            (id_pregunta, id_respuesta)
        )

        respuesta = cursor.fetchone()

        if respuesta is None:
            return False

        return respuesta["es_correcta"] == 1

    finally:
        cerrar_conexion(conexion)