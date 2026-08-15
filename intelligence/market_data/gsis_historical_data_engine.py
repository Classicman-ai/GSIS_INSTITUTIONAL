import os
import sys
import sqlite3
import datetime


# ============================================================
# GSIS PATH CONTROL
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(
        0,
        BASE_DIR
    )


from intelligence.market_data.gsis_provider_manager import (
    GSISProviderManager
)


print("==============================")
print("GSIS HISTORICAL DATA ENGINE v1.0 ONLINE")
print("LONG TERM MARKET DATA ACQUISITION ACTIVE")
print("==============================")


DATABASE = os.path.join(
    BASE_DIR,
    "database",
    "gsis_market_database.sqlite"
)



class GSISHistoricalDataEngine:


    def __init__(self):

        self.manager = GSISProviderManager()

        self.connection = sqlite3.connect(
            DATABASE
        )

        self.create_database()



    # ========================================================
    # DATABASE INITIALIZATION
    # ========================================================

    def create_database(self):

        cursor = self.connection.cursor()


        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS gsis_historical_market_data
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            date TEXT UNIQUE,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            provider TEXT,
            imported_at TEXT
            )
            """
        )


        self.connection.commit()



    # ========================================================
    # DOWNLOAD HISTORY
    # ========================================================

    def acquire_history(
        self,
        symbol="XAUUSD",
        limit=5000
    ):


        print("==============================")
        print("HISTORICAL ACQUISITION START")
        print("==============================")


        history = self.manager.get_history(
            symbol,
            limit
        )


        imported = 0
        skipped = 0


        cursor = self.connection.cursor()


        for provider, data in history.items():


            candles = data.get(
                "candles",
                []
            )


            for candle in candles:


                try:


                    cursor.execute(

                        """
                        INSERT INTO
                        gsis_historical_market_data

                        (
                        symbol,
                        date,
                        open,
                        high,
                        low,
                        close,
                        provider,
                        imported_at
                        )

                        VALUES (?,?,?,?,?,?,?,?)

                        """,

                        (

                        symbol,

                        candle["date"],

                        candle["open"],

                        candle["high"],

                        candle["low"],

                        candle["close"],

                        provider,

                        self.timestamp()

                        )

                    )


                    imported += 1


                except sqlite3.IntegrityError:


                    skipped += 1



        self.connection.commit()



        return {


            "status":
            "HISTORICAL IMPORT COMPLETE",


            "symbol":
            symbol,


            "imported":
            imported,


            "skipped":
            skipped,


            "database":
            DATABASE,


            "timestamp":
            self.timestamp()

        }



    # ========================================================
    # DATABASE STATUS
    # ========================================================

    def database_status(self):


        cursor = self.connection.cursor()


        cursor.execute(

            """
            SELECT COUNT(*)

            FROM gsis_historical_market_data

            """

        )


        total = cursor.fetchone()[0]


        return {

            "historical_records":
            total,

            "database":
            DATABASE,

            "timestamp":
            self.timestamp()

        }



    def timestamp(self):

        return datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()




if __name__ == "__main__":


    engine = GSISHistoricalDataEngine()


    print("==============================")
    print("GSIS HISTORICAL DATA TEST")
    print("==============================")


    print(

        engine.acquire_history(
            "XAUUSD",
            5000
        )

    )


    print(

        engine.database_status()

    )
