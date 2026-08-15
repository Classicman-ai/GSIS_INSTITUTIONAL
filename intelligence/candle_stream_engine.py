import datetime


class CandleStreamEngine:


    def __init__(self):

        print("==============================")
        print("GSIS CANDLE STREAM ENGINE v1.0 ONLINE")
        print("==============================")
        print("REALTIME CANDLE GENERATION ACTIVE")


    def build_candle(
        self,
        tick
    ):

        candle = {

            "symbol":
            tick["symbol"],

            "timeframe":
            "M1",

            "open":
            tick["price"],

            "high":
            tick["price"],

            "low":
            tick["price"],

            "close":
            tick["price"],

            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }


        print("==============================")
        print("REALTIME CANDLE CREATED")
        print("==============================")

        print(candle)

        return candle
