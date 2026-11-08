from nicegui import ui
from interfaz import AgendaUI

def iniciar_aplicacion():
    app = AgendaUI()
    app.construir_interfaz()

iniciar_aplicacion()

ui.run(title="Agenda URL", native=True, port=0, window_size=(1200, 800), reload=False)