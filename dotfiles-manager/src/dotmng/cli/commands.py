from dotmng.modules          import DataBase

from dotmng.cli.console      import Console
from dotmng.cli.printer      import Printer

from dotmng.core.pipelines   import Pipeline
from dotmng.core.reporter    import Reporter
from dotmng.core.context     import Context
from dotmng.core.steps       import *


class CMD:
    def __init__(self, config, log):
        self.base_path = config.DATA_DIR
        self.db_path = config.DB_PATH

        self.printer = Printer()
        self.log = log

        self.console = Console(config)
        self.reporter = Reporter(self.console)

        self.home_path = Path.home()
        self.conf_path = self.home_path.joinpath(".config")

        self.db = DataBase(self.db_path)

    def check(self, arg):
        self.console.print(function="task", text="COMPROBANDO DOTFILES.", color="info", icon="󰕘")

        context = Context(
            path=self.home_path,
            session=self.db,
            reporter=self.reporter,
            startswith=".",
        )

        steps = [
            get_hash_dot(input_attr="ALL_DOTFILES"),
            get_dotfiles,
            gen_hash_dot(input_attr="dotfiles"),
            compare_hashes(value="ALL_DOTFILES")
        ]

        pipeline = Pipeline(steps)
        result = pipeline.run(context)

        if result.error:
            self.log.error(result.error)
            return None

        if result.halt:
            if not result.hash:
                self.console.print(function="first_message")
                return None

        if result.hash_equal:
            self.console.print(function="tree", text="No es necesario actualizar.", poss="final", color="success", icon="󰪩")

        else:
            self.console.print(function="tree", text="Es necesario actualizar.", poss="final", color="warning", icon="󰪩")

        return result

    def update(self, args):
        self.console.print(function="task", text=f"IDENTIFICANDO APLICACIONES.", color="info", icon="󰕘")

        context = Context(
            path=self.home_path,
            session=self.db,
            reporter=self.reporter,
            log=self.log,
            force=False if not args.force else True,
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
        result = pipeline.run(context)

        if result.error:
            self.console.print(function="error", text="Error en la operacion, no se ha podido completar la acción", color="error", icon="⚠")
            self.log.error(result.error)
            return result

        elif result.halt:
            return result

        else:
            if result.conflicts:
                self.console.print(function="jump")
                self.console.print(function="show_conflicts", conflicts=result.conflicts)

        return result

    def apps_check(self, args):
        self.console.print(function="task", text="COMPROBANDO DOTFILES.", color="info", icon="󰕘")

        context = Context(
            path=self.home_path,
            session=self.db,
            reporter=self.reporter,
            log=self.log,
            startswith=".",
        )

        steps = [
            get_dotfiles,
            identify_dotfiles,
            filter_ignore,
            gen_hash_dot(input_attr="known_apps"),
            compare_hashes(value="KNOWNS")
        ]

        pipeline = Pipeline(steps)
        result = pipeline.run(context)

        if result.error:
            self.log.error(result.error)
            return None

        if result.halt:
            if not result.hash:
                self.console.print(function="first_message")
                return None

        if result.hash_equal:
            self.console.print(function="tree", text="No es necesario actualizar.", poss="final", color="success", icon="󰪩")

        else:
            self.console.print(function="tree", text="Es necesario actualizar.", poss="final", color="warning", icon="󰪩")

        return result

    def apps_list(self, args):
        context = Context(
            session = self.db,
            reporter=self.reporter
        )

        steps = [
            locate_conflict,
            gen_inform
        ]

        pipeline = Pipeline(steps)
        result = pipeline.run(context)

        conflicts = []
        for key, value in result.conflicts.items():
            for v in value:
                conflicts.append(v["app_id"])

        if result.error:
            self.console.error("Error en la operacion, no se ha podido completar la acción", "error", "⚠")
            self.log.error(result.error)
            return result

        else:
            self.console.print(function="show_apps", data=result.data, conflicts=conflicts)

            if result.conflicts:
                self.console.print(function="show_conflicts", conflicts=result.conflicts)

    def apps_bind(self, args):
        context = Context(
            session=self.db,
            reporter=self.reporter,
            log=self.log,
            id_app=args.id
        )

        steps = [
            bind_local_inventory
        ]

        pipeline = Pipeline(steps)
        result = pipeline.run(context)

        if result.error:
            self.console.print(function="error", text="Error en la operacion, no se ha podido completar la acción", color="error", icon="⚠")
            self.log.error(result.error)
            return result

        self.console.print(function="message", text="Desvinculado con éxito.", color="success", icon="✔")
        self.console.print(function="jump")

        return result

    def apps_unbind(self, args):
        context = Context(
            session=self.db,
            reporter=self.reporter,
            log=self.log,
            id_app=args.id
        )

        steps = [
            unbind_local_inventory
        ]

        pipeline = Pipeline(steps)
        result = pipeline.run(context)

        if result.error:
            self.console.print(function="error", text="Error en la operacion, no se ha podido completar la acción", color="error", icon="⚠")
            self.log.error(result.error)
            return result

        self.console.print(function="message", text="Desvinculado con éxito.", color="success", icon="✔")
        self.console.print(function="jump")

        return result

    def unknown_check(self, args):
        self.console.print(function="task", text="COMPROBANDO DOTFILES DESCONOCIDOS.", color="info", icon="󰕘")

        context = Context(
            reporter=self.reporter,
            path=self.home_path,
            session=self.db,
            log=self.log,
            startswith=".",
        )

        steps = [
            get_dotfiles,
            identify_dotfiles,
            filter_ignore,
            gen_hash_dot(input_attr="unknown_files"),
            compare_hashes(value="UNKNOWNS")
        ]

        pipeline = Pipeline(steps)
        result = pipeline.run(context)

        if result.error:
            self.log.error(result.error)
            return None

        if result.halt:
            if not result.hash:
                self.console.print(function="first_message")
                return None

        if result.hash_equal:
            self.console.print(function="tree", text="No es necesario actualizar.", poss="final", color="success", icon="󰪩")

        else:
            self.console.print(function="tree", text="Es necesario actualizar.", poss="final", color="warning", icon="󰪩")

        return result

    def unknown_list(self, args):
        context = Context(
            session=self.db,
            reporter=self.reporter
        )

        steps = [
            get_local_unknown
        ]

        pipeline = Pipeline(steps)
        result = pipeline.run(context)

        if result.error:
            self.console.print(function="error", text="Error al acceder a la base de datos.", color="error", icon="󰴀")
            self.log.error(result.error)
            return result

        self.console.print(function="show_unknown", data=result.local_unknown)
        return result


    def unknown_link(self, args):
        pass

    def unknown_unlink(self, args):
        pass

    def unknown_toggle(self, args):
        context = Context(
            reporter=self.reporter,
            session=self.db,
            id=args.id
        )

        steps = [
            unknown_toggle
        ]

        pipeline = Pipeline(steps)
        result = pipeline.run(context)

        if result.error:
            self.console.print(function="error", text="Error en la operacion, no se ha podido completar la acción", color="error", icon="⚠")
            self.log.error(result.error)
            return result

        self.console.print(function="message", text="Regla de exclusión actualizada con éxito.", color="success", icon="✔")
        self.console.print(function="jump")

        return result


    def utils_list(self, args):
        pass

    def utils_add(self, args):
        pass

    def utils_rm(self, args):
        pass

    def utils_toggle(self, args):
        pass
