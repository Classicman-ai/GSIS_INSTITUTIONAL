"""
=========================================================
GSIS INSTITUTIONAL
Pattern Database Engine
Version: 1.0
=========================================================
"""

import sqlite3
from datetime import datetime
import os


class PatternDatabase:

    def __init__(self, db_path="database/patterns.db"):

        self.db_path = db_path

        os.makedirs(
            os.path.dirname(db_path),
            exist_ok=True
        )


    def connect(self):

        return sqlite3.connect(
            self.db_path
        )


    def initialize(self):

        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS patterns (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            pattern_id TEXT UNIQUE,

            asset TEXT,

            timeframe TEXT,

            pattern_type TEXT,

            conditions TEXT,

            occurrences INTEGER DEFAULT 0,

            successful INTEGER DEFAULT 0,

            failed INTEGER DEFAULT 0,

            probability REAL DEFAULT 0,

            confidence REAL DEFAULT 0,

            status TEXT DEFAULT 'ACTIVE',

            created_at TEXT,

            updated_at TEXT

        )
        """)


        conn.commit()
        conn.close()


        print(
            "[PATTERN DATABASE] Initialized"
        )


    def create_pattern_id(self):

        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT COUNT(*) 
            FROM patterns
            """
        )

        count = cursor.fetchone()[0]


        conn.close()


        return (
            f"GSIS-PAT-{count+1:06d}"
        )


    def add_pattern(
            self,
            asset,
            timeframe,
            pattern_type,
            conditions):


        pattern_id = self.create_pattern_id()


        conn = self.connect()

        cursor = conn.cursor()


        now = datetime.utcnow()


        cursor.execute("""
        INSERT INTO patterns (

            pattern_id,
            asset,
            timeframe,
            pattern_type,
            conditions,
            created_at,
            updated_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

        """,

        (
            pattern_id,
            asset,
            timeframe,
            pattern_type,
            str(conditions),
            str(now),
            str(now)
        ))


        conn.commit()

        conn.close()


        return pattern_id



    def update_result(
            self,
            pattern_id,
            success):


        conn = self.connect()

        cursor = conn.cursor()


        if success:

            cursor.execute("""
            UPDATE patterns
            SET successful = successful + 1
            WHERE pattern_id = ?
            """,
            (pattern_id,))


        else:

            cursor.execute("""
            UPDATE patterns
            SET failed = failed + 1
            WHERE pattern_id = ?
            """,
            (pattern_id,))


        cursor.execute("""
        UPDATE patterns
        SET occurrences = successful + failed,
            probability =
            CASE
            WHEN occurrences > 0
            THEN successful * 100.0 / occurrences
            ELSE 0
            END,
            updated_at = ?

        WHERE pattern_id = ?

        """,
        (
            str(datetime.utcnow()),
            pattern_id
        ))


        conn.commit()

        conn.close()
