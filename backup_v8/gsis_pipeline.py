from core.context_runner import GSISContextRunner


class GSISPipeline:


    def __init__(self, symbol):

        self.runner = GSISContextRunner(symbol)


    def execute_engine(self, name, engine):

        result = engine.run(
            self.runner.context.symbol
        )

        self.runner.push(
            name,
            result
        )

        return result


    def output(self):

        return self.runner.snapshot()
