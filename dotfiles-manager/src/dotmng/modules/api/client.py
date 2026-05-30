import requests
from dotmng.modules.logger import Logger

log_manager = Logger()


class AppClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.log = log_manager.setup_logger("CLIENT")

    def discovery_apps(self, payload: dict) -> str | None:
        try:
            url = f"{self.endpoint.rstrip('/')}/discovery"
            self.log.info(f"Enviando petición de descubrimiento a {url} con {len(payload)} elementos...")
            
            wrapped_payload = {"data": payload}
            import json
            self.log.debug(f"JSON enviado al servidor (payload de discovery): {json.dumps(wrapped_payload)}")
            response = requests.post(url, json=wrapped_payload, timeout=10)

            if response.status_code in [200, 202]:
                data = response.json()
                task_id = data.get("taskID")
                self.log.info(f"Petición de descubrimiento aceptada. Task ID recibido: {task_id}")
                return task_id
            
            self.log.error(f"Error en respuesta del servidor al enviar descubrimiento. Código HTTP: {response.status_code}, Respuesta: {response.text}")
            return None

        except Exception as e:
            self.log.exception(f"Excepción en discovery_apps al conectar con {self.endpoint}")
            return None
