import os
import dotmng.version as version

from pathlib import Path


class Config:
    def __init__(self):
        self.__version__ = version.__version__
        self.__author__  = version.__author__
        self.__name__    = version.__name__
        self.__app__     = version.__app__

        # --- RUTAS XDG ---
        # ~/.local/share/dotmng (Para la DB)
        self.DATA_DIR = Path(os.getenv("XDG_DATA_HOME", Path.home() / ".local/share")) / self.__app__
        self.DB_PATH = self.DATA_DIR / "data.db"

        # ~/.local/state/dotmng (Para los Logs)
        self.STATE_DIR = Path(os.getenv("XDG_STATE_HOME", Path.home() / ".local/state")) / self.__app__

        # ~/.cache/dotmng (Para descargas temporales, caché de iconos, etc.)
        self.CACHE_DIR = Path(os.getenv("XDG_CACHE_HOME", Path.home() / ".cache")) / self.__app__

        # Asegurar que las carpetas existan al instanciar la config
        self._ensure_dirs()

    def _ensure_dirs(self):
        for directory in [self.DATA_DIR, self.STATE_DIR, self.CACHE_DIR]:
            directory.mkdir(parents=True, exist_ok=True)


# Instancia global para importar en el resto del proyecto
cfg = Config()