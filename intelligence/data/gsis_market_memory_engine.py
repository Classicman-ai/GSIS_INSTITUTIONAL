import os
import sqlite3
from datetime import datetime, timezone


print("==============================")
print("GSIS MARKET MEMORY ENGINE v1.0 ONLINE")
print("HISTORICAL MARKET INTELLIGENCE ACTIVE")
print("==============================")


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database",
    "gsis_market_database.sqlite"
)



class GSISMarketMemoryEngine:


    def __init__(self):

        self.connection = sqlite3.connect(
            DATABASE_PATH
        )



    def load_market_history(self):

        cursor = self.connection.cursor()


        cursor.execute(
            """
            SELECT
            symbol,
            timeframe,
            timestamp,
            open,
            high,
            low,
            close,
            volume

            FROM market_candles

            ORDER BY timestamp ASC
            """
        )


        rows = cursor.fetchall()


        candles = []


        for row in rows:

            candles.append(

                {

                    "symbol": row[0],

                    "timeframe": row[1],

                    "timestamp": row[2],

                    "open": row[3],

                    "high": row[4],

                    "low": row[5],

                    "close": row[6],

                    "volume": row[7]

                }

            )


        return candles




    def calculate_statistics(
        self,
        candles
    ):


        if not candles:

            return {

                "samples": 0,

                "status":
                "NO DATA"

            }



        bullish = 0

        bearish = 0

        ranges = []



        for candle in candles:


            if candle["close"] > candle["open"]:

                bullish += 1


            elif candle["close"] < candle["open"]:

                bearish += 1



            ranges.append(

                candle["high"]
                -
                candle["low"]

            )



        average_range = (
            sum(ranges)
            /
            len(ranges)
        )



        return {


            "samples":
            len(candles),


            "bullish_candles":
            bullish,


            "bearish_candles":
            bearish,


            "bullish_ratio":
            round(
                bullish / len(candles) * 100,
                2
            ),


            "bearish_ratio":
            round(
                bearish / len(candles) * 100,
                2
            ),


            "average_range":
            round(
                average_range,
                4
            )


        }





    def generate_memory_profile(self):


        candles = self.load_market_history()


        statistics = self.calculate_statistics(
            candles
        )



        profile = {


            "status":
            "MARKET MEMORY GENERATED",


            "database":
            DATABASE_PATH,


            "statistics":
            statistics,


            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()


        }


        return profile





if __name__ == "__main__":


    engine = GSISMarketMemoryEngine()


    print("==============================")
    print("GSIS MARKET MEMORY RESULT")
    print("==============================")


    result = (
        engine.generate_memory_profile()
    )


    print(result)
