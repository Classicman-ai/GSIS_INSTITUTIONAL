import sqlite3
import os
import datetime


class GSISSQLiteDatabaseEngine:

    def __init__(self):

        print("==============================")
        print("GSIS SQLITE DATABASE ENGINE v1.0 ONLINE")
        print("INSTITUTIONAL DATA STORAGE ACTIVE")
        print("==============================")

        self.path = "database/gsis_intelligence.db"

        os.makedirs(
            "database",
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            self.path
        )

        self.create_tables()


    def create_tables(self):

        cursor = self.connection.cursor()


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_reactions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            event TEXT,

            forecast TEXT,

            actual TEXT,

            surprise REAL,

            market_before TEXT,

            market_after TEXT,

            trade_result TEXT,

            confidence INTEGER,

            rr REAL,

            timestamp TEXT

        )
        """)


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS economic_events (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            event TEXT,

            currency TEXT,

            impact TEXT,

            event_time TEXT

        )
        """)


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_memory (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            pattern TEXT,

            context TEXT,

            outcome TEXT,

            confidence REAL,

            timestamp TEXT

        )
        """)


        self.connection.commit()



    def insert_reaction(
        self,
        data
    ):

        cursor = self.connection.cursor()


        cursor.execute("""

        INSERT INTO market_reactions

        (
        event,
        forecast,
        actual,
        surprise,
        market_before,
        market_after,
        trade_result,
        confidence,
        rr,
        timestamp
        )

        VALUES (?,?,?,?,?,?,?,?,?,?)

        """,

        (

        data["event"],
        data["forecast"],
        data["actual"],
        data["surprise"],
        str(data["market_before"]),
        str(data["market_after"]),
        data["trade"]["result"],
        data["trade"]["confidence"],
        data["trade"]["rr"],
        datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()

        ))


        self.connection.commit()



    def count_records(self):

        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM market_reactions"
        )

        return cursor.fetchone()[0]



if __name__ == "__main__":


    engine = GSISSQLiteDatabaseEngine()


    print("==============================")
    print("DATABASE STATUS")
    print("==============================")

    print({

        "status":"READY",

        "market_reactions":
            engine.count_records()

    })
