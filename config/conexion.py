import os
import sqlite3
import sys
from pathlib import Path

NOMBRE_APLICACION = "ProyectoCiberseguridad"
RUTA_PROYECTO = Path(__file__).resolve().parent.parent


def obtener_ruta_recursos():
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)

    return RUTA_PROYECTO


def obtener_directorio_datos():
    directorio_configurado = os.getenv("PROYECTO_CIBERSEGURIDAD_DATOS")

    if directorio_configurado:
        return Path(directorio_configurado)

    # Durante el desarrollo se conserva la base dentro del proyecto.
    if not getattr(sys, "frozen", False):
        return Path(__file__).resolve().parent

    # En el ejecutable la base se guarda fuera del paquete temporal.
    if sys.platform == "win32":
        base = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.getenv("XDG_DATA_HOME", Path.home() / ".local" / "share"))

    return base / NOMBRE_APLICACION


RUTA_RECURSOS = obtener_ruta_recursos()
RUTA_DB = obtener_directorio_datos() / "app.db"
RUTA_ESQUEMA = RUTA_RECURSOS / "sql" / "crear_tablas.sql"
RUTA_DATOS = RUTA_RECURSOS / "sql" / "insertar_datos.sql"


# Establece la conexión con SQLite.
def conectar_db():
    RUTA_DB.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory = sqlite3.Row
    configurar_conexion(conexion)
    return conexion


# Crea las tablas y carga los datos iniciales de forma idempotente.
def inicializar_db():
    conexion = conectar_db()

    try:
        conexion.executescript(RUTA_ESQUEMA.read_text(encoding="utf-8"))
        conexion.executescript(RUTA_DATOS.read_text(encoding="utf-8"))
    finally:
        cerrar_conexion(conexion)


# Configura la conexión con la base de datos.
def configurar_conexion(conexion):
    conexion.execute("PRAGMA foreign_keys = ON")


# Cierra una conexión abierta.
def cerrar_conexion(conexion):
    if conexion is not None:
        conexion.close()
