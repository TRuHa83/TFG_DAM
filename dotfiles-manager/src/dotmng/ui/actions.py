import subprocess

from pathlib import Path

from dotmng.modules import DataBase


class Actions:
    def __init__(self, config, log):
        self.base_path = config.DATA_DIR
        self.db_path = config.DB_PATH

        self.log = log

        self.home_path = Path.home()
        self.conf_path = self.home_path.joinpath(".config")

        self.db = DataBase(self.db_path)

    def get_distro_info(self):
        command = ['cat', '/etc/os-release']
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)

            data = {}
            for line in result.stdout.splitlines():
                if '=' in line:
                    key, value = line.split('=', 1)
                    data[key] = value.strip('"')

            return data.get('PRETTY_NAME') or data.get('NAME') or data.get('ID') or "Desconocido"

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            self.log.error(f"Error al ejecutar el comando: {e}")
            return "Desconocido"

    def get_id_machine(self):
        command = ["cat", "/etc/machine-id"]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout.strip()

        except subprocess.CalledProcessError as e:
            self.log.error(f"Error al ejecutar el comando: {e}")
            return "Desconocido"

    def get_hostname(self):
        command = ["hostname"]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout.strip()

        except subprocess.CalledProcessError as e:
            self.log.error(f"Error al ejecutar el comando: {e}")
            return "Desconocido"

    def get_apps(self):
        return self.db.get_local_for_inform()

    def get_conflicts(self):
        return self.db.get_local_conflicts()

    def get_disables(self):
        return self.db.get_user_inventory_overrides()

    def set_disables(self, app_id: str, enabled: bool):
        self.db.set_user_inventory_override(app_id=app_id, enabled=enabled)

    def get_unknowns(self):
        return self.db.get_local_unknown()

    def set_unknowns(self, id_file: int):
        unknown = self.db.get_local_unknown_by_id(id_file)
        if not unknown:
            self.log.warning(f"Archivo desconocido con id {id_file} no encontrado.")
            return

        # Leer el estado efectivo actual (calculado con LEFT JOIN)
        all_unknowns = self.db.get_local_unknown()
        current_enabled = all_unknowns.get(id_file, {}).get("enabled", True)
        self.db.set_user_unknown_override(path=unknown["path"], enabled=not current_enabled)

    def state_hashes(self):
        data = {}
        states = ["ALL_DOTFILES", "KNOWNS", "UNKNOWNS"]
        for state in states:
            info = self.db.get_system_state_hashes(state)
            data[state] = {
                "current_hash": info.current_hash,
                "item_count": info.item_count,
                "last_checked_at": info.last_checked_at
            }

        return data

    def get_conf_server(self, config):
        return self.db.get_conf_server(config)

    def set_conf_server(self, config, value):
        return self.db.set_conf_server(config, value)

    def get_server_task(self, task_id: str=None):
        return self.db.get_server_task(task_id)

    def set_server_task(self, task_id: str, state: str=None):
        self.db.set_server_task(task_id, state)

    def save_classified_data(self, data: dict):
        if data:
            self.log.info(f"Enviando {len(data)} aplicaciones clasificadas para guardar en la base de datos.")
            self.db.save_classified_data(data)
        else:
            self.log.warning("No se recibieron datos de clasificación para guardar.")

    def clear_local_inventory_and_unknown(self):
        self.db.clear_local_inventory_and_unknown()

