import os
import hashlib
import zipfile
from datetime import datetime

RUTA_DAT = "../data/contactos.dat"
RUTA_JSON = "../data/indice.json"
RUTA_HASH = "../data/contactos.sha256"
RUTA_ZIP = "../reports/respaldo_agenda.zip"

def actualizar_hash():
    if not os.path.exists(RUTA_DAT):
        return
    sha256 = hashlib.sha256()
    with open(RUTA_DAT, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            sha256.update(bloque)
    with open(RUTA_HASH, "w") as f:
        f.write(sha256.hexdigest())

def verificar_integridad():
    if not os.path.exists(RUTA_DAT) or not os.path.exists(RUTA_HASH):
        return False, "Faltan archivos para verificar la integridad."
    with open(RUTA_HASH, "r") as f:
        hash_guardado = f.read().strip()
    sha256 = hashlib.sha256()
    with open(RUTA_DAT, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            sha256.update(bloque)
    hash_actual = sha256.hexdigest()
    if hash_actual == hash_guardado:
        return True, "Integridad verificada: El archivo NO ha sido alterado."
    else:
        return False, "¡ALERTA! El archivo fue modificado fuera de la aplicación."


def crear_respaldo_zip():
    archivos_a_respaldar = [RUTA_DAT, RUTA_JSON]
    tamano_original = 0
    with zipfile.ZipFile(RUTA_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for ruta in archivos_a_respaldar:
            if os.path.exists(ruta):
                tamano_original += os.path.getsize(ruta)
                zipf.write(ruta, arcname=os.path.basename(ruta))
    if tamano_original == 0:
        return False, "No hay archivos para respaldar."
    tamano_zip = os.path.getsize(RUTA_ZIP)
    resumen = (f"Respaldo creado en reports/respaldo_agenda.zip\n"
               f"Tamaño original: {tamano_original} bytes\n"
               f"Tamaño comprimido: {tamano_zip} bytes")
    return True, resumen

def obtener_metadatos():
    if not os.path.exists(RUTA_DAT):
        return "El archivo de contactos no existe aún."
    datos = os.stat(RUTA_DAT)
    tamano = datos.st_size
    fecha_mod = datetime.fromtimestamp(datos.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    permiso_lectura = "Sí" if os.access(RUTA_DAT, os.R_OK) else "No"
    permiso_escritura = "Sí" if os.access(RUTA_DAT, os.W_OK) else "No"
    info = (f"Archivo: contactos.dat\n"
            f"Tamaño: {tamano} bytes\n"
            f"Última modificación: {fecha_mod}\n"
            f"Permiso Lectura: {permiso_lectura}\n"
            f"Permiso Escritura: {permiso_escritura}")
    return info