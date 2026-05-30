import re
import ast
import json
import hashlib

from pathlib import Path


""" RECUPERA LOS DOTFILES DEL USUARIO """
def get_dotfiles(context):
    # Obtenemos la ruta
    path = context.path
    files_home = Path.iterdir(path)

    reporter = context.reporter

    dotfiles = []
    # Iteramos los archivos en busca de dotfiles
    for files in files_home:
        if files.name.startswith(context.startswith):
            # Clasificamos los dotfiles
            dotfiles.append({
                "path": files.name,
                "type": "file" if files.is_file() or files.is_symlink() else "folder"
            })

    # Ordenamos los dotfiles por nombre
    context.dotfiles = sorted(dotfiles, key=lambda x: x["path"])

    reporter.send("get_dotfiles", context)
    return context

""" OBTIENE EL HASH ALMACENADO """
def get_hash_dot(input_attr):

    def hashes(context):
        context.list_name = input_attr

        # Recupera el hash de la DB
        db = context.session
        hashed = db.get_system_state_hashes(input_attr)

        context.hash = hashed.current_hash if hashed else None
        context.count = hashed.item_count if hashed else 0
        context.last_checked_at = hashed.last_checked_at  if hashed else None

        if not context.hash:
            context.halt = True

        return context

    return hashes

""" GENERA EL HASH DE UNA CADENA DE TEXTO """
def gen_hash_dot(input_attr):

        def hashes(context):
            reporter = context.reporter

            # Obtenemos el string
            dot_list = getattr(context, input_attr, None)
            if dot_list is None:
                return context

            # Convertimos a String
            dot_str = json.dumps(dot_list)

            # Generamos el hash
            context.list_name = input_attr
            context.hash = hashlib.md5(dot_str.encode('utf-8')).hexdigest()
            context.count = len(dot_list)

            reporter.send("gen_hash_dot", context)
            return context

        return hashes

""" RECUPERA EL HASH DE LA BD Y LO COMPARA """
def compare_hashes(value):

    def compare(context):
        reporter = context.reporter
        context.list_name = value

        # Recupera el hash de la DB
        db = context.session
        last_hash = db.get_system_state_hashes(value)

        # Compara si son iguales
        if not last_hash is None and last_hash.current_hash == context.hash:
            context.hash_equal = True
            reporter.send("compare_hashes", context)
            return context

        context.hash_equal = False

        reporter.send("compare_hashes", context)
        return context

    return compare

""" ACTUALIZA EL HASH DE LA BD """
def update_dot_hash(context):
    reporter = context.reporter

    # Comprueba si necesita actualizar o modo forzado activo
    if not context.hash_equal or context.force:
        try:
            # Actualiza el hash en la DB
            db = context.session
            db.set_system_state_hashes(context.hash, context.count, context.list_name)
            reporter.send("update_dot_hash", context)

        except Exception as e:
            context.halt = True
            context.error = e
            reporter.send("update_dot_hash", context)
            return context

    else:
        reporter.send("update_dot_hash", context)
        context.halt = True

    return context

""" IDENTIFICA Y CLASIFICA LOS DOTFILES """
def identify_dotfiles(context):
    reporter = context.reporter
    reporter.send("identify_dotfiles", context)

    dotfiles = context.dotfiles

    db = context.session
    apps_ref = db.get_known_apps()
    context.apps_ref = apps_ref

    unknown_files = []
    known_apps = []
    for dotf in dotfiles:
        ignore = False
        for app in apps_ref:
            app_ref = ast.literal_eval(app.files_info_json)
            for ar in app_ref:
                if dotf["path"] == ar["path"] and dotf["type"] == ar["type"]:
                    known_apps.append({
                        "path": dotf["path"],
                        "type": dotf["type"],
                        "app_id": app.app_id
                    })

                    ignore = True
                    break

        if not ignore:
            unknown_files.append(dotf)

    context.known_apps = known_apps
    context.unknown_files = unknown_files

    reporter.send("count_identify_dotfiles", context)
    return context

