"""
=========================================================
GSIS INSTITUTIONAL
EVENT INTELLIGENCE DATABASE
Version: 1.0

Economic + Geopolitical Event Memory
=========================================================
"""

import sqlite3
import uuid
import os
from datetime import datetime


class EventDatabase:


    def __init__(self):

        self.db_path = "database/event_memory.db"

        self.connection = None

        self.cursor = None



    def initialize(self):


        os.makedirs(
            "database",
            exist_ok=True
        )


        self.connection = sqlite3.connect(
            self.db_path
        )

        self.cursor = self.connection.cursor()



        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS events (

            event_id TEXT PRIMARY KEY,

            event_type TEXT,

            event_name TEXT,

            country TEXT,

            importance TEXT,

            event_time TEXT,

            forecast REAL,

            actual REAL,

            previous REAL,

            affected_asset TEXT,

            volatility_before REAL,

            volatility_after REAL,

            market_reaction TEXT,

            pattern_id TEXT,

            created_at TEXT

        )

        """)


        self.connection.commit()


        print(
            "EVENT INTELLIGENCE DATABASE ONLINE"
        )



    def create_event(self, event):


        event_id = (

            "EVT-"

            +

            str(uuid.uuid4())[:8].upper()

        )


        self.cursor.execute("""

        INSERT INTO events (

            event_id,

            event_type,

            event_name,

            country,

            importance,

            event_time,

            forecast,

            actual,

            previous,

            affected_asset,

            volatility_before,

            volatility_after,

            market_reaction,

            pattern_id,

            created_at

        )

        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

        """,

        (

            event_id,

            event.get("event_type"),

            event.get("event_name"),

            event.get("country"),

            event.get("importance"),

            event.get("event_time"),

            event.get("forecast"),

            event.get("actual"),

            event.get("previous"),

            event.get("affected_asset"),

            event.get("volatility_before"),

            event.get("volatility_after"),

            event.get("market_reaction"),

            event.get("pattern_id"),

            str(datetime.utcnow())

        ))


        self.connection.commit()


        print(
            "EVENT STORED:",
            event_id
        )


        return event_id



    def close(self):


        if self.connection:

            self.connection.close()
