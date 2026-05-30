class Context:
    """
    Objeto dinámico para pasar información entre los pasos del pipeline.
    Contiene los parámetros de entrada y almacena los resultados.
    """

    def __init__(self, **kwargs):
        self.halt = False   # Si un paso lo pone a True, el pipeline se detiene
        self.error = None   # Para capturar excepciones controladas
        self.success = True # Indica si se ha realizado la tarea
        self.jump = False   # Salta a la siguiente tarea

        # Guardamos cualquier parámetro dinámico (ej. args.force, args.name)
        for key, value in kwargs.items():
            setattr(self, key, value)