""" FILTRA IGNORADOS DE APPS"""
def filter_ignore(context):
    home_path = context.path
    db = context.session
    log = getattr(context, "log", None)
    ignores = db.get_global_ignore_rules()

    def apply_filter(data):
        for key, value in ignores.items():
            for d in data:
                path = d['path']
                if value['enabled']:
                    match = value['match_type']
                    if match == "REGEX":
                        if re.search(value['pattern'], path):
                            if log:
                                log.info(f"Excluido por regex: {path}")
                            data.remove(d)

                    elif match == "EXTENSION":
                        file = Path(home_path / path)
                        if file.is_file() and file.suffix == value['pattern']:
                            if log:
                                log.info(f"Excluido por extension: {path}")
                            data.remove(d)

                    elif match == "EXACT":
                        if path == value['pattern']:
                            if log:
                                log.info(f"Excluido por nombre exacto: {path}")
                            data.remove(d)

        return data

    context.known_apps = apply_filter(context.known_apps)
    context.unknown_files = apply_filter(context.unknown_files)

    return context

""" OBTIENE EL INVENTARIO LOCAL """
def get_local_inventory(context):
    try:
        db = context.session

        local_inventory = db.get_local_inventory()
        context.local_inventory = local_inventory

        return context

    except Exception as e:
        context.halt = True
        context.error = e
        return context

""" ACTUALIZA EL INVENTARIO LOCAL """
def set_local_inventory(context):
    reporter = context.reporter

    try:
        db = context.session

        known_apps = context.known_apps
        local_inventory = db.set_local_inventory(known_apps)
        context.local_inventory = local_inventory

        reporter.send("set_local_inventory", context)
        return context

    except Exception as e:
        context.halt = True
        context.error = e

        reporter.send("set_local_inventory", context)
        return context

""" OBTIENE EL INVENTARIO LOCAL """
def get_local_unknown(context):
    try:
        db = context.session

        local_unknown = db.get_local_unknown()
        context.local_unknown = local_unknown

        return context

    except Exception as e:
        context.halt = True
        context.error = e
        return context


def set_local_unknown(context):
    reporter = context.reporter

    try:
        db = context.session

        unknown_files = context.unknown_files
        local_unknown = db.set_local_unknown(unknown_files)
        context.local_unknown = local_unknown

        reporter.send("set_local_unknown", context)
        return context

    except Exception as e:
        context.halt = True
        context.error = e

        reporter.send("set_local_unknown", context)
        return context

""" DESHABILITA DOTFILE DESCONOCIDO """
def unknown_toggle(context):
    reporter = context.reporter
    id = context.id
    db = context.session

    try:
        # Obtener el archivo desconocido por su id para tener el path estable
        unknown = db.get_local_unknown_by_id(id)
        if not unknown:
            reporter.send("unknown_toggle", context)
            return context

        # Leer el estado efectivo actual (LEFT JOIN ya calculado en get_local_unknown)
        current = db.get_local_unknown()
        current_enabled = current.get(id, {}).get("enabled", True)

        # Invertir el estado y guardar el override
        new_enabled = not current_enabled
        db.set_user_unknown_override(unknown["path"], new_enabled)

    except Exception as e:
        reporter.send("unknown_toggle", context)

    return context

""" VINCULA APP AL INVENTARIO LOCAL"""
def bind_local_inventory(context):
    reporter = context.reporter
    id_app = context.id_app

    try:
        db = context.session
        app = db.get_local_inventory_by_id(id_app)
        db.set_user_inventory_override(app_id=app.get("app_id"), enabled=True)

    except Exception as e:
        reporter.send("bind_local_inventory", context)
        context.error = True

    return context

""" DESVINCULA APP DEL INVENTARIO LOCAL"""
def unbind_local_inventory(context):
    reporter = context.reporter
    id_app = context.id_app

    try:
        db = context.session
        app = db.get_local_inventory_by_id(id_app)
        db.set_user_inventory_override(app_id=app.get("app_id"), enabled=False)

    except Exception as e:
        reporter.send("unbind_local_inventory", context)
        context.error = True

    return context

""" LOCALIZA CONFLICTOS """
def locate_conflict(context):
    reporter = context.reporter
    try:
        db = context.session
        conflicts = db.get_local_conflicts()
        context.conflicts = conflicts

        if conflicts:
            reporter.send("locate_conflict", context)

        return context

    except Exception as e:
        context.halt = True
        context.error = e

        reporter.send("locate_conflict", context)
        return context

""" GENERA EL INFORME """
def gen_inform(context):
    reporter = context.reporter
    try:
        db = context.session
        data = db.get_local_for_inform()

        context.data = data
        return context

    except Exception as e:
        context.halt = True
        context.error = e

        reporter.send("gen_inform", context)
        return context
