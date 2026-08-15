import math


class StatisticalEngine:

    def __init__(self):

        print("==============================")
        print("GSIS STATISTICAL ENGINE ONLINE")
        print("==============================")


    def calculate(self, candle):

        open_price = candle.get("open")
        high = candle.get("high")
        low = candle.get("low")
        close = candle.get("close")


        candle_range = high - low


        if open_price != 0:

            return_pct = (
                (close - open_price)
                / open_price
            ) * 100

        else:

            return_pct = 0



        features = {

            "symbol": candle.get("symbol"),

            "timeframe": candle.get("timeframe"),

            "timestamp": candle.get("timestamp"),

            "open": open_price,

            "high": high,

            "low": low,

            "close": close,

            "return_pct": round(
                return_pct,
                5
            ),

            "volatility_range": round(
                candle_range,
                5
            ),

            "ema20": close

        }


        print("==============================")
        print("GSIS GOLD STATISTICAL FEATURES")
        print("==============================")

        print(features)


        return features
