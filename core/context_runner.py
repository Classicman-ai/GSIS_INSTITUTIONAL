class GSISContext:

    def __init__(self, symbol):

        self.symbol = symbol

        self.market = None
        self.liquidity = None
        self.volume = None
        self.orderflow = None
        self.regime = None
        self.adaptive = None
        self.validation = None
        self.fusion = None
        self.signal = None
        self.risk = None
        self.quality = None
        self.execution = None
        self.journal = None
        self.performance = None
        self.memory = None
        self.intelligence = None



class GSISContextRunner:


    def __init__(self, symbol):

        self.context = GSISContext(symbol)



    def push(self, name, result):

        setattr(
            self.context,
            name,
            result
        )

        print(
            "CONTEXT UPDATE:",
            name,
            result.get("engine","")
        )



    def update(self, name, result):

        self.push(
            name,
            result
        )



    def snapshot(self):

        return {

            "symbol":
                self.context.symbol,

            "market":
                self.context.market,

            "liquidity":
                self.context.liquidity,

            "volume":
                self.context.volume,

            "orderflow":
                self.context.orderflow,

            "regime":
                self.context.regime,

            "adaptive":
                self.context.adaptive,

            "validation":
                self.context.validation,

            "fusion":
                self.context.fusion,

            "signal":
                self.context.signal,

            "risk":
                self.context.risk
        }
