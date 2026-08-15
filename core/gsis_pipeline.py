from core.context_runner import GSISContextRunner


class GSISPipeline:


    def __init__(self, symbol):

        self.runner = GSISContextRunner(symbol)



    def execute_engine(self, name, engine):

        result = engine.execute(
            self.runner.context
        )


        self.runner.update(
            name.lower(),
            result
        )


        return result



    def output(self):

        return self.runner.snapshot()
