import sqlite3
from pathlib import Path

RUTA_DB = Path(__file__).resolve().parent / "app.db"


# Establece la conexión con SQLite.
def conectar_db():
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory = sqlite3.Row  # NUEVA LÍNEA
    configurar_conexion(conexion)
    return conexion


# Configura la conexión con la base de datos.
def configurar_conexion(conexion):
    conexion.execute("PRAGMA foreign_keys = ON")


# Cierra una conexión abierta.
def cerrar_conexion(conexion):
    if conexion is not None:
        conexion.close()