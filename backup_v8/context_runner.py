from core.data_models import GSISContext


class GSISContextRunner:


    def __init__(self, symbol):

        self.context = GSISContext(
            symbol=symbol
        )


    def push(self, engine_name, output):

        self.context.update(
            engine_name,
            output
        )


    def get_context(self):

        return self.context


    def snapshot(self):

        return self.context.snapshot()
