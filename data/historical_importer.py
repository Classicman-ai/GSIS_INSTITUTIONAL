"""
=========================================================
GSIS INSTITUTIONAL
Historical Data Importer
Version: 1.0
=========================================================
"""

import sqlite3
import os
from datetime import datetime


class HistoricalImporter:


    def __init__(
        self,
        db_path="database/historical.db"
    ):

        self.db_path = db_path



    def connect(self):

        return sqlite3.connect(
            self.db_path
        )



    def validate_candle(self, candle):

        required = [

            "symbol",
            "timeframe",
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume"

        ]


        for field in required:

            if field not in candle:

                return False


        return True



    def import_candle(
            self,
            candle):


        if not self.validate_candle(candle):

            print(
                "[INVALID CANDLE]"
            )

            return False



        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute("""
        SELECT id

        FROM candles

        WHERE symbol=?
        AND timeframe=?
        AND timestamp=?

        """,

        (

            candle["symbol"],

            candle["timeframe"],

            candle["timestamp"]

        ))


        exists = cursor.fetchone()


        if exists:

            conn.close()

            return False



        cursor.execute("""
        INSERT INTO candles

        (
        symbol,
        timeframe,
        timestamp,
        open,
        high,
        low,
        close,
        volume
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        """,

        (

        candle["symbol"],
        candle["timeframe"],
        candle["timestamp"],
        candle["open"],
        candle["high"],
        candle["low"],
        candle["close"],
        candle["volume"]

        ))



        conn.commit()

        conn.close()


        return True



    def import_batch(
            self,
            candles):


        imported = 0


        for candle in candles:

            if self.import_candle(candle):

                imported += 1



        print(
            "IMPORTED:",
            imported
        )


        return imported
