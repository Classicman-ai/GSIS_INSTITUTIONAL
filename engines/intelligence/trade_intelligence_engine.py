from datetime import datetime, timezone
import sqlite3
import os


class TradeIntelligenceEngine:


    def __init__(self):

        self.engine_name = "GSIS TRADE INTELLIGENCE ENGINE"
        self.version = "1.0"

        os.makedirs("database", exist_ok=True)

        self.database = "database/gsis_learning.db"

        self.initialize_database()



    def initialize_database(self):

        conn = sqlite3.connect(self.database)

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS trade_memory (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            symbol TEXT,

            direction TEXT,

            regime TEXT,

            confidence REAL,

            fusion_score INTEGER,

            entry REAL,

            stop_loss REAL,

            tp1 REAL,

            tp2 REAL,

            tp3 REAL,

            result TEXT

        )
        """)

        conn.commit()

        conn.close()



    def save_trade(self, context):

        signal = context.signal or {}
        risk = context.risk or {}
        regime = context.regime or {}
        fusion = context.fusion or {}


        conn = sqlite3.connect(self.database)

        cursor = conn.cursor()


        cursor.execute("""
        INSERT INTO trade_memory

        (
        timestamp,
        symbol,
        direction,
        regime,
        confidence,
        fusion_score,
        entry,
        stop_loss,
        tp1,
        tp2,
        tp3,
        result
        )

        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)

        """,

        (

        datetime.now(timezone.utc).isoformat(),

        context.symbol,

        signal.get("direction","NO_TRADE"),

        regime.get("market_regime","UNKNOWN"),

        fusion.get("confidence",0),

        fusion.get("fusion_score",0),

        risk.get("entry"),

        risk.get("stop_loss"),

        risk.get("targets",{}).get("TP1"),

        risk.get("targets",{}).get("TP2"),

        risk.get("targets",{}).get("TP3"),

        "OPEN"

        ))


        conn.commit()

        conn.close()



    def analytics(self):

        conn = sqlite3.connect(self.database)

        cursor = conn.cursor()


        cursor.execute(
            "SELECT COUNT(*) FROM trade_memory"
        )

        total = cursor.fetchone()[0]


        cursor.execute(
            """
            SELECT regime, COUNT(*)
            FROM trade_memory
            GROUP BY regime
            ORDER BY COUNT(*) DESC
            LIMIT 1
            """
        )

        best_regime = cursor.fetchone()


        conn.close()


        return {

            "total_trades": total,

            "best_regime":
            best_regime[0]
            if best_regime else "NONE"

        }



    def run(self, context):


        self.save_trade(context)

        report = self.analytics()


        return {

            "engine":
            self.engine_name,

            "version":
            self.version,

            "symbol":
            context.symbol,

            "timestamp":
            datetime.now(timezone.utc).isoformat(),


            "learning_database":
            self.database,


            "stored":
            True,


            "analytics":
            report,


            "status":
            "INTELLIGENCE_ACTIVE"

        }



if __name__ == "__main__":


    class Dummy:

        symbol="BTCUSDT"

        signal={
            "direction":"LONG"
        }

        risk={

            "entry":68500,

            "stop_loss":67500,

            "targets":{

                "TP1":69500,

                "TP2":70500,

                "TP3":72000
            }

        }

        regime={

            "market_regime":"TRENDING_UP"

        }

        fusion={

            "confidence":0.86,

            "fusion_score":6

        }


    engine = TradeIntelligenceEngine()

    print(
        engine.run(Dummy())
    )
