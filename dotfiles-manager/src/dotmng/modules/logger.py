import sys
import logging

from datetime import datetime

from logging.handlers import TimedRotatingFileHandler

from dotmng.config import cfg


logging.addLevelName(logging.WARNING, 'WARN')


class Logger:
    def __init__(self):
        # Configuración base
        self.LOG_DIR = cfg.STATE_DIR
        self.FORMATTER = logging.Formatter(
            "%(asctime)s [ %(levelname)5s ] [ %(lineno)3d ] %(name)-4s > %(message)s",
            datefmt='%H:%M:%S'
        )
        now = datetime.now().strftime("%Y-%m-%d")
        self.name = f"{now}.log"

    def setup_logger(self, name: str, level: str = "INFO", console: bool = False):
        """
        Configura y devuelve un logger con el nombre especificado.
        """
        if not self.LOG_DIR.exists():
            self.LOG_DIR.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger(name)

        # Si el logger ya tiene handlers, no añadimos más para evitar duplicados
        if not logger.handlers:
            logger.setLevel(level)

            file_handler = TimedRotatingFileHandler(
                filename=self.LOG_DIR / self.name,
                when="midnight",
                interval=1,
                backupCount=30,
                encoding="utf-8"
            )

            file_handler.setLevel(level)
            file_handler.setFormatter(self.FORMATTER)

            logger.addHandler(file_handler)

            is_ui_mode = len(sys.argv) <= 1
            if console or (is_ui_mode and sys.stdout.isatty()):
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setLevel("DEBUG")
                console_handler.setFormatter(self.FORMATTER)

                logger.addHandler(console_handler)


        return logger