import sqlite3
import os
from datetime import datetime


DB_PATH = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    ),
    "database",
    "pattern_library.db"
)


class PatternLibraryEngine:


    def __init__(self):

        print("==============================")
        print("GSIS PATTERN LIBRARY ENGINE v1.0 ONLINE")
        print("==============================")
        print("INSTITUTIONAL PATTERN DATABASE ACTIVE")
        print("==============================")


        self.create_database()



    def create_database(self):

        os.makedirs(
            os.path.dirname(DB_PATH),
            exist_ok=True
        )


        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()


        cursor.execute("""

        CREATE TABLE IF NOT EXISTS patterns (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            pattern_name TEXT,

            symbol TEXT,

            direction TEXT,

            occurrences INTEGER,

            wins INTEGER,

            losses INTEGER,

            confidence REAL,

            last_seen TEXT

        )

        """)


        conn.commit()

        conn.close()



    def save_pattern(
        self,
        pattern_name,
        symbol,
        direction,
        confidence
    ):


        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()


        cursor.execute("""

        SELECT id, occurrences

        FROM patterns

        WHERE pattern_name=?

        """,
        (pattern_name,))


        existing = cursor.fetchone()



        if existing:


            cursor.execute("""

            UPDATE patterns

            SET occurrences=?,
            confidence=?,
            last_seen=?

            WHERE id=?

            """,
            (
                existing[1] + 1,
                confidence,
                datetime.utcnow().isoformat(),
                existing[0]
            ))


        else:


            cursor.execute("""

            INSERT INTO patterns

            (
            pattern_name,
            symbol,
            direction,
            occurrences,
            wins,
            losses,
            confidence,
            last_seen
            )

            VALUES (?,?,?,?,?,?,?,?)

            """,
            (
                pattern_name,
                symbol,
                direction,
                1,
                0,
                0,
                confidence,
                datetime.utcnow().isoformat()
            ))



        conn.commit()

        conn.close()



    def get_patterns(self):


        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()


        cursor.execute("""

        SELECT *

        FROM patterns

        ORDER BY confidence DESC

        """)


        data = cursor.fetchall()


        conn.close()


        return data





if __name__ == "__main__":


    engine = PatternLibraryEngine()


    engine.save_pattern(

        "XAUUSD_SELL_LIQUIDITY_SWEEP_FVG_CHOCH",

        "XAUUSD",

        "SELL",

        100

    )


    print("==============================")
    print("GSIS PATTERN LIBRARY RESULT")
    print("==============================")


    print(
        engine.get_patterns()
    )
