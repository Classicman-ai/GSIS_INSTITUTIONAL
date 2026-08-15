"""
=========================================================
GSIS INSTITUTIONAL
Feature Database Engine
Version: 1.0
=========================================================
"""

import sqlite3
import os
from datetime import datetime


class FeatureDatabase:


    def __init__(
            self,
            db_path="database/features.db"):

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
        CREATE TABLE IF NOT EXISTS features (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            symbol TEXT,

            timeframe TEXT,

            timestamp TEXT,

            close REAL,

            return_pct REAL,

            direction TEXT,

            candle_range REAL,

            volatility REAL,

            created_at TEXT

        )
        """)


        conn.commit()

        conn.close()


        print(
            "[FEATURE DATABASE READY]"
        )



    def save_feature(
            self,
            symbol,
            timeframe,
            feature):


        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute("""
        INSERT INTO features
        (

        symbol,
        timeframe,
        timestamp,
        close,
        return_pct,
        direction,
        candle_range,
        volatility,
        created_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

        """,

        (

        symbol,

        timeframe,

        feature["timestamp"],

        feature["close"],

        feature["return_pct"],

        feature["direction"],

        feature["range"],

        feature["volatility"],

        str(datetime.utcnow())

        ))


        conn.commit()

        conn.close()



    def get_features(
            self,
            symbol,
            timeframe,
            limit=100):


        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute("""
        SELECT *

        FROM features

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
