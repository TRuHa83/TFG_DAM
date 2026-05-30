from dotmng.modules import log_manager

from .commands import CMD
from .create import create_parser


class CLI:
    def __init__(self, config):
        self.__version__ = config.__version__
        self.__author__  = config.__author__
        self.__name__    = config.__name__

        self.log = log_manager.setup_logger("CLI")

        self.cmd = CMD(config, self.log)
        self.parser, self.subparsers = create_parser(config, self.cmd)
        self.log.info("Command Line Interface inicializada")

        # === INFO ===
        info_parser = self.subparsers.add_parser('info', help='Muestra información del sistema y configuración actual')

        # === VERSION ===
        version_parser = self.subparsers.add_parser('version', help='Muestra la versión del programa')

        # === HELP ===
        help_parser = self.subparsers.add_parser('help', help='Muestra esta ayuda')

        # === UNINSTALL ===
        uninstall_parser = self.subparsers.add_parser('uninstall', help='Desinstala dotmng del sistema')

    def info(self):
        self.log.info("Mostrando información de la aplicación")
        print("[|] Información:")
        print(f"[*] Versión: {self.__version__}")
        print(f"[*] Autor: {self.__author__}")

    def version(self):
        self.log.info("Mostrando versión del programa")
        print(self.__version__)

    def help(self):
        self.log.info("Mostrando ayuda")
        from dotmng.cli.printer import Printer
        Printer().init_app(self.__version__)
        self.parser.print_help()

    def uninstall(self):
        import os
        import subprocess

        from dotmng.cli.printer import Printer
        printer = Printer()

        self.log.info("Desinstalando dotmng")
        
        printer.message("Iniciando desinstalación...", "info", "⚙")
        
        # Eliminar archivos del escritorio
        apps_dir = os.path.expanduser("~/.local/share/applications")
        icons_dir = os.path.expanduser("~/.local/share/icons")
        
        desktop_file = os.path.join(apps_dir, "dotmng.desktop")
        icon_file = os.path.join(icons_dir, "dotmng.png")
        
        if os.path.exists(desktop_file):
            os.remove(desktop_file)
            printer.task("Entrada de escritorio eliminada.", "success", "✔")
            
        if os.path.exists(icon_file):
            os.remove(icon_file)
            printer.task("Icono eliminado.", "success", "✔")
            
        # Desinstalar mediante uv
        printer.message("Desinstalando herramienta a través de uv...", "info", "⚙")
        try:
            subprocess.run(["uv", "tool", "uninstall", "dotfiles-manager"], check=True)
            printer.task("dotmng desinstalado correctamente.", "success", "✔")

        except subprocess.CalledProcessError:
            printer.error("Error al desinstalar con uv. Es posible que no estuviese instalado.", "error", "✖")

        except FileNotFoundError:
            printer.error("uv no se encuentra instalado en el sistema.", "error", "✖")

    def run(self, args):
        parsed_args = self.parser.parse_args(args)

        if parsed_args.category == 'info':
            self.info()

        elif parsed_args.category == 'version':
            self.version()

        elif parsed_args.category == 'help':
            self.help()

        elif parsed_args.category == 'uninstall':
            self.uninstall()

        elif parsed_args.category in ['apps', 'unknown', 'utils'] and getattr(parsed_args, 'command', None) is None:
            from dotmng.cli.printer import Printer
            printer = Printer()
            printer.error(f"Error: Se requiere un subcomando para '{parsed_args.category}'.", "error", "⚠")
            printer.console.print(f"  Utiliza [bold cyan]dotmng {parsed_args.category} help[/bold cyan] para ver las opciones disponibles.\n")

        elif hasattr(parsed_args, 'func'):
            parsed_args.func(parsed_args)

        else:
            from dotmng.cli.printer import Printer
            Printer().init_app(self.__version__)
            self.parser.print_help()

