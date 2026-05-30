from .api    import ServerPoller, TaskPoller, AppClient
from .logger import Logger

log_manager = Logger()

log_main = log_manager.setup_logger("MAIN")
log_pipe = log_manager.setup_logger("PIPE")
log_cli  = log_manager.setup_logger("CLI")
log_ui   = log_manager.setup_logger("UI")
log_db   = log_manager.setup_logger("DB")

from .database import (
    DataBase, UI_Preferences, ServerConfig,
    OSDistroMapping, KnownAppsReference,
    GlobalIgnoreRules
)