class ModularEngine:
    def __init__(self, name, engine):
        self.name = name
        self.engine = engine

    def execute(self, context):
        # New-style engines
        if hasattr(self.engine, "run"):
            try:
                return self.engine.run(context)
            except TypeError:
                pass

        # Legacy engines
        if hasattr(self.engine, "execute"):
            return self.engine.execute(context)

        raise RuntimeError(
            f"{self.name} has no compatible run() or execute() method."
        )
