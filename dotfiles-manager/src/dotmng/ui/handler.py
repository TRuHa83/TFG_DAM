from datetime import datetime

from PySide6.QtCore import QObject, Signal


class Handler(QObject):
    ui_signal = Signal(str, object)
    update_widget_signal = Signal(str, object, object)

    def __init__(self):
        super().__init__()
        self.halt = False

    def update_label(self, context):
        if self.halt:
            return

        self.ui_signal.emit("check_dotfiles", context)

    def gen_hash_dot(self, context):
        pass

    def compare_hashes(self, context):
        led_green = ":/assets/icons/led_green.svg"
        led_red = ":/assets/icons/led_red.svg"

        match context.list_name:
            case "ALL_DOTFILES":
                self.update_widget_signal.emit("led_dotfiles", led_green if context.hash_equal else led_red, True)

            case "KNOWNS":
                self.update_widget_signal.emit("led_apps", led_green if context.hash_equal else led_red, True)

            case "UNKNOWNS":
                self.update_widget_signal.emit("led_unknown", led_green if context.hash_equal else led_red, True)

    def get_current_time(self):
        return datetime.now()
