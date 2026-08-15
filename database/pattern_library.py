"""
=========================================================
GSIS INSTITUTIONAL
PATTERN LIBRARY DATABASE
Version: 1.0

Institutional Pattern Knowledge Base
=========================================================
"""

import sqlite3
import uuid
import os
from datetime import datetime


class PatternLibraryDatabase:

    def __init__(self):

        self.db_path = "database/pattern_library.db"
        self.connection = None
        self.cursor = None


    def initialize(self):

        os.makedirs("database", exist_ok=True)

        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS pattern_library (

            pattern_id TEXT PRIMARY KEY,

            pattern_name TEXT,

            symbol TEXT,

            timeframe TEXT,

            regime TEXT,

            direction TEXT,

            confidence_grade TEXT,

            probability REAL,

            total_occurrences INTEGER,

            successful_occurrences INTEGER,

            win_rate REAL,

            first_seen TEXT,

            last_seen TEXT,

            created_at TEXT

        )

        """)

        self.connection.commit()

        print("PATTERN LIBRARY ONLINE")


    def create_pattern(self, pattern):

        pattern_id = "PAT-" + str(uuid.uuid4())[:8].upper()

        now = str(datetime.utcnow())

        self.cursor.execute("""

        INSERT INTO pattern_library (

            pattern_id,
            pattern_name,
            symbol,
            timeframe,
            regime,
            direction,
            confidence_grade,
            probability,
            total_occurrences,
            successful_occurrences,
            win_rate,
            first_seen,
            last_seen,
            created_at

        )

        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)

        """, (

            pattern_id,
            pattern.get("pattern_name"),
            pattern.get("symbol"),
            pattern.get("timeframe"),
            pattern.get("regime"),
            pattern.get("direction"),
            pattern.get("confidence_grade"),
            pattern.get("probability"),
            1,
            0,
            0.0,
            now,
            now,
            now

        ))

        self.connection.commit()

        print("PATTERN CREATED:", pattern_id)

        return pattern_id


    def close(self):

        if self.connection:

            self.connection.close()
