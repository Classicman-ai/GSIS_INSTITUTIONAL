"""
=========================================================

GSIS INSTITUTIONAL

CANDLE DATABASE WRITER ENGINE v1.0

Completed Candle Storage Layer

=========================================================
"""

import os
import sys


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from database.database_engine import DatabaseEngine
from core.event_bus import event_bus



class CandleDatabaseWriter:


    def __init__(self):

        self.database = DatabaseEngine()

        print("==============================")
        print("GSIS CANDLE DATABASE WRITER")
        print("==============================")



    def save_candle(self, candle):


        self.database.save_candle(

            symbol=candle["symbol"],

            timeframe=candle["timeframe"],

            open_price=candle["open"],

            high_price=candle["high"],

            low_price=candle["low"],

            close_price=candle["close"],

            volume=candle["volume"]

        )


        print(
            "CANDLE SAVED TO DATABASE"
        )

        print(candle)




writer = CandleDatabaseWriter()



def candle_receiver(data):

    writer.save_candle(data)



event_bus.subscribe(

    "completed_candle",

    candle_receiver

)



print(
    "CANDLE DATABASE WRITER ONLINE"
)
