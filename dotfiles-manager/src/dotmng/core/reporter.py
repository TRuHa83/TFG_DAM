from dotmng.modules import log_manager

class Reporter:
    def __init__(self, sender):
        self.sender = sender
        self.log = log_manager.setup_logger("PIPE")

    def send(self, function, context):
        method = getattr(self.sender, function, None)

        if method and callable(method):
            method(context)

        else:
            self.log.debug(f"El método '{function}' no existe en el sender '{self.sender.__class__.__name__}' o no es callable.")
