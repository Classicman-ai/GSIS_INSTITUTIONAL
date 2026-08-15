import os
import sys
import sqlite3
from datetime import datetime, timezone


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)


print("==============================")
print("GSIS TRADE LIFECYCLE ENGINE v1.2 ONLINE")
print("==============================")
print("AUTO SCHEMA REPAIR + TRADE ID MANAGEMENT ACTIVE")
print("==============================")


DB_PATH = "database/qmos.db"


class TradeLifecycleEngine:


    def __init__(self):

        self.conn = sqlite3.connect(DB_PATH)

        self.repair_database()



    def repair_database(self):

        cursor = self.conn.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS trade_lifecycle (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            trade_id TEXT UNIQUE,

            symbol TEXT,

            direction TEXT,

            entry REAL,

            stop_loss REAL,

            take_profit REAL,

            confidence REAL,

            reasons TEXT,

            status TEXT,

            open_time TEXT

        )

        """)


        cursor.execute(
            "PRAGMA table_info(trade_lifecycle)"
        )

        columns = [
            row[1]
            for row in cursor.fetchall()
        ]


        required = [

            "trade_id",
            "symbol",
            "direction",
            "entry",
            "stop_loss",
            "take_profit",
            "confidence",
            "reasons",
            "status",
            "open_time"

        ]


        if not all(
            col in columns
            for col in required
        ):

            print(
                "OLD TRADE TABLE DETECTED - REBUILDING"
            )

            cursor.execute(
                "DROP TABLE trade_lifecycle"
            )


            cursor.execute("""

            CREATE TABLE trade_lifecycle (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                trade_id TEXT UNIQUE,

                symbol TEXT,

                direction TEXT,

                entry REAL,

                stop_loss REAL,

                take_profit REAL,

                confidence REAL,

                reasons TEXT,

                status TEXT,

                open_time TEXT

            )

            """)


        self.conn.commit()



    def generate_trade_id(self):

        timestamp = datetime.now(
            timezone.utc
        ).strftime(
            "%Y%m%d%H%M%S"
        )


        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM trade_lifecycle"
        )


        number = cursor.fetchone()[0] + 1


        return (
            f"GSIS-{timestamp}-{number:06d}"
        )



    def open_trade(
        self,
        symbol,
        direction,
        entry,
        stop_loss,
        take_profit,
        confidence,
        reasons
    ):


        trade_id = self.generate_trade_id()


        now = datetime.now(
            timezone.utc
        ).isoformat()


        if isinstance(reasons, list):

            reasons = " | ".join(
                reasons
            )


        cursor = self.conn.cursor()


        cursor.execute("""

        INSERT INTO trade_lifecycle (

            trade_id,

            symbol,

            direction,

            entry,

            stop_loss,

            take_profit,

            confidence,

            reasons,

            status,

            open_time

        )

        VALUES (?,?,?,?,?,?,?,?,?,?)

        """,

        (

            trade_id,

            symbol,

            direction,

            entry,

            stop_loss,

            take_profit,

            confidence,

            reasons,

            "OPEN",

            now

        ))


        self.conn.commit()


        result = {

            "trade_id": trade_id,

            "status": "TRADE OPENED",

            "symbol": symbol,

            "direction": direction,

            "entry": entry,

            "stop_loss": stop_loss,

            "take_profit": take_profit,

            "confidence": confidence,

            "time": now

        }


        print("==============================")
        print("GSIS TRADE CREATED")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = TradeLifecycleEngine()


    engine.open_trade(

        "XAUUSD",

        "SELL",

        2387.5,

        2387.8,

        2387.2,

        100,

        [

            "LIQUIDITY SWEEP CONFIRMED",

            "BEARISH ORDER BLOCK",

            "BEARISH FVG",

            "BEARISH CHoCH"

        ]

    )
