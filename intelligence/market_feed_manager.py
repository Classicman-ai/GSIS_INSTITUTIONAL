class MarketFeedManager:


    def __init__(
        self,
        realtime_engine,
        candle_engine
    ):

        self.realtime_engine = realtime_engine
        self.candle_engine = candle_engine


        print("==============================")
        print("GSIS MARKET FEED MANAGER v1.0 ONLINE")
        print("==============================")



    def update(
        self,
        symbol,
        price
    ):

        tick = self.realtime_engine.receive_tick(
            symbol,
            price
        )


        candle = self.candle_engine.build_candle(
            tick
        )


        return candle
