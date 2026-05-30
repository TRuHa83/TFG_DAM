from rich         import box
from rich.rule    import Rule
from rich.align   import Align
from rich.table   import Table
from rich.panel   import Panel
from rich.columns import Columns
from rich.console import Console


class Printer:
    def __init__(self):
        self.color = {
            "info": "bold bright_cyan", "warning": "bold gold1",
            "error": "bold red", "success": "bold green",
            "data": "bold blue", "menu": "bold dark_orange3",
            "submenu": "bold green4"
        }

        """
        ✔  ✘    ℹ  ⚡  󱇬  󰕘      󰌹" 󰌺  󰒺  󱪚  󱪠
          󰈙  󰗂  󰪩  󰴀          󰚰      └  ├ │
        """

        self.console = Console(color_system="truecolor")

    def init_app(self, version: str):
        title = (
        f"\n  ____        _    __ _ _                     __  __                                   \n"
        f" |  _ \\  ___ | |_ / _(_) | ___  ___          |  \\/  | __ _ _ __   __ _  __ _  ___ _ __ \n"
        f" | | | |/ _ \\| __| |_| | |/ _ \\/ __|  _____  | |\\/| |/ _` | '_ \\ / _` |/ _` |/ _ \\ '__|\n"
        f" | |_| | (_) | |_|  _| | |  __/\\__ \\ |_____| | |  | | (_| | | | | (_| | (_| |  __/ |   \n"
        f" |____/ \\___/ \\__|_| |_|_|\\___||___/         |_|  |_|\\__,_|_| |_|\\__,_|\\__, |\\___|_|\n"
        f"                                                                       |___/  v{version}\n"
        )

        print(title)
        self.jump()

    def first_message(self):
        self.console.print("\n  [bold italic]En primera ejecución:[/bold italic]")
        self.console.print("[bright_black]└[/bright_black] [white]# dotmng update[/white]\n")

    def jump(self):
        self.console.print()

    def task(self, text: str, color: str, icon: str):
        self.console.print(f"[{self.color[color]}]{icon} {text}[/{self.color[color]}]")

    def message(self, text: str, color: str, icon: str):
        self.console.print(f"  [{self.color[color]}]{icon}[/{self.color[color]}] {text}")

    def tree(self, text: str, poss: str ,color: str, icon: str):
        if poss == "middel":
            self.console.print(f"    [bright_black]├[/bright_black] [{self.color[color]}]{icon}[/{self.color[color]}] {text}")

        else:
            self.console.print(f"    [bright_black]└[/bright_black] [{self.color[color]}]{icon}[/{self.color[color]}] {text}\n")

    def show_apps(self, data, conflicts):
        # --- HEADER ---
        head = Table(
            title="[bold blue]󰒺 Desglose de Inventario[/bold blue]",
            border_style="blue",
            box=box.HORIZONTALS,
            width=80,
            pad_edge=False,
            show_header=True,
            show_footer=False,
            show_edge=True
        )

        head.add_column(" Aplicación", style="italic green", width=25)
        head.add_column("Archivos (Paths)", style="dim", width=15)
        head.add_column("App ID ", style="blue", justify="right", width=20)
        head.box.bottom = "   "
        self.console.print()
        self.console.print(head)

        # --- Renderizar por Bloques ---
        for parent in sorted(data.keys(), key=lambda x: "" if x is None else str(x)):
            display_parent = parent if parent is not None else "Sin Categoría"

            # Título de la Categoría como una línea divisoria (Rule)
            title = Rule(f"[bold cyan]󰉋 {display_parent}[/bold cyan]", style="cyan", align="left")
            self.console.print(title, width=80)

            # Tabla sin bordes verticales, solo un divisor bajo la cabecera (box=SIMPLE)
            table = Table(box=box.SIMPLE, show_header=False, width=80, pad_edge=False)
            table.add_column("Aplicación", style="italic green", width=25)
            table.add_column("Archivos (Paths)", style="dim", width=15)
            table.add_column("App ID", style="blue", justify="right", width=20)

            last_sub = None
            for (name, sub, app_id), paths in sorted(data[parent].items(), key=lambda item: tuple("" if x is None else str(x) for x in item[0])):
                # Mostrar la subcategoría solo la primera vez para mantenerlo limpio
                display_name = f"󰀻 {name}" if name != last_sub else ""
                paths_str = ", ".join(sorted(list(set(paths))))

                table.add_row(f"{'[gold1]' if app_id in conflicts else ''}{display_name}", f"{'[gold1]' if app_id in conflicts else ''}{paths_str}", f"{'[gold1]' if app_id in conflicts else ''}{app_id}")
                last_sub = name

            self.console.print(table)

        # --- FOOTER ---
        foot = Table(
            border_style="blue",
            box=box.HORIZONTALS,
            width=80,
            pad_edge=False,
            show_header=True,
            show_footer=False,
            show_edge=True
        )

        foot.add_column(" Aplicación", style="italic green", width=25)
        foot.add_column("Archivos (Paths)", style="dim", width=15)
        foot.add_column("App ID ", style="blue", justify="right", width=20)
        foot.box.bottom = "   "
        self.console.print(foot)

    def show_unknown(self, data):
        items = list(data.items())
        total = len(items)

        table = Table(box=None, show_header=True, pad_edge=False, collapse_padding=True, header_style="bold white")
        table.add_column("ID", justify="right", style="dim cyan", width=4)
        table.add_column(" · Dotfiles desconocidos", style="white", width=45)
        table.add_column("Estado", justify="center", width=8)

        for index, (key, value) in enumerate(items):
            # Lógica de dibujo del árbol (solo el último lleva la esquina)
            is_last = (index == total - 1)
            prefix = " └─" if is_last else " ├─"

            # Colores y Emojis
            is_enabled = value.get("enabled", False)
            if value["type"] == "folder":
                path_color = "bold dim cyan" if is_enabled else "dim cyan"
                emoji = "📂"
            else:
                path_color = "white" if is_enabled else "bright_black"
                emoji = "📄"

            # Construcción de la fila
            path_display = f"[dim white]{prefix}[/dim white] {emoji} [{path_color}]{value['path'][:38]}[/]"
            status = "[bold green]✔[/]" if is_enabled else "[bold red]✘[/]"

            table.add_row(
                str(index + 1),
                path_display,
                status
            )

        self.console.print(table)
        self.console.print()

        self.console.print("\n  [bold italic]Para cambiar el estado:[/bold italic]")
        self.console.print("[bright_black]└[/bright_black] [white]# dotmng unknown toggle --id [ID][/white]\n")

    def show_conflicts(self, conflicts):
        self.console.print("[bold gold1] ALERTAS DE CONFLICTO[/bold gold1] (Rutas duplicadas)")
        for path, entries in conflicts.items():
            num_apps = len(entries)
            # Cabecera del conflicto: archivo y número de apps
            self.console.print(
                f"  [bold dark_orange3]󱃔 {path}[/bold dark_orange3]")

            # Lista de IDs y nombres involucrados
            count = len(entries)
            for num, entry in enumerate(entries):
                self.console.print(f"    {"[bright_black]├[/bright_black]" if num < count - 1 else "[bright_black]└[/bright_black]"} [cyan]ID: {entry['id']}[/cyan] - [magenta]{entry['app_name']}[/magenta]")

        self.console.print("\n  [bold italic]Para resolverlo, desvincula el ID que no estés utilizando en el sistema:[/bold italic]")
        self.console.print("[bright_black]└[/bright_black] [white]# dotmng apps unbind --id [ID][/white]\n")

    def error(self, text: str, color: str, icon: str):
        self.console.print(f"\n[{self.color[color]}]{icon} {text}[/{self.color[color]}]")