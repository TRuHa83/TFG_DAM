import requests
from pathlib import Path


class Icon:
    def __init__(self, cache_dir):
        self.cache_path = Path(cache_dir)
        self.cache_path.mkdir(parents=True, exist_ok=True)

    def resolve(self, app_name):
        name = app_name.lower().strip().replace(" ", "-")
        local_file = self.cache_path / f"{name}.svg"

        # 1. ¿Ya lo tenemos? (Caché local)
        if local_file.exists():
            return str(local_file)

        # 2. Intentar buscar online
        try:
            # timeout=3 es vital para que el script no se quede colgado si no hay red
            search_res = requests.get(
                f"https://api.iconify.design/search?query={name}&limit=1",
                timeout=3
            )

            if search_res.status_code == 200:
                data = search_res.json()
                if data.get("icons"):
                    icon_id = data["icons"][0]  # Ejemplo: "simple-icons:steam"
                    prefix, icon_name = icon_id.split(':')

                    # Descargamos el SVG real
                    svg_res = requests.get(f"https://api.iconify.design/{prefix}/{icon_name}.svg?width=64&height=64", timeout=3)
                    if svg_res.status_code == 200:
                        local_file.write_bytes(svg_res.content)
                        return str(local_file)

        except Exception:
            return None
