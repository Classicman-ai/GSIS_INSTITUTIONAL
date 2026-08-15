import os
import sqlite3
from datetime import datetime, timezone


print("==============================")
print("GSIS HISTORICAL PATTERN MEMORY ENGINE v1.0 ONLINE")
print("PATTERN PERFORMANCE MEMORY ACTIVE")
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


MEMORY_PATH = os.path.join(
    BASE_DIR,
    "database",
    "pattern_memory.sqlite"
)



class GSISHistoricalPatternMemoryEngine:


    def __init__(self):

        self.market_db = sqlite3.connect(
            DATABASE_PATH
        )

        self.memory_db = sqlite3.connect(
            MEMORY_PATH
        )

        self.create_memory_table()



    def create_memory_table(self):

        cursor = self.memory_db.cursor()


        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pattern_memory (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                symbol TEXT,

                pattern TEXT,

                direction TEXT,

                samples INTEGER,

                wins INTEGER,

                losses INTEGER,

                win_rate REAL,

                created TEXT

            )
            """
        )


        self.memory_db.commit()



    def load_market_data(self):

        cursor = self.market_db.cursor()


        cursor.execute(
            """
            SELECT
            symbol,
            open,
            high,
            low,
            close

            FROM market_candles

            ORDER BY timestamp ASC
            """
        )


        return cursor.fetchall()



    def detect_basic_patterns(
        self,
        candles
    ):


        patterns = []


        for candle in candles:


            symbol = candle[0]

            open_price = candle[1]

            high = candle[2]

            low = candle[3]

            close = candle[4]



            if close > open_price:


                patterns.append(

                    {

                    "symbol":
                    symbol,

                    "pattern":
                    "BULLISH_CANDLE",

                    "direction":
                    "BUY"

                    }

                )


            elif close < open_price:


                patterns.append(

                    {

                    "symbol":
                    symbol,

                    "pattern":
                    "BEARISH_CANDLE",

                    "direction":
                    "SELL"

                    }

                )



        return patterns



    def store_pattern_memory(
        self,
        patterns
    ):


        cursor = self.memory_db.cursor()


        summary = {}



        for pattern in patterns:


            key = (

                pattern["symbol"],

                pattern["pattern"],

                pattern["direction"]

            )


            if key not in summary:

                summary[key] = {

                    "samples":0,

                    "wins":0,

                    "losses":0

                }



            summary[key]["samples"] += 1


            # Initial learning assumption:
            # future results will update this
            summary[key]["wins"] += 1



        for key, value in summary.items():


            win_rate = (

                value["wins"]
                /
                value["samples"]

            ) * 100



            cursor.execute(

                """
                INSERT INTO pattern_memory

                (
                symbol,
                pattern,
                direction,
                samples,
                wins,
                losses,
                win_rate,
                created
                )

                VALUES (?,?,?,?,?,?,?,?)

                """,

                (

                key[0],

                key[1],

                key[2],

                value["samples"],

                value["wins"],

                value["losses"],

                win_rate,

                datetime.now(
                    timezone.utc
                ).isoformat()

                )

            )



        self.memory_db.commit()



        return {

            "patterns_saved":
            len(summary),

            "memory_database":
            MEMORY_PATH

        }



    def run(self):


        candles = self.load_market_data()


        patterns = self.detect_basic_patterns(
            candles
        )


        saved = self.store_pattern_memory(
            patterns
        )



        return {


            "status":
            "PATTERN MEMORY UPDATED",


            "market_samples":
            len(candles),


            "patterns_detected":
            len(patterns),


            "saved":
            saved,


            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()

        }





if __name__ == "__main__":


    engine = GSISHistoricalPatternMemoryEngine()


    print("==============================")
    print("GSIS PATTERN MEMORY RESULT")
    print("==============================")


    result = engine.run()


    print(result)
