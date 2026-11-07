import json
import os
from reportlab.pdfgen import canvas
import repositorio_archivos as repo

RUTA_JSON_EXPORT = "../reports/exportacion.json"
RUTA_PDF = "../reports/reporte_contactos.pdf"

def obtener_todos_los_contactos():
    contactos = []
    if not os.path.exists(repo.RUTA_ARCHIVO):
        return contactos
    with open(repo.RUTA_ARCHIVO, "r", encoding="utf-8") as f:
        while True:
            registro_str = f.read(repo.TAMANO_TOTAL_REGISTRO)
            if not registro_str or len(registro_str) < repo.TAMANO_TOTAL_REGISTRO:
                break
            contacto = repo.desempaquetar_contacto(registro_str)
            contactos.append(contacto)
    return contactos

def exportar_a_json():
    contactos = obtener_todos_los_contactos()
    if not contactos:
        return False, "No hay contactos guardados para exportar."
    with open(RUTA_JSON_EXPORT, "w", encoding="utf-8") as f:
        json.dump(contactos, f, indent=4, ensure_ascii=False)
    return True, f"JSON exportado en:\nreports/exportacion.json"

def generar_reporte_pdf():
    contactos = obtener_todos_los_contactos()
    if not contactos:
        return False, "No hay contactos guardados para el reporte."
    pdf = canvas.Canvas(RUTA_PDF)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 800, "REPORTE DE CONTACTOS")
    pdf.setFont("Helvetica-Bold", 10)
    y = 760
    pdf.drawString(40, y, "ID | Nombre | Teléfono | Correo | Ciudad")
    y -= 15
    pdf.line(40, y, 550, y)
    y -= 20
    pdf.setFont("Helvetica", 10)
    for c in contactos:
        texto = f"{c['id']} | {c['nombre']} | {c['telefono']} | {c['correo']} | {c['ciudad']}"
        pdf.drawString(40, y, texto)
        y -= 20
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(200, 800, "REPORTE DE CONTACTOS (Continuación)")
            pdf.setFont("Helvetica-Bold", 10)
            y = 760
            pdf.drawString(40, y, "ID | Nombre | Teléfono | Correo | Ciudad")
            y -= 15
            pdf.line(40, y, 550, y)
            y -= 20
            pdf.setFont("Helvetica", 10)
    pdf.save()
    return True, f"PDF generado en:\nreports/reporte_contactos.pdf"