"""
=========================================================
GSIS INSTITUTIONAL
HISTORICAL DATA IMPORT ENGINE
Version: 1.0

Historical Market Data Loader
=========================================================
"""


import csv
import os



class HistoricalImportEngine:


    def __init__(self):

        self.name = "Historical Import Engine"

        self.status = "CREATED"



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("HISTORICAL IMPORT ENGINE ONLINE")
        print("==============================")



    def validate_row(
            self,
            row):


        required = [

            "timestamp",

            "open",

            "high",

            "low",

            "close"

        ]


        for field in required:


            if field not in row:

                return False



        return True



    def load_csv(
            self,
            file_path):


        if not os.path.exists(file_path):

            print(
                "FILE NOT FOUND:",
                file_path
            )

            return []



        data = []



        with open(
            file_path,
            "r"
        ) as file:


            reader = csv.DictReader(
                file
            )


            for row in reader:


                if self.validate_row(row):


                    data.append({

                        "timestamp":
                        row["timestamp"],


                        "open":
                        float(row["open"]),


                        "high":
                        float(row["high"]),


                        "low":
                        float(row["low"]),


                        "close":
                        float(row["close"])

                    })



        print(

            "HISTORICAL DATA LOADED:",

            len(data)

        )


        return data



    def prepare_memory_records(
            self,
            candles):


        records = []


        for candle in candles:


            records.append({

                "timestamp":
                candle["timestamp"],


                "symbol":
                candle.get(
                    "symbol",
                    "UNKNOWN"
                ),


                "timeframe":
                candle.get(
                    "timeframe",
                    "UNKNOWN"
                ),


                "open":
                candle["open"],


                "high":
                candle["high"],


                "low":
                candle["low"],


                "close":
                candle["close"]

            })



        return records
