class ModularEngine:

    def __init__(self, name, engine):
        self.name = name
        self.engine = engine


    def execute(self, context):

        if hasattr(self.engine, "run"):

            return self.engine.run(context)


        elif hasattr(self.engine, "execute"):

            return self.engine.execute(context)


        else:

            raise RuntimeError(
                f"{self.name} has no run() or execute() method"
            )
