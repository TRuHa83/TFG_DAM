import time
import requests

from PySide6.QtCore import QThread, Signal
from dotmng.modules.logger import Logger

log_manager = Logger()


# Hilo que comprueba si el servidor está disponible
class ServerPoller(QThread):
    # Señales para comunicar resultados a la App/UI
    finished_ok    = Signal(str)   # Se emite cuando el servidor responde OK
    finished_error = Signal(str)   # Se emite cuando falla
    status_changed = Signal(bool)  # Indica si el pooling está activo o no

    def __init__(self, endpoint: str, interval: int = 60):
        super().__init__()
        self.log = log_manager.setup_logger("POLLER")
        check = endpoint.rstrip('/') + "/health"
        self.endpoint = check
        self.interval = interval
        self._is_running = False
        self.last_response_ok = False

    def stop(self):
        # Detiene el hilo de forma segura.
        self._is_running = False

    def run(self):
        self._is_running = True
        self.log.info(f"Iniciando ServerPoller en endpoint: {self.endpoint}")
        self.status_changed.emit(True)

        while self._is_running:
            try:
                # Realizar la petición
                response = requests.get(self.endpoint, timeout=10)

                # Comprobamos si la respuesta del servidor es "ok"
                if response.status_code == 200 and response.text == "ok":
                    self.last_response_ok = True
                    self.finished_ok.emit(response.text)

                else:
                    self.last_response_ok = False
                    error_msg = f"respuesta del servidor: {response.status_code}"
                    self.log.warning(f"ServerPoller: Servidor no disponible ({error_msg})")
                    self.finished_error.emit(error_msg)
                    self._is_running = False  # Detenemos el pooling

            except Exception as e:
                self.last_response_ok = False
                self.log.warning(f"ServerPoller: Error de conexión con el servidor (servidor apagado o no disponible): {e}")
                self.finished_error.emit(f"fallo de conexión con el servidor")
                self._is_running = False  # Detenemos el pooling ante cualquier excepción de red

            # Esperar antes de la siguiente petición si sigue activo
            if self._is_running:
                time.sleep(self.interval)

        self.status_changed.emit(False)
        self.log.info("ServerPoller finalizado.")


# Hilo para comprobar el estado de la petición
class TaskPoller(QThread):
    status_changed = Signal(str, dict)
    finished = Signal(bool, dict)

    def __init__(self, endpoint: str, task_id: str, interval: int = 2):
        super().__init__()
        self.log = log_manager.setup_logger("POLLER")
        self.endpoint = endpoint.rstrip('/')
        self.task_id = task_id
        self.interval = interval
        self._is_running = False

    def stop(self):
        self._is_running = False

    def run(self):
        self._is_running = True
        self.log.info(f"Iniciando TaskPoller para la tarea {self.task_id} en {self.endpoint}...")
        
        while self._is_running:
            try:
                url = f"{self.endpoint}/task/{self.task_id}"
                self.log.debug(f"TaskPoller: Consultando estado de la tarea en {url}...")
                response = requests.get(url, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    import json
                    self.log.debug(f"JSON recibido del servidor: {json.dumps(data)}")
                    status = data.get("status", "QUEUE").upper()
                    
                    self.log.debug(f"TaskPoller: Estado de la tarea {self.task_id} es {status}")
                    self.status_changed.emit(status, data)

                    if status == "COMPLETE":
                        self.log.info(f"TaskPoller: Tarea {self.task_id} completada exitosamente.")
                        self.finished.emit(True, data)
                        self._is_running = False

                    elif status == "ERROR":
                        self.log.error(f"TaskPoller: El servidor reportó error en la tarea {self.task_id}. Respuesta: {data}")
                        self.finished.emit(False, data)
                        self._is_running = False
                else:
                    error_data = {"error": f"HTTP {response.status_code}", "text": response.text}
                    self.log.error(f"TaskPoller: Respuesta HTTP inesperada ({response.status_code}) consultando tarea {self.task_id}: {response.text}")
                    self.status_changed.emit("error", error_data)
                    self.finished.emit(False, error_data)
                    self._is_running = False

            except Exception as e:
                error_data = {"error": str(e)}
                self.log.exception(f"TaskPoller: Excepción ocurrida al consultar la tarea {self.task_id}")
                self.status_changed.emit("error", error_data)
                self.finished.emit(False, error_data)
                self._is_running = False

            if self._is_running:
                time.sleep(self.interval)

        self.log.info(f"TaskPoller para la tarea {self.task_id} finalizado.")