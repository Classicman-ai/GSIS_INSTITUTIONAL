import sqlite3
from datetime import datetime, timezone
import os


print("==============================")
print("GSIS PATTERN MATCHING ENGINE v1.4 ONLINE")
print("==============================")
print("SELF INITIALIZING MEMORY PATTERN SCORING ACTIVE")
print("==============================")


DB_PATH = "database/qmos.db"


class PatternMatchingEngine:

    def __init__(self):

        self.conn = sqlite3.connect(DB_PATH)
        self.create_tables()


    def create_tables(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pattern_library(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            pattern TEXT UNIQUE,

            symbol TEXT,

            direction TEXT,

            occurrences INTEGER DEFAULT 0,

            wins INTEGER DEFAULT 0,

            losses INTEGER DEFAULT 0,

            confidence REAL DEFAULT 0,

            timestamp TEXT

        )
        """)

        self.conn.commit()


    def build_pattern_name(self, signal):

        symbol = signal.get("symbol","")
        direction = signal.get("direction","")

        reasons = signal.get("reasons",[])

        clean = "_".join(
            r.replace(" ","_")
            for r in reasons
        )

        return f"{symbol}_{direction}_{clean}"


    def match_pattern(
        self,
        symbol,
        direction,
        reasons,
        confidence
    ):

        pattern = self.build_pattern_name({

            "symbol":symbol,
            "direction":direction,
            "reasons":reasons

        })


        cursor = self.conn.cursor()


        cursor.execute(
            """
            SELECT pattern, confidence
            FROM pattern_library
            """
        )


        records = cursor.fetchall()


        best_pattern = None
        best_score = 0
        stored_confidence = 0


        for row in records:

            stored_pattern=row[0]

            stored_conf=row[1]


            score=0


            current_words=set(
                pattern.split("_")
            )

            stored_words=set(
                stored_pattern.split("_")
            )


            common=current_words.intersection(
                stored_words
            )


            if len(current_words)>0:

                score=int(
                    len(common)
                    /
                    len(current_words)
                    *
                    100
                )


            if score > best_score:

                best_score=score
                best_pattern=stored_pattern
                stored_confidence=stored_conf



        result={

            "status":"MATCHING COMPLETE",

            "pattern":best_pattern,

            "match_score":best_score,

            "stored_confidence":stored_confidence,

            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()

        }


        print("==============================")
        print("GSIS PATTERN MATCH RESULT")
        print("==============================")

        print(result)


        return result



if __name__=="__main__":


    engine=PatternMatchingEngine()


    engine.match_pattern(

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
