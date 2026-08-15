# ==========================================
# GSIS AUTHORITY DATABASE ENGINE v1.1
# ==========================================

import sqlite3
from datetime import datetime, timezone


DB_PATH = "data/gsis.db"


def create_table():

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS authority_log (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        trade_id TEXT,

        symbol TEXT,

        direction TEXT,

        decision TEXT,

        status TEXT,

        confidence REAL,

        setup TEXT,

        timeframe TEXT,

        reason TEXT,

        authority_version TEXT,

        timestamp TEXT

    )
    """)

    conn.commit()
    conn.close()



def save_decision(data):

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()


    cur.execute("""
    INSERT INTO authority_log
    (
        trade_id,
        symbol,
        direction,
        decision,
        status,
        confidence,
        setup,
        timeframe,
        reason,
        authority_version,
        timestamp
    )

    VALUES (?,?,?,?,?,?,?,?,?,?,?)

    """,

    (

        data.get("trade_id"),

        data.get("symbol"),

        data.get("direction"),

        data.get("decision"),

        data.get("status"),

        data.get("confidence"),

        data.get("setup"),

        data.get("timeframe"),

        data.get("reason",""),

        data.get("authority"),

        datetime.now(timezone.utc).isoformat()

    ))


    conn.commit()

    conn.close()
