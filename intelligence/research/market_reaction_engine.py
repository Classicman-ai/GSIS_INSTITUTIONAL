import json
import os
import uuid
import datetime


class MarketReactionEngine:

    def __init__(self):

        print("==============================")
        print("GSIS MARKET REACTION ENGINE v1.0 ONLINE")
        print("MARKET REACTION MEMORY ACTIVE")
        print("==============================")

        self.database = "database/market_reactions"

        os.makedirs(self.database, exist_ok=True)

    def record_event(

        self,

        event,

        forecast,

        actual,

        market_before,

        market_after,

        trade

    ):

        surprise = self.calculate_surprise(

            forecast,
            actual

        )

        record = {

            "event_id": str(uuid.uuid4()),

            "event": event,

            "forecast": forecast,

            "actual": actual,

            "surprise": surprise,

            "market_before": market_before,

            "market_after": market_after,

            "trade": trade,

            "timestamp":

                datetime.datetime.now(

                    datetime.timezone.utc

                ).isoformat()

        }

        filename = os.path.join(

            self.database,

            record["event_id"] + ".json"

        )

        with open(filename, "w") as f:

            json.dump(

                record,

                f,

                indent=4

            )

        return record

    def calculate_surprise(

        self,

        forecast,

        actual

    ):

        try:

            f = float(

                str(forecast)

                .replace("%", "")
                .replace("K", "")

            )

            a = float(

                str(actual)

                .replace("%", "")
                .replace("K", "")

            )

            return round(

                a - f,

                2

            )

        except:

            return "UNKNOWN"

    def total_records(self):

        return len(

            os.listdir(

                self.database

            )

        )


if __name__ == "__main__":

    engine = MarketReactionEngine()

    market_before = {

        "trend": "BULLISH",

        "bos": False,

        "choch": False,

        "liquidity": "BUY_SIDE"

    }

    market_after = {

        "trend": "BEARISH",

        "bos": True,

        "choch": True,

        "liquidity_sweep": True,

        "order_block": True,

        "fvg": True,

        "candlestick": "BEARISH_ENGULFING",

        "chart_pattern": "HEAD_AND_SHOULDERS"

    }

    trade = {

        "decision": "SELL",

        "confidence": 94,

        "result": "WIN",

        "rr": 3.2

    }

    result = engine.record_event(

        event="NFP",

        forecast="185",

        actual="225",

        market_before=market_before,

        market_after=market_after,

        trade=trade

    )

    print("==============================")
    print("GSIS MARKET REACTION SAVED")
    print("==============================")
    print(result)

    print("==============================")
    print("TOTAL REACTION RECORDS")
    print("==============================")
    print(engine.total_records())
