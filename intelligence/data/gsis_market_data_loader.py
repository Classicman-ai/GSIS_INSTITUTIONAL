import os
import json
import sqlite3
from datetime import datetime, timezone


print("==============================")
print("GSIS MARKET DATA LOADER v1.0 ONLINE")
print("HISTORICAL MARKET DATA INGESTION ACTIVE")
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


DATA_FOLDER = os.path.join(
    BASE_DIR,
    "database",
    "market_data"
)


os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(
    os.path.dirname(DATABASE_PATH),
    exist_ok=True
)


class GSISMarketDataLoader:


    def __init__(self):

        self.connection = sqlite3.connect(
            DATABASE_PATH
        )

        self.create_database()



    def create_database(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS market_candles (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                symbol TEXT,

                timeframe TEXT,

                timestamp TEXT,

                open REAL,

                high REAL,

                low REAL,

                close REAL,

                volume REAL,

                source TEXT

            )
            """
        )


        self.connection.commit()



    def store_candle(
        self,
        candle
    ):


        cursor = self.connection.cursor()


        cursor.execute(
            """
            INSERT INTO market_candles
            (
                symbol,
                timeframe,
                timestamp,
                open,
                high,
                low,
                close,
                volume,
                source
            )

            VALUES (?,?,?,?,?,?,?,?,?)

            """,

            (

                candle["symbol"],

                candle["timeframe"],

                candle["timestamp"],

                candle["open"],

                candle["high"],

                candle["low"],

                candle["close"],

                candle["volume"],

                candle["source"]

            )
        )


        self.connection.commit()



    def database_status(self):

        cursor = self.connection.cursor()


        cursor.execute(
            """
            SELECT COUNT(*)
            FROM market_candles
            """
        )


        total = cursor.fetchone()[0]


        return {

            "status":
            "MARKET DATABASE READY",

            "candles_stored":
            total,

            "database":
            DATABASE_PATH,

            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()

        }




if __name__ == "__main__":


    engine = GSISMarketDataLoader()


    sample = {

        "symbol":
        "XAUUSD",

        "timeframe":
        "D1",

        "timestamp":
        datetime.now(
            timezone.utc
        ).isoformat(),

        "open":
        2385.0,

        "high":
        2392.0,

        "low":
        2382.0,

        "close":
        2389.5,

        "volume":
        0,

        "source":
        "GSIS_TEST"

    }


    engine.store_candle(
        sample
    )


    print("==============================")
    print("GSIS DATABASE STATUS")
    print("==============================")

    print(
        engine.database_status()
    )
