import os
import csv
import json
from datetime import datetime, timezone


print("==============================")
print("GSIS HISTORICAL MARKET DOWNLOADER v1.0 ONLINE")
print("MARKET DATA ACQUISITION CONTROL ACTIVE")
print("==============================")


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


DATA_FOLDER = os.path.join(
    BASE_DIR,
    "database",
    "historical_import"
)


os.makedirs(
    DATA_FOLDER,
    exist_ok=True
)


DATA_FILE = os.path.join(
    DATA_FOLDER,
    "XAUUSD_HISTORICAL_DATA.csv"
)



class GSISHistoricalMarketDownloader:


    def __init__(self):

        self.file = DATA_FILE



    def create_sample_history(self):

        """
        Creates a structured historical
        data template.

        This format is compatible with
        GSIS Historical Data Importer.
        """


        candles = [

            {
                "timestamp":
                "2026-07-01T00:00:00Z",

                "open":
                2325.0,

                "high":
                2340.0,

                "low":
                2318.0,

                "close":
                2335.0,

                "volume":
                0
            },


            {
                "timestamp":
                "2026-07-02T00:00:00Z",

                "open":
                2335.0,

                "high":
                2355.0,

                "low":
                2330.0,

                "close":
                2350.0,

                "volume":
                0
            }

        ]



        with open(
            self.file,
            "w",
            newline=""
        ) as csv_file:


            writer = csv.DictWriter(

                csv_file,

                fieldnames=[

                    "timestamp",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume"

                ]

            )


            writer.writeheader()


            writer.writerows(
                candles
            )



        return {

            "status":
            "DATA FILE CREATED",

            "file":
            self.file,

            "records":
            len(candles)

        }




    def status(self):

        exists = os.path.exists(
            self.file
        )


        return {

            "data_file":
            self.file,

            "available":
            exists,

            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()

        }




if __name__ == "__main__":


    engine = GSISHistoricalMarketDownloader()


    print("==============================")
    print("GSIS DOWNLOAD STATUS")
    print("==============================")


    result = engine.create_sample_history()

    print(result)


    print(engine.status())
