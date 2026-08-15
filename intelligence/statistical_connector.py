"""
=========================================================

GSIS INSTITUTIONAL

STATISTICAL INTELLIGENCE CONNECTOR v1.0

Candle -> Market Features

=========================================================
"""

import os
import sys
import math
from collections import deque
from datetime import datetime, UTC


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from core.event_bus import event_bus


class StatisticalConnector:


    def __init__(self):

        self.prices = deque(maxlen=200)

        self.symbol = "BTCUSDT"


    def process_candle(self, candle):

        close = candle["close"]

        self.prices.append(close)


        features = {


            "symbol":
            candle["symbol"],


            "timeframe":
            candle["timeframe"],


            "close":
            close,


            "timestamp":
            datetime.now(UTC).isoformat()

        }


        if len(self.prices) > 1:

            previous = self.prices[-2]


            features["return_pct"] = (
                (close - previous)
                /
                previous
            ) * 100


            features["log_return"] = math.log(
                close / previous
            )


        else:

            features["return_pct"] = 0

            features["log_return"] = 0



        if len(self.prices) >= 20:

            features["ema20"] = sum(
                list(self.prices)[-20:]
            ) / 20

        else:

            features["ema20"] = close



        print()

        print("==============================")

        print("GSIS STATISTICAL FEATURES")

        print("==============================")

        print(features)



        event_bus.publish(

            "market_features",

            features

        )



def feature_listener(data):

    print(
        "FEATURE EVENT RECEIVED"
    )

    print(data)



engine = StatisticalConnector()


event_bus.subscribe(

    "completed_candle",

    engine.process_candle

)


event_bus.subscribe(

    "market_features",

    feature_listener

)


print(
    "STATISTICAL CONNECTOR ONLINE"
)
