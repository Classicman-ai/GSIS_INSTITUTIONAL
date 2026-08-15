"""
=========================================================
GSIS INSTITUTIONAL
HISTORY ENGINE
Version: 2.0
Managed Module Architecture
=========================================================
"""

import sqlite3
import os
from datetime import datetime


class HistoryEngine:


    def __init__(self):

        self.name = "History Engine"

        self.db_path = (
            "database/market_history.db"
        )

        self.status = "CREATED"



    def initialize(self):

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

            timeframe TEXT,

            timestamp INTEGER,

            open REAL,

            high REAL,

            low REAL,

            close REAL,

            created_at TEXT

        )
        """)


        conn.commit()

        conn.close()


        self.status = "ONLINE"


        print("==============================")
        print("GSIS HISTORY ENGINE ONLINE")
        print("==============================")



    def save_candle(
            self,
            candle):


        if candle is None:

            return



        conn = sqlite3.connect(
            self.db_path
        )

        cursor = conn.cursor()



        cursor.execute("""
        INSERT INTO candles

        (

        timeframe,

        timestamp,

        open,

        high,

        low,

        close,

        created_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

        """,

        (

        candle["timeframe"],

        candle["timestamp"],

        candle["open"],

        candle["high"],

        candle["low"],

        candle["close"],

        str(datetime.utcnow())

        ))



        conn.commit()

        conn.close()



    def update(
            self,
            candles):


        if not candles:

            return



        for timeframe, candle in candles.items():

            self.save_candle(
                candle
            )


            print(

                "HISTORY SAVED:",

                timeframe

            )



    def shutdown(self):

        self.status = "OFFLINE"

        print(
            "HISTORY ENGINE STOPPED"
        )

