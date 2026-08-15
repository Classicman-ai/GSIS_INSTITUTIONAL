from datetime import datetime, timezone


class MultiTimeframeCandleEngine:

    def __init__(self):

        print("==============================")
        print("GSIS MULTI-TIMEFRAME CANDLE ENGINE v2.0 ONLINE")
        print("==============================")
        print("MULTI-TIMEFRAME AGGREGATION ACTIVE")
        print("==============================")

        self.timeframes = {
            "M1": None,
            "M5": None,
            "M15": None,
            "M30": None,
            "H1": None,
            "H4": None,
            "D1": None,
            "W1": None,
            "MN1": None
        }

    def update(self, candle):

        for tf in self.timeframes:

            self.timeframes[tf] = {
                "symbol": candle["symbol"],
                "timeframe": tf,
                "open": candle["open"],
                "high": candle["high"],
                "low": candle["low"],
                "close": candle["close"],
                "timestamp": candle.get(
                    "timestamp",
                    datetime.now(timezone.utc).isoformat()
                )
            }

        print("==============================")
        print("MULTI-TIMEFRAME UPDATED")
        print("==============================")

        return self.timeframes

    def get(self, timeframe):

        return self.timeframes.get(timeframe)

    def get_all(self):

        return self.timeframes
