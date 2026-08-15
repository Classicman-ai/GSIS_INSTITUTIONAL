import sqlite3
from datetime import datetime, timezone


class FeatureMemoryEngine:

    def __init__(self):

        self.name = "GSIS FEATURE MEMORY ENGINE v1.0"

        self.db = "database/qmos.db"

        self.create_table()

        print("==============================")
        print("GSIS FEATURE MEMORY ENGINE ONLINE")
        print("==============================")
        print("FEATURE STORAGE ACTIVE")


    def create_table(self):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feature_memory (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            symbol TEXT,

            timeframe TEXT,

            close REAL,

            return_pct REAL,

            log_return REAL,

            ema20 REAL,

            timestamp TEXT

        )
        """)

        conn.commit()

        conn.close()



    def save_feature(self, feature):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()


        cursor.execute("""
        INSERT INTO feature_memory
        (
            symbol,
            timeframe,
            close,
            return_pct,
            log_return,
            ema20,
            timestamp
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

        """,

        (

            feature.get("symbol"),

            feature.get("timeframe"),

            feature.get("close"),

            feature.get("return_pct"),

            feature.get("log_return"),

            feature.get("ema20"),

            feature.get(
                "timestamp",
                datetime.now(
                    timezone.utc
                ).isoformat()
            )

        ))


        conn.commit()

        conn.close()


        print("FEATURE MEMORY UPDATED")

        return feature



    def process(self, feature):

        print("==============================")
        print("FEATURE MEMORY UPDATE")
        print("==============================")

        print(feature)

        return self.save_feature(feature)



engine = FeatureMemoryEngine()
