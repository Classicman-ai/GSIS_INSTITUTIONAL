import sqlite3
from datetime import datetime, timezone


class MemoryEngine:

    def __init__(self):
        self.db = "database/gsis_memory.db"
        self.create_table()


    def create_table(self):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            timestamp TEXT,
            direction TEXT,
            entry REAL,
            stop_loss REAL,
            quality TEXT,
            fusion_score REAL,
            result TEXT
        )
        """)

        conn.commit()
        conn.close()



    def execute(self, context):

        signal = context.signal or {}
        risk = context.risk or {}
        quality = context.quality or {}
        fusion = context.fusion or {}


        direction = signal.get(
            "direction",
            "NO_TRADE"
        )


        entry = risk.get(
            "entry"
        )


        stop_loss = risk.get(
            "stop_loss"
        )


        quality_grade = quality.get(
            "quality_grade",
            "N/A"
        )


        fusion_score = fusion.get(
            "fusion_score",
            0
        )


        result = (
            "TRADE_STORED"
            if direction != "NO_TRADE"
            else "NO_TRADE_STORED"
        )


        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()


        cursor.execute(
            """
            INSERT INTO memory
            (
            symbol,
            timestamp,
            direction,
            entry,
            stop_loss,
            quality,
            fusion_score,
            result
            )
            VALUES (?,?,?,?,?,?,?,?)
            """,
            (
            context.symbol,
            datetime.now(timezone.utc).isoformat(),
            direction,
            entry,
            stop_loss,
            quality_grade,
            fusion_score,
            result
            )
        )


        conn.commit()
        conn.close()


        return {

            "engine":
            "GSIS MEMORY ENGINE",

            "version":
            "1.1",

            "symbol":
            context.symbol,

            "direction":
            direction,

            "stored":
            True,

            "database":
            self.db,

            "status":
            "MEMORY_STORED"

        }



if __name__ == "__main__":

    print(
        "GSIS MEMORY ENGINE v1.1 READY"
    )
