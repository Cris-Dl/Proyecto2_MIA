from nicegui import ui
import repositorio_archivos as repo
import gestor_indice as indice
import utilidades as util
import exportador as exp

class AgendaUI:
    def __init__(self):
        self.inputs = {}
        self.input_buscar = None
        self.menu_actual = 'Inicio'
        self.vista_actual = 'inicio'
        self.dark_mode = None

    def cambiar_menu(self, menu):
        self.menu_actual = menu
        if menu == 'Ayuda':
            self.vista_actual = 'ayuda_acerca'
        else:
            self.vista_actual = 'esperando_accion'

        self.render_top_bar.refresh()
        self.render_main_content.refresh()

    def cambiar_vista(self, vista):
        self.vista_actual = vista
        self.render_main_content.refresh()

    @ui.refreshable
    def render_top_bar(self):
        with ui.row().classes(
                'w-full bg-primary dark:bg-slate-800 p-3 items-center justify-between shadow-md rounded-b-lg mb-4 transition-colors'):

            ui.label(self.menu_actual.upper()).classes('text-xl font-bold text-white tracking-wider ml-4')

            with ui.row().classes('flex-grow justify-end gap-2 sm:gap-4 mr-4'):
                estilo_btn_top = 'text-white font-semibold'
                if self.menu_actual == 'Contactos':
                    ui.button('Nuevo Contacto', icon='add',
                              on_click=lambda: self.cambiar_vista('nuevo_contacto')).classes(estilo_btn_top).props(
                        'flat')
                    ui.button('Buscar / Modificar', icon='search',
                              on_click=lambda: self.cambiar_vista('buscar_modificar')).classes(estilo_btn_top).props(
                        'flat')
                elif self.menu_actual == 'Exportar':
                    ui.button('JSON', icon='data_object', on_click=lambda: self.cambiar_vista('exportar_json')).classes(
                        estilo_btn_top).props('flat')
                    ui.button('PDF', icon='picture_as_pdf',
                              on_click=lambda: self.cambiar_vista('exportar_pdf')).classes(estilo_btn_top).props('flat')
                elif self.menu_actual == 'Herramientas':
                    ui.button('Integridad SHA-256', icon='security',
                              on_click=lambda: self.cambiar_vista('herramienta_hash')).classes(estilo_btn_top).props(
                        'flat')
                    ui.button('Respaldo ZIP', icon='folder_zip',
                              on_click=lambda: self.cambiar_vista('herramienta_zip')).classes(estilo_btn_top).props(
                        'flat')
                    ui.button('Metadatos', icon='info',
                              on_click=lambda: self.cambiar_vista('herramienta_meta')).classes(estilo_btn_top).props(
                        'flat')

    @ui.refreshable
    def render_main_content(self):
        with ui.column().classes('w-full flex-grow flex items-center justify-start pt-6'):
            with ui.card().classes('w-full max-w-lg p-5 shadow-2xl rounded-xl dark:bg-slate-800 transition-all'):

                if self.vista_actual == 'inicio':
                    with ui.column().classes('w-full items-center py-10'):
                        ui.icon('contact_page', size='64px').classes('text-gray-400 dark:text-gray-500 mb-4')
                        ui.label('Bienvenido a la Agenda MVP').classes(
                            'text-2xl font-bold text-center text-gray-700 dark:text-white mb-2')
                        ui.label('Seleccione una categoría en el menú lateral para comenzar.').classes(
                            'text-center text-gray-500 dark:text-gray-400')

                elif self.vista_actual == 'esperando_accion':
                    with ui.column().classes('w-full items-center py-10'):
                        ui.icon('ads_click', size='64px').classes('text-blue-400 dark:text-gray-500 mb-4')
                        ui.label(f'Sección: {self.menu_actual}').classes(
                            'text-2xl font-bold text-center text-gray-700 dark:text-white mb-2')
                        ui.label('Seleccione una operación en la barra superior.').classes(
                            'text-center text-gray-500 dark:text-gray-400')

                elif self.vista_actual == 'nuevo_contacto':
                    ui.label('Agregar Nuevo Contacto').classes(
                        'text-2xl mb-2 font-bold text-center w-full text-gray-700 dark:text-white')
                    self.dibujar_formulario(modo="nuevo")

                elif self.vista_actual == 'buscar_modificar':
                    ui.label('Buscar y Modificar').classes(
                        'text-2xl mb-2 font-bold text-center w-full text-gray-700 dark:text-white')

                    with ui.row().classes('w-full items-center gap-2 mb-2'):
                        self.input_buscar = ui.number('ID a buscar').classes('flex-grow')
                        ui.button('Buscar', on_click=self.ejecutar_busqueda, color='primary', icon='search').classes(
                            'h-10')

                    ui.separator().classes('mb-3')
                    self.dibujar_formulario(modo="modificar")

                elif self.vista_actual == 'exportar_json':
                    ui.label('Exportar a JSON').classes(
                        'text-2xl mb-4 font-bold text-center w-full text-gray-700 dark:text-white')
                    ui.label('Genera un archivo JSON estructurado con todos los registros actuales.').classes(
                        'mb-6 text-center w-full dark:text-gray-300')
                    ui.button('Ejecutar Exportación', on_click=self.accion_exportar_json, color='primary',
                              icon='data_object').classes('w-full text-lg font-bold')

                elif self.vista_actual == 'exportar_pdf':
                    ui.label('Reporte PDF').classes(
                        'text-2xl mb-4 font-bold text-center w-full text-gray-700 dark:text-white')
                    ui.label(
                        'Genera un documento PDF formateado en tabla con la lista de todos los contactos.').classes(
                        'mb-6 text-center w-full dark:text-gray-300')
                    ui.button('Generar PDF', on_click=self.accion_generar_pdf, color='primary',
                              icon='picture_as_pdf').classes('w-full text-lg font-bold')

                elif self.vista_actual == 'herramienta_hash':
                    ui.label('Integridad SHA-256').classes(
                        'text-2xl mb-4 font-bold text-center w-full text-gray-700 dark:text-white')
                    ui.label(
                        'Verifica si el archivo de contactos ha sido alterado externamente comparando su Hash.').classes(
                        'mb-6 text-center w-full dark:text-gray-300')
                    ui.button('Verificar Archivo', on_click=self.accion_verificar_integridad, color='primary',
                              icon='security').classes('w-full text-lg font-bold')

                elif self.vista_actual == 'herramienta_zip':
                    ui.label('Respaldo ZIP').classes(
                        'text-2xl mb-4 font-bold text-center w-full text-gray-700 dark:text-white')
                    ui.label('Comprime la base de datos y el índice JSON en un archivo ZIP de seguridad.').classes(
                        'mb-6 text-center w-full dark:text-gray-300')
                    ui.button('Crear ZIP', on_click=self.accion_respaldo_zip, color='primary',
                              icon='folder_zip').classes('w-full text-lg font-bold')

                elif self.vista_actual == 'herramienta_meta':
                    ui.label('Metadatos del Sistema').classes(
                        'text-2xl mb-4 font-bold text-center w-full text-gray-700 dark:text-white')
                    ui.label(
                        'Consulta el tamaño exacto, fechas de modificación y permisos del sistema operativo.').classes(
                        'mb-6 text-center w-full dark:text-gray-300')
                    ui.button('Ver Metadatos', on_click=self.accion_info_archivo, color='primary', icon='info').classes(
                        'w-full text-lg font-bold')

                elif self.vista_actual == 'ayuda_acerca':
                    ui.label('Acerca de...').classes(
                        'text-2xl mb-4 font-bold text-center w-full text-gray-700 dark:text-white')
                    ui.label(
                        'Proyecto 02 - Manejo de Archivos\nUniversidad Rafael Landívar\n\nDesarrollado en Python con Acceso Aleatorio.').classes(
                        'text-center w-full whitespace-pre-line dark:text-gray-300')

    def dibujar_formulario(self, modo):
        self.inputs['id'] = ui.number('ID (Número entero)').classes('w-full mb-1')
        if modo == "modificar":
            self.inputs['id'].disable()

        self.inputs['nombre'] = ui.input('Nombre').classes('w-full mb-1')
        self.inputs['telefono'] = ui.input('Teléfono').classes('w-full mb-1')
        self.inputs['correo'] = ui.input('Correo Electrónico').classes('w-full mb-1')
        self.inputs['ciudad'] = ui.input('Ciudad').classes('w-full mb-3')

        if modo == "nuevo":
            ui.button('Guardar Nuevo Contacto', on_click=self.guardar_contacto, color='positive', icon='save').classes(
                'w-full text-lg font-bold')
        else:
            ui.button('Guardar Cambios', on_click=self.modificar_contacto, color='warning', icon='edit').classes(
                'w-full text-lg font-bold text-white')

    def construir_interfaz(self):
        self.dark_mode = ui.dark_mode()
        ui.query('body').classes('bg-slate-50 dark:bg-slate-900 transition-colors')

        with ui.left_drawer(elevated=True).classes(
                'flex flex-col justify-between bg-slate-50 dark:bg-slate-950 border-r dark:border-slate-800 transition-colors'):
            with ui.column().classes('w-full p-4'):
                ui.label('Agenda URL').classes(
                    'text-2xl font-bold text-center w-full py-3 rounded-xl bg-slate-200 dark:bg-slate-800 text-primary dark:text-blue-400 shadow-sm mt-2')
                ui.separator().classes('my-5')

                estilo_btn = 'w-full justify-start px-4 py-3 mb-2 text-lg font-bold border border-slate-300 dark:border-slate-700 rounded-lg text-primary dark:text-slate-300 transition-colors hover:bg-slate-200 dark:hover:bg-slate-800'
                ui.button('Contactos', icon='person', on_click=lambda: self.cambiar_menu('Contactos')).classes(
                    estilo_btn).props('flat')
                ui.button('Exportar', icon='download', on_click=lambda: self.cambiar_menu('Exportar')).classes(
                    estilo_btn).props('flat')
                ui.button('Herramientas', icon='build', on_click=lambda: self.cambiar_menu('Herramientas')).classes(
                    estilo_btn).props('flat')
                ui.button('Ayuda', icon='help', on_click=lambda: self.cambiar_menu('Ayuda')).classes(estilo_btn).props(
                    'flat')

            with ui.column().classes('w-full p-4 items-center'):
                ui.separator().classes('w-full mb-4')
                ui.switch('Modo Oscuro').bind_value(self.dark_mode, 'value').classes('font-bold dark:text-gray-300')

        with ui.column().classes(
                'w-full min-h-screen p-0 m-0 bg-slate-50 dark:bg-slate-900 transition-colors flex flex-col'):
            self.render_top_bar()
            self.render_main_content()

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

    def ejecutar_busqueda(self):
        id_buscar = self.input_buscar.value
        if id_buscar is None:
            return

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
            ui.notify('Contacto cargado. Edite los campos y presione Guardar Cambios.', type='info')

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
            if not input_field.props.get('disable'):
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
        with ui.dialog() as dialog, ui.card().classes('dark:bg-slate-800'):
            ui.label('Metadatos del Archivo').classes('text-lg font-bold dark:text-white')
            ui.label(info).classes('whitespace-pre-line dark:text-gray-300')
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