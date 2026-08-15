"""
=========================================================

GSIS INSTITUTIONAL

DATABASE ENGINE v2.4

Central Memory Core
Schema Migration Edition

=========================================================
"""


import sqlite3
import os
from datetime import datetime, UTC



class DatabaseEngine:


    def __init__(self):

        self.db_path = "database/gsis.db"


        os.makedirs(
            "database",
            exist_ok=True
        )


        self.connection = sqlite3.connect(
            self.db_path
        )


        self.initialize()


        print("==============================")
        print("GSIS DATABASE ENGINE v2.4 ONLINE")
        print("==============================")
        print("GSIS MEMORY CORE ACTIVE")




    def initialize(self):

        self.create_tables()

        self.migrate_learning_memory()

        print(
            "DATABASE INITIALIZATION COMPLETE"
        )




    def create_tables(self):

        cursor = self.connection.cursor()


        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS learning_memory
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT
            )
            """
        )


        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS system_logs
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event TEXT,
                timestamp TEXT
            )
            """
        )


        self.connection.commit()





    def migrate_learning_memory(self):


        cursor = self.connection.cursor()


        cursor.execute(
            "PRAGMA table_info(learning_memory)"
        )


        columns = [

            row[1]

            for row in cursor.fetchall()

        ]



        required = {


            "symbol": "TEXT",

            "pattern_type": "TEXT",

            "market_state": "TEXT",

            "momentum": "TEXT",

            "confidence": "REAL",

            "timestamp": "TEXT"

        }



        for column, datatype in required.items():


            if column not in columns:


                cursor.execute(

                    f"""

                    ALTER TABLE learning_memory

                    ADD COLUMN {column} {datatype}

                    """

                )


        self.connection.commit()



        print(
            "LEARNING MEMORY SCHEMA VERIFIED"
        )





    def save_learning_memory(self, pattern):


        cursor = self.connection.cursor()


        cursor.execute(

            """
            INSERT INTO learning_memory
            (
            symbol,
            pattern_type,
            market_state,
            momentum,
            confidence,
            timestamp
            )

            VALUES (?,?,?,?,?,?)

            """,

            (

            pattern.get("symbol"),

            pattern.get("pattern_type"),

            pattern.get("market_state"),

            pattern.get("momentum"),

            pattern.get("confidence"),

            pattern.get("timestamp")

            )

        )


        self.connection.commit()


        print(
            "LEARNING MEMORY UPDATED"
        )





    def get_learning_patterns(self, symbol=None):


        cursor = self.connection.cursor()


        if symbol:


            cursor.execute(

                """
                SELECT *
                FROM learning_memory
                WHERE symbol=?
                ORDER BY id DESC
                """,

                (symbol,)

            )


        else:


            cursor.execute(

                """
                SELECT *
                FROM learning_memory
                ORDER BY id DESC
                """

            )


        return cursor.fetchall()





    def log_event(self,event):


        cursor = self.connection.cursor()


        cursor.execute(

            """
            INSERT INTO system_logs
            (
            event,
            timestamp
            )

            VALUES (?,?)

            """,

            (

            event,

            datetime.now(
                UTC
            ).isoformat()

            )

        )


        self.connection.commit()
