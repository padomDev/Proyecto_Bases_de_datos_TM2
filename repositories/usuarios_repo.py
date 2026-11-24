from config.conexion import conectar_db, cerrar_conexion

def get_usuarios_repo():
    conexion = conectar_db()

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT id, nombre_usuario, salt, password_hash FROM usuarios"
        )

        usuarios = cursor.fetchall()

        return [dict(usuario) for usuario in usuarios]

    finally:
        cerrar_conexion(conexion)

def buscar_usuario(usuario):
    conexion = conectar_db()

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE nombre_usuario = ?",
            (usuario,)
        )

        resultado = cursor.fetchone()

        if resultado is None:
            return None

        return dict(resultado)

    finally:
        cerrar_conexion(conexion)

def registrar_usuario_repo(usuario, contraseña_hasheada, salt):
    conexion = conectar_db()

    try:
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO usuarios (
            nombre_usuario,
            salt, 
            password_hash
            )
            VALUES (?, ?, ?)
            """,    
            (usuario, salt, contraseña_hasheada)
        )

        conexion.commit()

        return cursor.lastrowid

    finally:
        cerrar_conexion(conexion)
