from dotmng.modules          import DataBase

from dotmng.core.pipelines   import Pipeline
from dotmng.core.reporter    import Reporter
from dotmng.core.context     import Context
from dotmng.core.steps       import *

from PySide6.QtCore import QThread


def build_check_steps(mode: str) -> list:
    _all_dotfiles = lambda: [
        get_dotfiles,
        gen_hash_dot(input_attr="dotfiles"),
        compare_hashes(value="ALL_DOTFILES"),
    ]
    _knowns = lambda: [
        gen_hash_dot(input_attr="known_apps"),
        compare_hashes(value="KNOWNS"),
    ]
    _unknowns = lambda: [
        gen_hash_dot(input_attr="unknown_files"),
        compare_hashes(value="UNKNOWNS"),
    ]

    flows = {
        "RESUME_ALL": lambda: [get_hash_dot(input_attr="ALL_DOTFILES"), *_all_dotfiles()],
        "KNOWNS":     lambda: [get_dotfiles, identify_dotfiles, filter_ignore, *_knowns()],
        "UNKNOWNS":   lambda: [get_dotfiles, identify_dotfiles, filter_ignore, *_unknowns()],
    }

    return flows[mode]()

class Worker(QThread):
    def __init__(self, config, task):
        super().__init__()
        self.task = task
        self.base_path = config["config"].DATA_DIR
        self.db_path = config["config"].DB_PATH

        self.handler = config["handler"]
        self.log = config["log"]

        self.home_path = Path.home()
        self.conf_path = self.home_path.joinpath(".config")

        self.db = DataBase(self.db_path)

    def run(self):
        funct = next(iter(self.task))
        flows = self.task[funct]

        method = getattr(self, funct, None)
        if method and callable(method):
            method(flows)

        else:
            self.log.error(f"La tarea '{self.task}' no existe en el Worker.")

    def check_action(self, flow: dict):
        reporter = Reporter(self.handler)

        context = Context(
            path=self.home_path,
            session=self.db,
            reporter=reporter,
            log=self.log,
            startswith=".",
        )

        steps = build_check_steps(flow["action"])
        pipeline = Pipeline(steps)
        pipeline.run(context)

    def update_action(self, flow: dict):
        reporter = Reporter(self.handler)

        context = Context(
            path=self.home_path,
            session=self.db,
            reporter=reporter,
            log=self.log,
            force=True,
            startswith=".",
        )

        steps = [
            get_dotfiles,
            gen_hash_dot(input_attr="dotfiles"),
            compare_hashes(value="ALL_DOTFILES"),
            update_dot_hash,
            identify_dotfiles,
            filter_ignore,
            gen_hash_dot(input_attr="known_apps"),
            compare_hashes(value="KNOWNS"),
            update_dot_hash,
            gen_hash_dot(input_attr="unknown_files"),
            compare_hashes(value="UNKNOWNS"),
            update_dot_hash,
            set_local_inventory,
            set_local_unknown,
            locate_conflict
        ]

        pipeline = Pipeline(steps)
        pipeline.run(context)
