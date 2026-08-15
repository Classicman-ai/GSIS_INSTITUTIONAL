import datetime


class RealtimeDataEngine:

    def __init__(self):
        print("==============================")
        print("GSIS REALTIME DATA ENGINE v1.0 ONLINE")
        print("==============================")
        print("LIVE MARKET DATA LAYER ACTIVE")


    def receive_tick(
        self,
        symbol,
        price
    ):

        tick = {

            "symbol": symbol,
            "price": price,
            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }

        print("==============================")
        print("LIVE TICK RECEIVED")
        print("==============================")

        print(tick)

        return tick
