"""
=========================================================
GSIS INSTITUTIONAL
Market Regime Database
Version: 1.0
=========================================================
"""

import sqlite3
import os
from datetime import datetime


class RegimeDatabase:


    def __init__(
            self,
            db_path="database/regimes.db"):

        self.db_path = db_path


        os.makedirs(
            "database",
            exist_ok=True
        )



    def connect(self):

        return sqlite3.connect(
            self.db_path
        )



    def initialize(self):

        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS regimes (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            symbol TEXT,

            timeframe TEXT,

            timestamp TEXT,

            regime TEXT,

            volatility REAL,

            return_pct REAL,

            confidence REAL,

            created_at TEXT

        )
        """)


        conn.commit()

        conn.close()


        print(
            "[REGIME DATABASE READY]"
        )



    def save_regime(
            self,
            symbol,
            timeframe,
            regime_data):


        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute("""
        INSERT INTO regimes

        (

        symbol,
        timeframe,
        timestamp,
        regime,
        volatility,
        return_pct,
        confidence,
        created_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        """,

        (

        symbol,

        timeframe,

        str(datetime.utcnow()),

        regime_data["regime"],

        regime_data.get(
            "volatility",
            0
        ),

        regime_data.get(
            "return_pct",
            0
        ),

        regime_data.get(
            "confidence",
            0
        ),

        str(datetime.utcnow())

        ))


        conn.commit()

        conn.close()



    def get_recent(
            self,
            symbol,
            timeframe,
            limit=100):


        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute("""
        SELECT *

        FROM regimes

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
