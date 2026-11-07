from nicegui import ui
import repositorio_archivos as repo
import gestor_indice as indice
import utilidades as util
import exportador as exp

class AgendaUI:
    def __init__(self):
        self.inputs = {}
        self.dialogo_buscar = None
        self.input_buscar = None

    def construir_interfaz(self):
        with ui.header(elevated=True).classes('bg-primary items-center justify-between px-4 py-2'):
            ui.label('Agenda de Contactos - MVP').classes('text-xl font-bold')

            with ui.row().classes('gap-2'):
                with ui.button('Contactos', icon='person').classes('text-white').props('flat'):
                    with ui.menu():
                        ui.menu_item('Buscar por ID', on_click=self.abrir_busqueda)
                        ui.menu_item('Modificar actual', on_click=self.modificar_contacto)

                with ui.button('Exportar', icon='download').classes('text-white').props('flat'):
                    with ui.menu():
                        ui.menu_item('Exportar a JSON', on_click=self.accion_exportar_json)
                        ui.menu_item('Generar Reporte PDF', on_click=self.accion_generar_pdf)

                with ui.button('Herramientas', icon='build').classes('text-white').props('flat'):
                    with ui.menu():
                        ui.menu_item('Verificar Integridad SHA-256', on_click=self.accion_verificar_integridad)
                        ui.menu_item('Crear Respaldo ZIP', on_click=self.accion_respaldo_zip)
                        ui.menu_item('Información del Archivo', on_click=self.accion_info_archivo)

                with ui.button('Ayuda', icon='help').classes('text-white').props('flat'):
                    with ui.menu():
                        ui.menu_item('Acerca de...',
                                     on_click=lambda: ui.notify('Laboratorio 2 - Universidad Rafael Landívar',
                                                                type='positive'))

        with ui.card().classes('w-full max-w-md mx-auto mt-12 p-6 shadow-lg rounded-lg'):
            ui.label('Gestión de Contacto').classes('text-2xl mb-4 font-bold text-center w-full text-gray-700')

            self.inputs['id'] = ui.number('ID (Número entero)').classes('w-full mb-2')
            self.inputs['nombre'] = ui.input('Nombre').classes('w-full mb-2')
            self.inputs['telefono'] = ui.input('Teléfono').classes('w-full mb-2')
            self.inputs['correo'] = ui.input('Correo Electrónico').classes('w-full mb-2')
            self.inputs['ciudad'] = ui.input('Ciudad').classes('w-full mb-4')

            ui.button('Guardar Nuevo Contacto', on_click=self.guardar_contacto, color='positive', icon='save').classes(
                'w-full')

        with ui.dialog() as self.dialogo_buscar, ui.card().classes('w-80'):
            ui.label('Buscar Contacto').classes('text-lg font-bold mb-2')
            self.input_buscar = ui.number('Ingrese el ID a buscar').classes('w-full')
            with ui.row().classes('w-full justify-end mt-4 gap-2'):
                ui.button('Cancelar', on_click=self.dialogo_buscar.close, color='red').props('flat')
                ui.button('Buscar', on_click=self.ejecutar_busqueda, color='primary')

    def guardar_contacto(self):
        val_id = self.inputs['id'].value

        if val_id is None:
            ui.notify('El ID es obligatorio.', type='negative')
            return

        id_contacto = int(val_id)

        if indice.buscar_en_indice(id_contacto) is not None:
            ui.notify('El ID ya existe. Use la opción Modificar.', type='warning')
            return

        posicion = repo.agregar_contacto(
            id_contacto,
            self.inputs['nombre'].value or "",
            self.inputs['telefono'].value or "",
            self.inputs['correo'].value or "",
            self.inputs['ciudad'].value or ""
        )

        indice.actualizar_indice(id_contacto, posicion)

        util.actualizar_hash()

        ui.notify('Contacto guardado correctamente', type='positive')
        self.limpiar_formulario()

    def abrir_busqueda(self):
        self.input_buscar.value = None
        self.dialogo_buscar.open()

    def ejecutar_busqueda(self):
        id_buscar = self.input_buscar.value
        if id_buscar is None:
            return

        self.dialogo_buscar.close()

        numero_registro = indice.buscar_en_indice(int(id_buscar))

        if numero_registro is None:
            ui.notify(f'El ID {id_buscar} no existe.', type='negative')
            return

        contacto = repo.leer_contacto_directo(numero_registro)

        if contacto:
            self.inputs['id'].value = contacto['id']
            self.inputs['nombre'].value = contacto['nombre']
            self.inputs['telefono'].value = contacto['telefono']
            self.inputs['correo'].value = contacto['correo']
            self.inputs['ciudad'].value = contacto['ciudad']

            ui.notify('Contacto cargado. Edite los campos y seleccione "Modificar actual".', type='info')

    def modificar_contacto(self):
        val_id = self.inputs['id'].value
        if val_id is None:
            ui.notify('Cargue un contacto válido primero.', type='negative')
            return

        id_contacto = int(val_id)
        numero_registro = indice.buscar_en_indice(id_contacto)

        if numero_registro is None:
            ui.notify('No se puede modificar un ID que no existe.', type='negative')
            return

        exito = repo.modificar_contacto(
            numero_registro,
            id_contacto,
            self.inputs['nombre'].value or "",
            self.inputs['telefono'].value or "",
            self.inputs['correo'].value or "",
            self.inputs['ciudad'].value or ""
        )

        if exito:
            util.actualizar_hash()
            ui.notify('Contacto actualizado en su posición original.', type='positive')
        else:
            ui.notify('Error al modificar el archivo.', type='negative')

    def limpiar_formulario(self):
        for input_field in self.inputs.values():
            input_field.value = None

    def accion_verificar_integridad(self):
        ok, mensaje = util.verificar_integridad()
        if ok:
            ui.notify(mensaje, type='positive', position='top')
        else:
            ui.notify(mensaje, type='negative', position='top', timeout=0)

    def accion_respaldo_zip(self):
        ok, mensaje = util.crear_respaldo_zip()
        if ok:
            ui.notify(mensaje, type='positive', multi_line=True, position='top-right', timeout=5000)
        else:
            ui.notify(mensaje, type='warning')

    def accion_info_archivo(self):
        info = util.obtener_metadatos()
        with ui.dialog() as dialog, ui.card():
            ui.label('Metadatos del Archivo').classes('text-lg font-bold')
            ui.label(info).classes('whitespace-pre-line')
            ui.button('Cerrar', on_click=dialog.close)
        dialog.open()

    def accion_exportar_json(self):
        ok, mensaje = exp.exportar_a_json()
        if ok:
            ui.notify(mensaje, type='positive', multi_line=True, position='top-right')
        else:
            ui.notify(mensaje, type='warning', multi_line=True, position='top-right')

    def accion_generar_pdf(self):
        ok, mensaje = exp.generar_reporte_pdf()
        if ok:
            ui.notify(mensaje, type='positive', multi_line=True, position='top-right')
        else:
            ui.notify(mensaje, type='warning', multi_line=True, position='top-right')