import sys
import os
import sqlite3
from datetime import datetime, timezone


# ==========================================
# GSIS PROJECT PATH
# ==========================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(
    0,
    PROJECT_ROOT
)


print("==============================")
print("GSIS PATTERN AUTO GENERATOR ENGINE v1.1 ONLINE")
print("==============================")
print("AUTOMATIC PATTERN CREATION ACTIVE")
print("==============================")


DB_PATH = "database/qmos.db"



class PatternAutoGenerator:


    def __init__(self):

        self.conn = sqlite3.connect(
            DB_PATH
        )

        self.create_table()



    # ======================================
    # DATABASE INITIALIZATION + UPGRADES
    # ======================================

    def create_table(self):

        cursor = self.conn.cursor()


        cursor.execute("""

        CREATE TABLE IF NOT EXISTS pattern_library (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            pattern TEXT UNIQUE,

            symbol TEXT,

            direction TEXT,

            occurrences INTEGER DEFAULT 1,

            wins INTEGER DEFAULT 0,

            losses INTEGER DEFAULT 0,

            confidence REAL DEFAULT 100

        )

        """)


        # Upgrade existing database

        columns = [

            "created_at TEXT",

            "last_seen TEXT"

        ]


        for column in columns:

            try:

                cursor.execute(

                    f"ALTER TABLE pattern_library ADD COLUMN {column}"

                )

            except sqlite3.OperationalError:

                pass



        self.conn.commit()



    # ======================================
    # BUILD PATTERN NAME
    # ======================================

    def build_pattern_name(
        self,
        symbol,
        direction,
        reasons
    ):


        clean_reasons = []


        for reason in reasons:

            clean = (

                reason
                .upper()
                .replace(" ", "_")
                .replace("-", "_")

            )


            clean_reasons.append(
                clean
            )


        pattern = (

            symbol.upper()
            + "_"
            + direction.upper()
            + "_"
            + "_".join(clean_reasons)

        )


        return pattern



    # ======================================
    # CREATE OR UPDATE PATTERN
    # ======================================

    def generate_pattern(
        self,
        symbol,
        direction,
        reasons,
        confidence=100
    ):


        pattern = self.build_pattern_name(

            symbol,

            direction,

            reasons

        )


        cursor = self.conn.cursor()



        cursor.execute(

            """

            SELECT occurrences, confidence

            FROM pattern_library

            WHERE pattern=?

            """,

            (pattern,)

        )


        existing = cursor.fetchone()



        now = datetime.now(
            timezone.utc
        ).isoformat()



        if existing:


            new_occurrences = existing[0] + 1


            cursor.execute(

                """

                UPDATE pattern_library

                SET

                occurrences=?,

                confidence=?,

                last_seen=?

                WHERE pattern=?

                """,

                (

                    new_occurrences,

                    confidence,

                    now,

                    pattern

                )

            )


            status = "PATTERN UPDATED"



        else:


            cursor.execute(

                """

                INSERT INTO pattern_library

                (

                pattern,

                symbol,

                direction,

                occurrences,

                confidence,

                created_at,

                last_seen

                )

                VALUES (?,?,?,?,?,?,?)

                """,

                (

                    pattern,

                    symbol,

                    direction,

                    1,

                    confidence,

                    now,

                    now

                )

            )


            status = "NEW PATTERN CREATED"



        self.conn.commit()



        result = {


            "pattern": pattern,


            "status": status,


            "occurrences":

            self.get_occurrences(pattern),


            "confidence":

            confidence,


            "timestamp":

            now

        }


        print("==============================")
        print("GSIS PATTERN GENERATOR RESULT")
        print("==============================")

        print(result)


        return result



    # ======================================
    # CHECK OCCURRENCE COUNT
    # ======================================

    def get_occurrences(
        self,
        pattern
    ):


        cursor = self.conn.cursor()


        cursor.execute(

            """

            SELECT occurrences

            FROM pattern_library

            WHERE pattern=?

            """,

            (pattern,)

        )


        result = cursor.fetchone()


        if result:

            return result[0]


        return 0





if __name__ == "__main__":


    engine = PatternAutoGenerator()



    engine.generate_pattern(

        symbol="XAUUSD",

        direction="SELL",

        reasons=[

            "LIQUIDITY SWEEP CONFIRMED",

            "BEARISH ORDER BLOCK",

            "BEARISH FVG",

            "BEARISH CHoCH"

        ],

        confidence=100

    )
