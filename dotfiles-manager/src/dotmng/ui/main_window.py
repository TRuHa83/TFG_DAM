import sys

from dotmng.modules     import log_manager
from dotmng.modules     import ServerPoller, TaskPoller, AppClient

from .worker            import Worker
from .actions           import Actions
from .handler           import Handler
from .widgets           import CustomItem
from .widgets           import CustomModel
from .load_screen       import LoadingScreen
from .interface.window  import Ui_MainWindow

from PySide6.QtGui      import QStandardItemModel, QStandardItem, QPixmap
from PySide6.QtCore     import QSize
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView


def _build_task_payload(source_widget) -> dict:
    properties_dict = {}
    method_name = None

    # Recorremos todas las propiedades del objeto
    for qbyte_name in source_widget.dynamicPropertyNames():
        name = qbyte_name.data().decode('utf-8')
        value = source_widget.property(name)

        # Separamos el 'method'
        if name == "method":
            method_name = value

        else:
            properties_dict[name] = value

    return {method_name: properties_dict}


class MainWindow(QMainWindow):
    def __init__(self, config, is_first_run=False):
        super().__init__()
        self.config = config
        self.__version__ = config.__version__
        self.is_first_run = is_first_run

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.stackedWidget.setCurrentIndex(0)

        self.log = log_manager.setup_logger("UI")

        self.action = Actions(config, self.log)
        self.handler = Handler()

        # Mostrar pantalla de carga
        self.loading_screen = LoadingScreen()
        self.loading_screen.show()

        QApplication.processEvents()
        self.load_config()

        self.endpoint = self.ui.endpoint_server.text()
        if self.endpoint != "":
            self.start_network_sync()

    def update_bar(self, text, step):
        self.loading_screen.task.setText(text)
        self.bar += step
        self.loading_screen.progress.setValue(self.bar)
        QApplication.processEvents()

    def reload_ui_data(self):
        self.update_bar("Cargando ajustes: ", 10)
        self.get_data()

        self.update_bar("Cargando dashboard: ", 10)
        self.update_info_dash()

        self.update_bar("Cargando aplicaciones: ", 10)
        self.update_info_apps()

        self.update_bar("Cargando desconocidos: ", 10)
        self.update_info_unknowns()

    def load_config(self):
        self.bar = 0

        if self.is_first_run:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Primera ejecución")
            msg_box.setText("Bienvenido a Dotfiles Manager.\n\nEs la primera vez que se inicia la interfaz gráfica y aún no se ha realizado ningún escaneo de tus dotfiles.\n\nPara que la aplicación funcione correctamente necesita analizar tu directorio home y registrar las aplicaciones reconocidas.\n\n¿Deseas realizar el escaneo inicial ahora?")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg_box.setDefaultButton(QMessageBox.StandardButton.Yes)
            
            if msg_box.exec() != QMessageBox.StandardButton.Yes:
                self.log.info("El usuario ha cancelado el escaneo inicial.")
                sys.exit(0)

            self.run_first_scan()

        self.reload_ui_data()

        self.loading_screen.task.setText("Iniciando interfaz...")
        self.update_bar("Cargando interfaz:", 10)
        self.connections()

        self.pending_discovery_task()

        # Cerrar pantalla de carga al finalizar
        self.loading_screen.close()

    def run_full_rescan(self):
        # Mostrar pantalla de carga
        self.loading_screen = LoadingScreen()
        self.loading_screen.show()
        self.bar = 0
        self.update_bar("Iniciando reescaneo completo...", 5)

        # Reutilizar run_first_scan
        self.run_first_scan()

        # Recargar los datos de la UI
        self.reload_ui_data()

        # Cerrar pantalla de carga al finalizar
        self.update_bar("Finalizando actualización...", 15)
        self.loading_screen.close()


    def run_first_scan(self):
        from pathlib import Path
        from dotmng.core.context import Context
        from dotmng.core.steps import (
            get_dotfiles,
            gen_hash_dot,
            compare_hashes,
            update_dot_hash,
            identify_dotfiles,
            filter_ignore,
            set_local_inventory,
            set_local_unknown,
            locate_conflict,
        )

        class _NullReporter:
            def send(self, *args, **kwargs):
                pass

        context = Context(
            path=Path.home(),
            session=self.action.db,
            reporter=_NullReporter(),
            log=self.log,
            force=True,
            startswith=".",
        )

        steps = [
            get_dotfiles,
            gen_hash_dot(input_attr="dotfiles"),
            compare_hashes(value="ALL_DOTFILES"),
            update_dot_hash,
            identify_dotfiles,
            filter_ignore,
            gen_hash_dot(input_attr="known_apps"),
            compare_hashes(value="KNOWNS"),
            update_dot_hash,
            gen_hash_dot(input_attr="unknown_files"),
            compare_hashes(value="UNKNOWNS"),
            update_dot_hash,
            set_local_inventory,
            set_local_unknown,
            locate_conflict,
        ]

        step_increment = 40 / len(steps)
        for i, step in enumerate(steps, 1):
            step_name = getattr(step, '__name__', f"Paso {i}")
            self.update_bar(f"Escaneo inicial: {step_name}...", step_increment)
            
            if context.halt or context.error:
                break
                
            if not context.jump:
                context = step(context)

    def get_data(self):
        text = self.loading_screen.task.text()

        self.update_bar(text + "hashes", 5)
        self.hashes = self.action.state_hashes()

        self.update_bar(text + "aplicaciones", 5)
        self.apps = self.action.get_apps()

        self.update_bar(text + "conflictos", 5)
        self.conflicts = self.action.get_conflicts()

        self.update_bar(text + "deshabilitados", 5)
        self.disables = self.action.get_disables()

        self.update_bar(text + "desconocidos", 5)
        self.unknowns = self.action.get_unknowns()

        self.pending_task = self.action.get_server_task()
        self.log.debug(f"main_window.py | 180 | {self.pending_task}")

    def update_info_dash(self):
        text = self.loading_screen.task.text()

        # --- DOTFILES --- #
        self.update_bar(text + "entidades", 5)
        def update_section(section_key, count_widget, hash_widget, time_widget, led_widget):
            data = self.hashes[section_key]
            count_widget.setText(str(data["item_count"]))
            hash_widget.setText(f"{data['current_hash'][:6]}...")
            hash_widget.setToolTip(data["current_hash"])
            time_widget.setText(data["last_checked_at"].strftime("%d / %m / %Y   %H:%M:%S"))
            led_widget.setVisible(False)

        update_section("ALL_DOTFILES", self.ui.count_dotfiles, self.ui.hash_dotfiles, self.ui.time_last_dotfiles, self.ui.led_dotfiles)
        update_section("KNOWNS", self.ui.count_files_apps, self.ui.hash_apps, self.ui.time_last_apps, self.ui.led_apps)
        update_section("UNKNOWNS", self.ui.count_files_unknown, self.ui.hash_unknown, self.ui.time_last_unknown, self.ui.led_unknown)

        # --- CLIENTE --- #
        self.update_bar(text + "sistema", 5)
        self.ui.hostname.setText(self.action.get_hostname())
        self.ui.os_machine.setText(self.action.get_distro_info())
        self.ui.id_machine.setText(self.action.get_id_machine())
        self.ui.version_manager.setText(self.__version__)

        # --- SERVIDOR --- #
        self.ui.server_status.setVisible(False)

        # Recuperamos el endpoint de la DB
        saved_endpoint = self.action.get_conf_server("endpoint")
        if saved_endpoint:
            self.ui.endpoint_server.setText(saved_endpoint)
            self.endpoint = saved_endpoint

        # Recuperamos la última conexión de la DB
        last_seen = self.action.get_conf_server("last_seen")
        if last_seen:
            self.ui.time_last_conection.setText(last_seen)

        #print(self.ui.endpoint_server.text())
        #print(self.ui.time_last_conection.text())

    def update_info_apps(self):
        text = self.loading_screen.task.text() or ""

        count = 0
        conflicts_apps = []
        enabled_apps = []
        disabled_apps = []

        self.ui.filter_cat.blockSignals(True)
        self.ui.filter_cat.clear()
        self.ui.filter_cat.addItem("Todas categorías")

        for key , value in self.apps.items():
            display_key = key if key is not None else "Sin categoría"
            self.update_bar(text + display_key, 2)
            self.ui.filter_cat.addItem(display_key)

            for (name, cat, app_id), files in value.items():
                files = ", ".join(files)
                cfts = any(conflict in files for conflict in self.conflicts)

                count += 1
                app = {
                    app_id: {
                        "name": name,
                        "files": files,
                        "main_cat": display_key,
                        "cat": cat,
                        "conflict": cfts
                    }
                }

                try:
                    override = self.disables.get(app_id)
                    if override is not None:
                        app[app_id]["disable"] = override["enabled"]

                    else:
                        app[app_id]["disable"] = True

                except KeyError:
                    app[app_id]["disable"] = True

                # Clasificamos según el orden deseado
                if cfts:
                    conflicts_apps.append(app)

                elif app[app_id]["disable"]:
                    enabled_apps.append(app)

                else:
                    disabled_apps.append(app)

        # Unimos las listas en el orden solicitado
        self.widget_apps = conflicts_apps + enabled_apps + disabled_apps

        self.ui.filter_cat.blockSignals(False)

        self.add_apps_to_widget()

        self.ui.count_apps.setText(str(count))
        self.ui.count_conflicts.setText(str(len(self.conflicts)))

    def update_info_unknowns(self):
        model = QStandardItemModel()
        self.ui.listView.setModel(model)
        self.ui.listView.setSpacing(4)
        self.ui.listView.setSelectionMode(QAbstractItemView.NoSelection)

        self.enabled_unknowns = []
        disabled_unknowns = []

        # Clasificamos primero
        for file_id, info in self.unknowns.items():
            if info["enabled"]:
                self.enabled_unknowns.append((file_id, info))
            else:
                disabled_unknowns.append((file_id, info))

        self.ui.count_unknown_off.setText(str(len(disabled_unknowns)))
        self.ui.count_unknown_total.setText(str(len(self.unknowns)))

        # Unimos las listas: primero habilitados, luego deshabilitados
        sorted_unknowns = self.enabled_unknowns + disabled_unknowns

        for file_id, info in sorted_unknowns:
            item = QStandardItem()
            item.setSizeHint(QSize(0, 55))
            model.appendRow(item)

            row_widget = CustomModel(
                file_id=file_id,
                file_path=info["path"],
                file_type=info["type"],
                enabled=info["enabled"],
            )

            row_widget.toggled.connect(self.toggle_unknown)

            index = item.index()
            self.ui.listView.setIndexWidget(index, row_widget)

    def connections(self):
        self.handler.ui_signal.connect(self.process_ui_signal)
        self.handler.update_widget_signal.connect(self.update_widget)

        for num in range(self.ui.stackedWidget.count()):
            button = 'nav_' + str(num)
            getattr(self.ui, button).clicked.connect(self.change_page)

        # DASHBOARD
        self.ui.main_update.clicked.connect(self.run_pipeline)

        self.ui.check_dotfiles.clicked.connect(self.run_pipeline)
        self.ui.check_apps.clicked.connect(self.run_pipeline)
        self.ui.check_unknown.clicked.connect(self.run_pipeline)

        #self.ui.check_updates.clicked.connect(self.connections)

        self.ui.edit_endpoint.clicked.connect(self.edit_endpoint)
        self.ui.endpoint_server.editingFinished.connect(self.set_endpoint)

        # APLICACIONES
        self.ui.app_update.clicked.connect(self.update_list_apps)
        self.ui.filter_cat.currentIndexChanged.connect(self.select_filter_cat)

        # DOTFILES UNKNOWNS
        self.ui.unknown_update.clicked.connect(self.update_dot_unknowns)
        self.ui.discovery_apps.clicked.connect(self.discovery_apps)

    def update_list_apps(self):
        self.apps = self.action.get_apps()
        self.conflicts = self.action.get_conflicts()
        self.disables = self.action.get_disables()

        self.update_info_apps()

    def update_dot_unknowns(self):
        self.log.debug(f"main_window.py | 356 | actualizando")
        self.unknowns = self.action.get_unknowns()

        if self.ui.listView.model() is not None:
            self.ui.listView.model().clear()

        self.update_info_unknowns()

    def add_apps_to_widget(self):
        main_cat = self.ui.filter_cat.currentText()
        layout = self.ui.widgetApps.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        for app in self.widget_apps:
            if main_cat == "Todas categorías":
                pass

            elif app[list(app.keys())[0]]["main_cat"] != main_cat:
                continue

            item = CustomItem(self.config.CACHE_DIR, app)
            # Evitamos el problema de "late binding" de los bucles en Python guardando 'item' y 'app'
            item.toggleButton.clicked.connect(lambda checked=False, i=item: self.toggle_app(i))
            layout.addWidget(item)

    def start_network_sync(self):
        # Detener el poller existente si lo hay
        if hasattr(self, 'poller') and self.poller.isRunning():
            self.poller.stop()
            self.poller.wait()

        self.poller = ServerPoller(self.endpoint, interval=30)

        # Conectar señales
        self.poller.finished_ok.connect(self.on_server_success)
        self.poller.finished_error.connect(self.on_server_failure)

        # Iniciar hilo
        self.poller.start()

    def on_server_success(self, data):
        # Actualizar icono de la UI a verde
        self.update_widget("server_status", ":/assets/icons/led_green.svg", True)

        # Guardamos en la DB y actualizamos el label con la hora formateada
        last_seen = self.action.set_conf_server("last_seen", "now")
        self.update_widget("time_last_conection", last_seen)

        # Volvemos a obtener la tarea pendiente para verificar su estado actual
        self.pending_task = self.action.get_server_task()

        # Activamos el botón descubrimiento de apps si no hay tareas pendientes activas
        if not self.pending_task or self.pending_task.get('state') not in ["QUEUE", "PROCESSING"]:
            self.ui.discovery_apps.setEnabled(True)
            self.update_widget("discovery_apps", "Descubrimiento")

    def on_server_failure(self, error):
        self.log.debug(f"main_window.py | 414 | Pooling detenido: {error}")

        # Actualizar icono de la UI a rojo
        self.update_widget("server_status", ":/assets/icons/led_red.svg", True)

        # Desactivamos el boton descubrimiento de apps
        self.ui.discovery_apps.setEnabled(False)

    def change_page(self):
        button = self.sender()
        index = button.property("index")
        self.ui.stackedWidget.setCurrentIndex(index)

    def edit_endpoint(self):
        self.ui.endpoint_server.setEnabled(True)
        self.ui.endpoint_server.setFocus()

    def set_endpoint(self):
        self.ui.endpoint_server.setEnabled(False)
        self.endpoint = self.ui.endpoint_server.text()
        
        # Guardamos en la DB
        self.action.set_conf_server("endpoint", self.endpoint)
        
        self.start_network_sync()

    def select_filter_cat(self):
        self.add_apps_to_widget()

    def toggle_app(self, item):
        app = {
            item.property("app_id"): {
                "name": item.property("name"),
                "files": item.property("files"),
                "cat": item.property("cat"),
                "conflict": item.property("conflict"),
                "disable": not item.property("disable")
            }
        }

        layout = self.ui.widgetApps.layout()
        index = layout.indexOf(item)
        if index != -1:
            layout.removeWidget(item)
            item.deleteLater()

            new_item = CustomItem(self.config.CACHE_DIR, app)
            # Evitamos el problema de "late binding" de los bucles en Python guardando 'new_item' y 'app'
            new_item.toggleButton.clicked.connect(lambda checked=False, i=new_item: self.toggle_app(i))
            layout.insertWidget(index, new_item)

        else:
            item.deleteLater()
            new_item = CustomItem(self.config.CACHE_DIR, app)
            new_item.toggleButton.clicked.connect(lambda checked=False, i=new_item: self.toggle_app(i))
            layout.addWidget(new_item)

        app_id = item.property("app_id")
        currently_disabled = item.property("disable")
        new_enabled = not currently_disabled

        self.action.set_disables(app_id=app_id, enabled=new_enabled)

    def toggle_unknown(self, file_id, checked):
        self.action.set_unknowns(file_id)
        if file_id in self.unknowns:
            self.unknowns[file_id]["enabled"] = checked

        # Re-evaluamos self.enabled_unknowns y actualizamos el contador en la UI
        self.enabled_unknowns = []
        disabled_count = 0
        for fid, info in self.unknowns.items():
            if info["enabled"]:
                self.enabled_unknowns.append((fid, info))
            else:
                disabled_count += 1
        
        self.ui.count_unknown_off.setText(str(disabled_count))

    def pending_discovery_task(self):
        # Solo consideramos la tarea pendiente si existe y su estado es QUEUE o PROCESSING
        if self.pending_task and self.pending_task.get('state') in ["QUEUE", "PROCESSING"]:
            self.log.debug(f"main_window.py | 409 | Tarea pendiente detectada: {self.pending_task['task_id']}")
            self.task_poller = TaskPoller(self.endpoint, self.pending_task['task_id'])
            self.task_poller.status_changed.connect(self.on_task_status)
            self.task_poller.finished.connect(self.on_task_finished)
            self.task_poller.start()

            # Bloqueamos el botón y cambiamos el texto
            #self.ui.discovery_apps.setEnabled(False)
            self.update_widget("discovery_apps", "Procesando...")

        else:
            # Si no hay tarea pendiente activa, aseguramos que el botón esté habilitado
            #self.ui.discovery_apps.setEnabled(True)
            self.update_widget("discovery_apps", "Descubrimiento")


    def discovery_apps(self):
        self.log.info("Iniciando descubrimiento de aplicaciones en el servidor...")
        
        # Nos aseguramos de reconstruir la lista de habilitados basándonos únicamente en los habilitados
        self.enabled_unknowns = [
            (file_id, info) for file_id, info in self.unknowns.items() if info["enabled"]
        ]
        
        if not self.enabled_unknowns:
            self.log.warning("No hay archivos desconocidos habilitados para enviar.")
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Sin elementos")
            msg_box.setText("No hay ningún archivo desconocido habilitado.")
            msg_box.setInformativeText("Por favor, marca al menos un archivo en la lista de desconocidos para poder realizar el descubrimiento.")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            return

        payload = {}
        for file_id, info in self.enabled_unknowns:
            payload[file_id] = {
                "path": info["path"],
                "type": info["type"]
            }

        client = AppClient(self.endpoint)
        
        try:
            task_id = client.discovery_apps(payload)
        except Exception as e:
            self.log.exception("Excepción al intentar llamar al endpoint de descubrimiento")
            task_id = None

        if task_id:
            self.log.info(f"Tarea de descubrimiento iniciada correctamente. ID de tarea: {task_id}")
            # Guardamos la nueva tarea en la DB
            self.action.set_server_task(task_id)

            # Iniciamos el poller
            self.task_poller = TaskPoller(self.endpoint, task_id)
            self.task_poller.status_changed.connect(self.on_task_status)
            self.task_poller.finished.connect(self.on_task_finished)
            self.task_poller.start()

            # Bloqueamos el botón y cambiamos el texto
            self.ui.discovery_apps.setEnabled(False)
            self.update_widget("discovery_apps", "Procesando...")

        else:
            self.log.error("No se pudo iniciar la tarea de descubrimiento en el servidor (el servidor no devolvió un ID de tarea).")
            self.ui.discovery_apps.setEnabled(True)
            self.update_widget("discovery_apps", "Descubrimiento")
            
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setWindowTitle("Error de servidor")
            msg_box.setText("No se pudo iniciar la tarea de descubrimiento en el servidor.")
            msg_box.setInformativeText("Verifica la conexión del servidor o consulta los archivos de registro de log del sistema para obtener más detalles.")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()

    def on_task_status(self, status, data):
        self.log.debug(f"Estado de la tarea recibido: {status}")
        # Actualizar estado en la DB local (en mayúsculas)
        if self.task_poller:
            self.action.set_server_task(self.task_poller.task_id, status.upper())

        # Aquí actualizamos el texto del botón según el estado del servidor
        if status == "PROCESSING":
            self.update_widget("discovery_apps", "En progreso...")

        elif status == "QUEUE":
            self.update_widget("discovery_apps", "En cola...")

    def on_task_finished(self, success, data):
        self.log.info(f"Tarea finalizada. Éxito: {success}")
        
        try:
            # Aseguramos el estado final en la DB
            status = "COMPLETE" if success else "ERROR"
            if self.task_poller:
                self.action.set_server_task(self.task_poller.task_id, status)

            self.ui.discovery_apps.setEnabled(True)
            self.update_widget("discovery_apps", "Descubrimiento")

            if success:
                classified_data = data.get("data", {})
                if classified_data:
                    self.log.info("Datos de clasificación recibidos. Guardando en la base de datos...")
                    self.action.save_classified_data(classified_data)

                self.log.info("Apps descubiertas con éxito. Iniciando reescaneo...")

                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Descubrimiento completado")
                msg_box.setText("El descubrimiento de aplicaciones se ha completado con éxito.")
                msg_box.setInformativeText("La base de datos de referencia ha sido actualizada.\n\nSe procederá a realizar un reescaneo completo del sistema para actualizar tu inventario local.")
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.exec()

                # Borrar tablas locales
                self.action.clear_local_inventory_and_unknown()

                # Ejecutar reescaneo completo con barra de carga
                self.run_full_rescan()

            else:
                error_msg = data.get("error", "Error desconocido")
                self.log.error(f"Fallo en la tarea de descubrimiento de aplicaciones en el servidor: {error_msg}")
                
                msg_box = QMessageBox(self)
                msg_box.setIcon(QMessageBox.Icon.Critical)
                msg_box.setWindowTitle("Error de descubrimiento")
                msg_box.setText("No se pudo completar el descubrimiento de aplicaciones.")
                msg_box.setInformativeText(f"Detalle del error devuelto por el servidor:\n{error_msg}")
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.exec()

        except Exception as e:
            self.log.exception("Error crítico durante el procesamiento del fin de la tarea")
            
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setWindowTitle("Error crítico")
            msg_box.setText("Ocurrió un error inesperado al procesar el descubrimiento.")
            msg_box.setInformativeText(f"Excepción capturada:\n{str(e)}")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            
            # Asegurar que se cierra la pantalla de carga si existe y está visible para evitar que la UI se congele
            if hasattr(self, 'loading_screen') and self.loading_screen:
                try:
                    self.loading_screen.close()
                except Exception:
                    pass

    def run_pipeline(self, ):
        if hasattr(self, 'worker') and self.worker.isRunning():
            return

        button = self.sender()

        config = {
            "config": self.config,
            "handler": self.handler,
            "log": self.log
        }

        self.worker = Worker(config, task=_build_task_payload(button))
        self.worker.start()

    def update_widget(self, widget_name, text=None, state=None):
        widget = getattr(self.ui, widget_name, None)

        if not widget:
            return

        if text is not None:
            if isinstance(text, str) and text.startswith(":/") and hasattr(widget, "setPixmap"):
                widget.setPixmap(QPixmap(text))

            elif hasattr(widget, "setText"):
                widget.setText(str(text))

            else:
                self.log.warning(f"El widget '{widget_name}' no tiene el método 'setText' o 'setPixmap'. No se pudo actualizar el widget.")

        if state is not None:
            widget.setVisible(state)

    def process_ui_signal(self, action, context):
        if action == "check_dotfiles":
            # Actualizamos los labels accediendo a las propiedades del objeto context
            if hasattr(context, 'count'):
                self.ui.count_dotfiles.setText(str(context.count))
            
            if hasattr(context, 'hash') and context.hash:
                self.ui.hash_dotfiles.setText(f"{context.hash[:6]}...")
                self.ui.hash_dotfiles.setToolTip(context.hash)