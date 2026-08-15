"""
=========================================================
GSIS INSTITUTIONAL

DATABASE INTELLIGENCE ENGINE

Version 1.0

Institutional Knowledge Storage Layer

=========================================================
"""


import sqlite3
from datetime import datetime
import json



class DatabaseIntelligenceEngine:


    def __init__(self):

        self.name = "Database Intelligence Engine"

        self.status = "CREATED"

        self.database = "database/gsis_intelligence.db"

        self.connection = None





    def initialize(self):


        self.connection = sqlite3.connect(
            self.database
        )


        self.create_tables()


        self.status = "ONLINE"


        print("==============================")
        print("DATABASE INTELLIGENCE ENGINE ONLINE")
        print("==============================")





    def create_tables(self):


        cursor = self.connection.cursor()



        cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS market_memory (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            symbol TEXT,

            timeframe TEXT,

            data TEXT,

            timestamp TEXT

        )
        """
        )



        cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS signals (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            signal TEXT,

            confidence REAL,

            outcome TEXT,

            timestamp TEXT

        )
        """
        )



        cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS patterns (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            pattern TEXT,

            result TEXT,

            timestamp TEXT

        )
        """
        )



        self.connection.commit()





    def store_market_data(
            self,
            symbol,
            timeframe,
            data):


        cursor = self.connection.cursor()


        cursor.execute(
        """

        INSERT INTO market_memory

        (
        symbol,
        timeframe,
        data,
        timestamp
        )

        VALUES (?,?,?,?)

        """,

        (

        symbol,

        timeframe,

        json.dumps(data),

        str(datetime.utcnow())

        )
        )


        self.connection.commit()





    def store_signal(
            self,
            signal):


        cursor = self.connection.cursor()


        cursor.execute(
        """

        INSERT INTO signals

        (
        signal,
        confidence,
        outcome,
        timestamp
        )

        VALUES (?,?,?,?)

        """,

        (

        signal.get(
            "direction"
        ),

        signal.get(
            "confidence"
        ),

        signal.get(
            "status"
        ),

        str(datetime.utcnow())

        )
        )


        self.connection.commit()





    def store_pattern(
            self,
            pattern,
            result):


        cursor = self.connection.cursor()


        cursor.execute(
        """

        INSERT INTO patterns

        (
        pattern,
        result,
        timestamp
        )

        VALUES (?,?,?)

        """,

        (

        pattern,

        result,

        str(datetime.utcnow())

        )
        )


        self.connection.commit()





    def statistics(self):


        cursor = self.connection.cursor()


        result = {}


        for table in [

            "market_memory",

            "signals",

            "patterns"

        ]:


            cursor.execute(
                f"SELECT COUNT(*) FROM {table}"
            )


            result[table] = cursor.fetchone()[0]



        return result
