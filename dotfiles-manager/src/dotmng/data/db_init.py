import json

from importlib.resources import files

from dotmng.modules import log_manager


# ---------------------------------------------------------------------------
# Reglas de exclusión globales por defecto
# ---------------------------------------------------------------------------

_DEFAULT_IGNORE_RULES = [
    ["(^|/)\\.config(/|$)",                     "REGEX"],
    ["(^|/)\\.cache(/|$)",                      "REGEX"],
    ["(^|/)\\.local(/|$)",                      "REGEX"],
    ["(^|/)\\.var(/|$)",                        "REGEX"],
    ["(^|/)\\.npm(/|$)",                        "REGEX"],
    ["(^|/)\\.nvm(/|$)",                        "REGEX"],
    ["(^|/)\\.asdf(/|$)",                       "REGEX"],
    ["(^|/)\\.m2(/|$)",                         "REGEX"],
    ["(^|/)\\.mvn(/|$)",                        "REGEX"],
    ["(^|/)\\.dotnet(/|$)",                     "REGEX"],
    ["(^|/)\\.jdks(/|$)",                       "REGEX"],
    ["(^|/)\\.java(/|$)",                       "REGEX"],
    ["(^|/)\\.platformio(/|$)",                 "REGEX"],
    ["(^|/)\\.wget-hsts(/|$)",                  "REGEX"],
    ["(^|/)\\.lesshst(/|$)",                    "REGEX"],
    ["(^|/)\\.pki(/|$)",                        "REGEX"],
    ["(^|/)\\.sudo_as_admin_successful(/|$)",   "REGEX"],
    [".bak",                                "EXTENSION"],
    [".swp",                                "EXTENSION"],
    [".tmp",                                "EXTENSION"],
    [".log",                                "EXTENSION"],
    [".cache",                              "EXTENSION"],
    ["_history$",                               "REGEX"],
    ["-hsts$",                                  "REGEX"],
    ["~$",                                      "REGEX"],
    ["pid$",                                    "REGEX"],
]


# ---------------------------------------------------------------------------
# Funciones internas de seed
# ---------------------------------------------------------------------------

def _seed_ignore_rules(db) -> None:
    """Inserta las reglas de exclusión globales por defecto."""
    from dotmng.modules.database.models import GlobalIgnoreRules

    log = log_manager.setup_logger("DB_INIT")
    log.info("Seed: insertando reglas de exclusión globales...")

    rules = [
        GlobalIgnoreRules(pattern=pattern, match_type=match_type)
        for pattern, match_type in _DEFAULT_IGNORE_RULES
    ]
    db.set_global_ignore_rules(rules)
    log.info(f"Seed: {len(rules)} reglas de exclusión insertadas.")


def _seed_known_apps(db) -> None:
    """Inserta las aplicaciones conocidas desde el JSON incluido en el paquete."""
    from dotmng.modules.database.models import KnownAppsReference

    log = log_manager.setup_logger("DB_INIT")
    log.info("Seed: cargando apps conocidas desde package data...")

    # Leer el JSON mediante importlib.resources (compatible con pip install)
    json_text = files("dotmng.data").joinpath("xdg_data.json").read_text(encoding="utf-8")
    data_apps: dict = json.loads(json_text)

    log.info(f"Seed: {len(data_apps)} apps encontradas en xdg_data.json")

    apps = []
    for key, value in data_apps.items():
        # --- Categoría principal ---
        main = db.get_categories_app(category=value["category"])
        if not main:
            new_cat_id = db.set_categories(value["category"])
            main = {"id_cat": new_cat_id}

        # --- Subcategoría ---
        sub_main = db.get_categories_app(category=value["subcategory"])
        if not sub_main:
            new_sub_id = db.set_categories(value["subcategory"], parent_id=main["id_cat"])
            sub_main = {"id_cat": new_sub_id}

        # Asignar subcategoría; si no existe, usar la principal
        asig_cat = sub_main["id_cat"] if sub_main["id_cat"] else main["id_cat"]

        apps.append(KnownAppsReference(
            app_id=key,
            app_name=value["app_name"],
            category_id=asig_cat,
            files_info_json=str(value["files_info_json"]),
            packages_json=str(value["packages_json"]),
        ))

    db.set_known_apps(apps)
    log.info(f"Seed: {len(apps)} apps conocidas insertadas correctamente.")


# ---------------------------------------------------------------------------
# Punto de entrada público
# ---------------------------------------------------------------------------

def initialize_database(db) -> None:
    log = log_manager.setup_logger("DB_INIT")
    log.info("Iniciando seed de datos por defecto...")

    try:
        _seed_ignore_rules(db)
        _seed_known_apps(db)
        log.info("Seed completado con éxito.")

    except Exception as e:
        log.error(f"Error durante el seed de la base de datos: {e}")
        raise
