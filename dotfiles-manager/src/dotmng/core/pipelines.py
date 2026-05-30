from .context import Context


class Pipeline:
    def __init__(self, steps: list):
        self.steps = steps

    def run(self, context: Context) -> Context:
        for step in self.steps:
            # Si un paso anterior falló o pidió detenerse, abortamos el bucle
            if context.halt or context.error:
                break

            if not context.jump:
                # Ejecutamos el paso pasándole el contexto actual
                context = step(context)

        return context