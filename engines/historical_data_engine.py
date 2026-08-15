"""
=========================================================
GSIS INSTITUTIONAL
Historical Data Engine
Version: 1.0
=========================================================
"""

import sqlite3
import os
from datetime import datetime

from core.base_engine import BaseEngine


class HistoricalDataEngine(BaseEngine):


    def __init__(self):

        super().__init__(
            "Historical Data Engine"
        )

        self.db_path = (
            "database/historical.db"
        )



    def initialize(self):

        super().initialize()

        os.makedirs(
            "database",
            exist_ok=True
        )


        conn = sqlite3.connect(
            self.db_path
        )

        cursor = conn.cursor()


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS candles (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            symbol TEXT,

            timeframe TEXT,

            timestamp TEXT,

            open REAL,

            high REAL,

            low REAL,

            close REAL,

            volume REAL

        )
        """)


        conn.commit()

        conn.close()


        print(
            "[HISTORICAL DATABASE READY]"
        )



    def store_candle(
            self,
            candle):


        conn = sqlite3.connect(
            self.db_path
        )

        cursor = conn.cursor()


        cursor.execute("""
        INSERT INTO candles (

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



    def get_history(
            self,
            symbol,
            timeframe,
            limit=100):


        conn = sqlite3.connect(
            self.db_path
        )


        cursor = conn.cursor()


        cursor.execute("""
        SELECT *

        FROM candles

        WHERE symbol=?
        AND timeframe=?

        ORDER BY timestamp DESC

        LIMIT ?

        """,

        (
            symbol,
            timeframe,
            limit
        ))


        data = cursor.fetchall()


        conn.close()


        return data



    def run(self):

        self.status = "RUNNING"

        print(
            "[Historical Engine] Ready"
        )



    def shutdown(self):

        super().shutdown()
