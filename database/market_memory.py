"""
=========================================================
GSIS INSTITUTIONAL
MARKET MEMORY DATABASE
Version: 1.0

Institutional Market Memory Storage
=========================================================
"""

import sqlite3
import uuid
import os
from datetime import datetime


class MarketMemoryDatabase:

    def __init__(self):

        self.db_path = "database/market_memory.db"

        self.connection = None

        self.cursor = None


    def initialize(self):

        os.makedirs("database", exist_ok=True)

        self.connection = sqlite3.connect(self.db_path)

        self.cursor = self.connection.cursor()

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS market_memory (

            memory_id TEXT PRIMARY KEY,

            timestamp TEXT,

            symbol TEXT,

            timeframe TEXT,

            open REAL,

            high REAL,

            low REAL,

            close REAL,

            return_pct REAL,

            volatility REAL,

            direction TEXT,

            volatility_state TEXT,

            regime TEXT,

            pattern_id TEXT,

            event_id TEXT,

            probability REAL,

            confidence_grade TEXT,

            decision TEXT,

            outcome TEXT,

            created_at TEXT

        )

        """)

        self.connection.commit()

        print("MARKET MEMORY DATABASE ONLINE")


    def create_memory(self, record):

        memory_id = str(uuid.uuid4())

        self.cursor.execute("""

        INSERT INTO market_memory (

            memory_id,

            timestamp,

            symbol,

            timeframe,

            open,

            high,

            low,

            close,

            return_pct,

            volatility,

            direction,

            volatility_state,

            regime,

            pattern_id,

            event_id,

            probability,

            confidence_grade,

            decision,

            outcome,

            created_at

        )

        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

        """, (

            memory_id,

            record.get("timestamp"),

            record.get("symbol"),

            record.get("timeframe"),

            record.get("open"),

            record.get("high"),

            record.get("low"),

            record.get("close"),

            record.get("return_pct"),

            record.get("volatility"),

            record.get("direction"),

            record.get("volatility_state"),

            record.get("regime"),

            record.get("pattern_id"),

            record.get("event_id"),

            record.get("probability"),

            record.get("confidence_grade"),

            record.get("decision"),

            record.get("outcome"),

            str(datetime.utcnow())

        ))

        self.connection.commit()

        print(f"MEMORY STORED: {memory_id}")

        return memory_id


    def get_memory(self, memory_id):

        self.cursor.execute(

            "SELECT * FROM market_memory WHERE memory_id=?",

            (memory_id,)

        )

        return self.cursor.fetchone()


    def close(self):

        if self.connection:

            self.connection.close()
