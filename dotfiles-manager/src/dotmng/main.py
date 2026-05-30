import sys

from dotmng.ui      import MainWindow
from dotmng.cli     import CLI
from dotmng.config  import cfg
from dotmng.modules import log_manager, DataBase


def main():
    log = log_manager.setup_logger("MAIN")

    log.info("=" * 20)
    log.info("DotfileManager starting...")

    if len(sys.argv) > 1:
        cli = CLI(cfg)
        cli.run(sys.argv[1:])

    else:
        from PySide6.QtWidgets import QApplication
        app = QApplication(sys.argv)

        # Detectar primer arranque (local_inventory vacía)
        db = DataBase(cfg.DB_PATH)
        is_first_run = db.is_first_run()

        window = MainWindow(cfg, is_first_run=is_first_run)
        window.show()

        sys.exit(app.exec())

if __name__ == "__main__":
    main()
