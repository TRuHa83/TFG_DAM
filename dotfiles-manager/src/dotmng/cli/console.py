from dotmng.cli.printer      import Printer

class Console:
    def __init__(self, config):
        self.printer = Printer()

    def print(self, function, **kwargs):
        method = getattr(self.printer, function, None)

        if not method:
            return

        filtered_args = {k: v for k, v in kwargs.items() if v is not None}
        method(**filtered_args)

    def get_dotfiles(self, context):
        dotfiles = context.dotfiles
        self.printer.message(f"Encontrados {len(dotfiles)} archivos", "submenu", "")

    def gen_hash_dot(self, context):
        self.printer.message(
            f"Hash generado: [dim cyan]{context.hash[:7]}...[/dim cyan] para [dim cyan]{context.list_name}[/dim cyan]", "menu",
            "󰈙")

    def compare_hashes(self, context):
        if context.hash_equal:
            self.printer.tree("El hash coincide con el de al base de datos", "middel", "submenu", "󰌹")
            return

        self.printer.tree("El hash no coincide con el de la base de datos", "middel", "warning", "󰌺")

    def update_dot_hash(self, context):
        if context.halt:
            self.printer.tree("Error al actualizar la base de datos", "final", "error", "󰴀")
            return

        if not context.hash_equal or context.force:
            self.printer.tree("Base de datos actualizada", "final", "submenu", "󰗂")
            return

        self.printer.tree("No es necesario actualizar.", "final", "submenu", "󰪩")

    def identify_dotfiles(self, context):
        self.printer.message("Clasificando dotfiles...", "menu", "󰒺")

    def count_identify_dotfiles(self, context):
        self.printer.tree(f"Dotfiles clasificados: {len(context.dotfiles) - len(context.unknown_files)}", "middel", "success", "󱪚")
        self.printer.tree(f"Dotfiles desconocidos: {len(context.unknown_files)}", "final", "warning", "󱪠")

    def set_local_inventory(self, context):
        if context.halt:
            self.printer.message("Error al actualizar la base de datos.", "error", "󰴀")
            return

        self.printer.message("Inventario local guardado con éxito.", "submenu", "󰪩")

    def set_local_unknown(self, context):
        if context.halt:
            self.printer.message("Error al actualizar la base de datos.", "error", "󰴀")
            return

        self.printer.message("Inventario desconocido guardado con éxito.", "submenu", "󰪩")

    def unknown_toggle(self):
        self.printer.message("Error al actualizar la base de datos.", "error", "󰴀")

    def unbind_local_inventory(self):
        self.printer.message("Error al actualizar la base de datos.", "error", "󰴀")

    def locate_conflict(self, context):
        if context.halt:
            self.printer.message("Error al obtener los datos de la base de datos.", "error", "󰴀")
            return

        if len(context.conflicts) > 0:
            self.printer.message(f"Detectado {len(context.conflicts)} conflictos pendientes de resolver.", "warning", "")

    def gen_inform(self):
        self.printer.message("Error al obtener los datos de la base de datos.", "error", "󰴀")
