from core.registry.engine_registry import EngineRegistry


class EngineLoader:


    def __init__(self):

        self.registry = EngineRegistry()


    def load(self, name, engine):

        self.registry.register(
            name,
            engine
        )


    def get(self, name):

        return self.registry.get(name)


    def status(self):

        return {
            "loaded_engines":
            self.registry.list_engines(),

            "count":
            len(self.registry.list_engines())
        }
