from .customs  import argparse, CustomFormatter


def print_subparser_help(cfg, subparser):
    from dotmng.cli.printer import Printer
    Printer().init_app(cfg.__version__)
    subparser.print_help()


def create_parser(cfg, cmd):
    parser = argparse.ArgumentParser(
        prog=cfg.__app__,
        description="Gestor de dotfiles y aplicaciones para usuarios",
        epilog=f"Run '{cfg.__app__} COMMAND help' for more information.",
        formatter_class=CustomFormatter,
        add_help=False,
        usage="%(prog)s [OPTIONS] COMMAND"
    )
    
    subparsers = parser.add_subparsers(title="Commands", dest="category")

    # === CHECK ===
    check_parser = subparsers.add_parser("check", help="Comprueba rápidamente si hay cambios (Macro-Hash)")
    check_parser.set_defaults(func=cmd.check)

    # === UPDATE ===
    update_parser = subparsers.add_parser('update', help='Actualiza los registros de aplicaciones en la DB')
    update_parser.add_argument('--force', '-f', action='store_true', help='Fuerza la actualización de las aplicaciones')
    update_parser.set_defaults(func=cmd.update)

    # === APPS ===
    apps_parser = subparsers.add_parser('apps', help='Gestion de aplicaciones instaladas en el sistema')
    apps_subs = apps_parser.add_subparsers(title='Options', dest="command")
    apps_parser.formatter_class = CustomFormatter

    # --- check ---
    apps_list = apps_subs.add_parser("check", help="Comprueba rápidamente si hay cambios (Macro-Hash)")
    apps_list.set_defaults(func=cmd.apps_check)

    # --- list ---
    apps_list = apps_subs.add_parser("list", help="Lista las aplicaciones registradas en la DB")
    apps_list.add_argument('--category', '-c', type=str, help='Filtra las aplicaciones por categoría')
    apps_list.set_defaults(func=cmd.apps_list)

    # --- bind ---
    apps_add = apps_subs.add_parser('bind', help='Registra manualmente aplicaciones en la DB')
    apps_add.add_argument('--id', type=str, required=True, help='ID de la aplicación')
    apps_add.set_defaults(func=cmd.apps_bind)

    # --- unbind ---
    apps_rm = apps_subs.add_parser('unbind', help='Elimina registro de una aplicaciones de la DB')
    apps_rm.add_argument('--id', type=str, required=True, help='ID de la aplicación')
    apps_rm.set_defaults(func=cmd.apps_unbind)

    # --- help ---
    apps_help = apps_subs.add_parser("help", help="Muestra esta ayuda")
    apps_help.set_defaults(func=lambda args: print_subparser_help(cfg, apps_parser))


    # === UNKNOWN ===
    unknown_parser = subparsers.add_parser('unknown', help='Comando desconocido para pruebas')
    unk_subs = unknown_parser.add_subparsers(title='Commands', dest="command")
    unknown_parser.formatter_class = CustomFormatter
    
    # --- list ---
    unk_list = unk_subs.add_parser('list', help='Lista las aplicaciones desconocidas')
    unk_list.add_argument('--type', '-t', choices=['file', 'folder'], help='Filtra por tipo')
    unk_list.set_defaults(func=cmd.unknown_list)

    # --- check ---
    unk_check = unk_subs.add_parser("check", help="Comprueba rápidamente si hay cambios (Macro-Hash)")
    unk_check.set_defaults(func=cmd.unknown_check)

    # --- toggle ---
    unk_ignore = unk_subs.add_parser('toggle', help='Añade un desconocido a las reglas de exclusión')
    unk_ignore.add_argument('--id', type=str, required=True, help='ID del dotfile')
    unk_ignore.set_defaults(func=cmd.unknown_toggle)

    # --- help ---
    unk_help = unk_subs.add_parser("help", help="Muestra esta ayuda")
    unk_help.set_defaults(func=lambda args: print_subparser_help(cfg, unknown_parser))


    # === UTILS ===
    utils_parser = subparsers.add_parser('utils', help='Utilidades varias para la gestión del sistema')
    utils_subs = utils_parser.add_subparsers(title='Commands', dest="command")
    utils_parser.formatter_class = CustomFormatter
    
    # --- list ---
    utils_list = utils_subs.add_parser('list', help='Lista las reglas de exclusión')
    utils_list.add_argument('--type', '-t', choices=['EXTENSION', 'REGEX', 'EXACT'], help='Filtra por tipo [EXTENSION | REGEX | EXACT]')
    utils_list.set_defaults(func=cmd.utils_list)

    # --- add ---
    utils_add = utils_subs.add_parser('add', help='Añade una regla de exclusión')
    utils_add.add_argument('--type', '-t', choices=['EXTENSION', 'REGEX', 'EXACT'], required=True, help='Tipo de regla')
    utils_add.add_argument('--pattern', '-p', type=str, required=True, help='Patrón de la regla')
    utils_add.set_defaults(func=cmd.utils_add)

    # --- remove ---
    utils_rm = utils_subs.add_parser('remove', help='Elimina una regla de exclusión')
    utils_rm.add_argument('--id', '-i', type=int, required=True, help='ID de la regla a eliminar')
    utils_rm.set_defaults(func=cmd.utils_rm)

    # --- toggle ---
    utils_toggle = utils_subs.add_parser('toggle', help='Activa o desactiva una regla de exclusión')
    utils_toggle.add_argument('--id', '-i', type=int, required=True, help='ID de la regla')
    utils_toggle.set_defaults(func=cmd.utils_toggle)

    # --- help ---
    utils_help = utils_subs.add_parser("help", help="Muestra esta ayuda")
    utils_help.set_defaults(func=lambda args: print_subparser_help(cfg, utils_parser))
    
    return parser, subparsers