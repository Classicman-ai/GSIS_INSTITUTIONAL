import os
import csv
import sqlite3
from datetime import datetime, timezone


print("==============================")
print("GSIS HISTORICAL DATA IMPORTER v1.0 ONLINE")
print("MARKET HISTORY ACQUISITION ACTIVE")
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


IMPORT_FOLDER = os.path.join(
    BASE_DIR,
    "database",
    "historical_import"
)


os.makedirs(
    IMPORT_FOLDER,
    exist_ok=True
)



class GSISHistoricalDataImporter:


    def __init__(self):

        self.connection = sqlite3.connect(
            DATABASE_PATH
        )

        self.create_table()



    def create_table(self):

        cursor = self.connection.cursor()


        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS market_candles (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                symbol TEXT,

                timeframe TEXT,

                timestamp TEXT UNIQUE,

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



    def import_csv(
        self,
        file_path,
        symbol="XAUUSD",
        timeframe="D1"
    ):

        imported = 0
        skipped = 0


        cursor = self.connection.cursor()


        with open(
            file_path,
            "r"
        ) as file:


            reader = csv.DictReader(
                file
            )


            for row in reader:


                try:


                    cursor.execute(

                        """
                        INSERT OR IGNORE INTO market_candles

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

                        symbol,

                        timeframe,

                        row["timestamp"],

                        float(row["open"]),

                        float(row["high"]),

                        float(row["low"]),

                        float(row["close"]),

                        float(
                            row.get(
                                "volume",
                                0
                            )
                        ),

                        "HISTORICAL_IMPORT"

                        )

                    )


                    if cursor.rowcount:

                        imported += 1

                    else:

                        skipped += 1



                except Exception:

                    skipped += 1



        self.connection.commit()


        return {

            "status":
            "IMPORT COMPLETE",

            "imported":
            imported,

            "skipped":
            skipped,

            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()

        }




    def database_summary(self):

        cursor = self.connection.cursor()


        cursor.execute(
            """
            SELECT COUNT(*)
            FROM market_candles
            """
        )


        total = cursor.fetchone()[0]


        return {

            "total_market_records":
            total,

            "database":
            DATABASE_PATH

        }




if __name__ == "__main__":


    engine = GSISHistoricalDataImporter()


    print("==============================")
    print("GSIS HISTORICAL DATABASE STATUS")
    print("==============================")


    print(
        engine.database_summary()
    )
