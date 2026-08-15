import os
import sys
from datetime import datetime, timezone


print("==============================")
print("GSIS DATA PIPELINE CONTROLLER v1.0 ONLINE")
print("AUTOMATED MARKET DATA INGESTION ACTIVE")
print("==============================")


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


sys.path.insert(
    0,
    PROJECT_ROOT
)


from intelligence.data.gsis_historical_market_downloader import (
    GSISHistoricalMarketDownloader
)

from intelligence.data.gsis_historical_data_importer import (
    GSISHistoricalDataImporter
)



class GSISDataPipelineController:


    def __init__(self):

        self.downloader = GSISHistoricalMarketDownloader()

        self.importer = GSISHistoricalDataImporter()



    def run_pipeline(self):

        print("==============================")
        print("GSIS DATA PIPELINE START")
        print("==============================")


        # Step 1
        # Acquire market data

        download = (
            self.downloader.create_sample_history()
        )


        print("DOWNLOAD RESULT")
        print(download)



        # Step 2
        # Import into database

        import_file = os.path.join(

            PROJECT_ROOT,

            "database",

            "historical_import",

            "XAUUSD_HISTORICAL_DATA.csv"

        )


        imported = self.importer.import_csv(

            import_file,

            symbol="XAUUSD",

            timeframe="D1"

        )


        print("IMPORT RESULT")
        print(imported)



        # Step 3
        # Database verification


        database = (
            self.importer.database_summary()
        )


        print("==============================")
        print("GSIS DATABASE STATUS")
        print("==============================")

        print(database)



        result = {


            "status":
            "PIPELINE COMPLETE",


            "download":
            download,


            "import":
            imported,


            "database":
            database,


            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()

        }


        print("==============================")
        print("GSIS PIPELINE RESULT")
        print("==============================")

        print(result)


        return result





if __name__ == "__main__":


    engine = GSISDataPipelineController()


    engine.run_pipeline()
