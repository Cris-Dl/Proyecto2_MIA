import json
import os

RUTA_INDICE = "../data/indice.json"

def cargar_indice():
    if os.path.exists(RUTA_INDICE):
        with open(RUTA_INDICE, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    return {}

def guardar_indice(indice):
    with open(RUTA_INDICE, "w", encoding="utf-8") as archivo:
        json.dump(indice, archivo, indent=4)


def actualizar_indice(id_contacto, numero_registro):
    indice = cargar_indice()
    indice[str(id_contacto)] = numero_registro
    guardar_indice(indice)

def buscar_en_indice(id_contacto):
    indice = cargar_indice()
    id_str = str(id_contacto)

    if id_str in indice:
        return indice[id_str]
    return None