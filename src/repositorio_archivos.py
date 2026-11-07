import os

TAMANO_ID = 10
TAMANO_NOMBRE = 40
TAMANO_TELEFONO = 15
TAMANO_CORREO = 40
TAMANO_CIUDAD = 20

TAMANO_TOTAL_REGISTRO = 126
RUTA_ARCHIVO = "../data/contactos.dat"

def formatear_campo(valor, tamano):
    valor_str = str(valor)
    return valor_str[:tamano].ljust(tamano)

def empaquetar_contacto(id_contacto, nombre, telefono, correo, ciudad):
    tam_id = formatear_campo(id_contacto, TAMANO_ID)
    tam_nombre = formatear_campo(nombre, TAMANO_NOMBRE)
    tam_tel = formatear_campo(telefono, TAMANO_TELEFONO)
    tam_correo = formatear_campo(correo, TAMANO_CORREO)
    tam_ciudad = formatear_campo(ciudad, TAMANO_CIUDAD)
    return f"{tam_id}{tam_nombre}{tam_tel}{tam_correo}{tam_ciudad}\n"

def desempaquetar_contacto(registro_str):
    return {
        "id": int(registro_str[0:10].strip()),
        "nombre": registro_str[10:50].strip(),
        "telefono": registro_str[50:65].strip(),
        "correo": registro_str[65:105].strip(),
        "ciudad": registro_str[105:125].strip()
    }

def agregar_contacto(id_contacto, nombre, telefono, correo, ciudad):
    registro = empaquetar_contacto(id_contacto, nombre, telefono, correo, ciudad)
    with open(RUTA_ARCHIVO, "a", encoding="utf-8") as f:
        byte_actual = f.tell()
        f.write(registro)
    numero_registro = byte_actual // TAMANO_TOTAL_REGISTRO
    return int(numero_registro)

def leer_contacto_directo(numero_registro):
    if not os.path.exists(RUTA_ARCHIVO):
        return None
    posicion_byte = numero_registro * TAMANO_TOTAL_REGISTRO
    with open(RUTA_ARCHIVO, "r", encoding="utf-8") as f:
        f.seek(posicion_byte)
        registro_str = f.read(TAMANO_TOTAL_REGISTRO)
        if not registro_str:
            return None
        return desempaquetar_contacto(registro_str)


def modificar_contacto(numero_registro, id_contacto, nombre, telefono, correo, ciudad):
    if not os.path.exists(RUTA_ARCHIVO):
        return False
    registro = empaquetar_contacto(id_contacto, nombre, telefono, correo, ciudad)
    posicion_byte = numero_registro * TAMANO_TOTAL_REGISTRO
    with open(RUTA_ARCHIVO, "r+", encoding="utf-8", newline='\n') as f:
        f.seek(posicion_byte)
        f.write(registro)
    return True

