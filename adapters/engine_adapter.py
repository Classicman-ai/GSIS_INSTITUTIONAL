class EngineAdapter:


    def __init__(self, engine):

        self.engine = engine


    def execute(self, context):

        symbol = context.symbol

        result = self.engine.run(symbol)

        return result
