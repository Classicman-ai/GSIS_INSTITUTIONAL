import os
import sqlite3
import time
from datetime import datetime, timezone


DB_PATH = "data/gsis.db"


def heartbeat():
    return time.time()


def initialize_database():

    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS engine_states
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        engine TEXT,
        symbol TEXT,
        status TEXT,
        regime TEXT,
        score REAL,
        decision TEXT,
        risk_status TEXT,
        execution_status TEXT,
        timestamp TEXT
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_events
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        event TEXT,
        value REAL,
        timestamp TEXT
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trade_history
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        direction TEXT,
        entry REAL,
        stop_loss REAL,
        take_profit REAL,
        result TEXT,
        timestamp TEXT
    )
    """)


    conn.commit()
    conn.close()



def save_state():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
    """
    INSERT INTO engine_states
    (
    engine,
    symbol,
    status,
    regime,
    score,
    decision,
    risk_status,
    execution_status,
    timestamp
    )

    VALUES (?,?,?,?,?,?,?,?,?)
    """,

    (
    "GSIS_DATABASE_BRIDGE_v1.0",
    "BTCUSDT",
    "ACTIVE",
    "MARKDOWN",
    -30,
    "WAIT",
    "BLOCKED",
    "BLOCKED",
    datetime.now(timezone.utc).isoformat()
    ))

    conn.commit()
    conn.close()



def database_state():

    return {

    "engine":
    "GSIS_DATABASE_BRIDGE_v1.0",

    "status":
    "ACTIVE",

    "heartbeat":
    heartbeat(),

    "database":
    DB_PATH,

    "tables":
    [
    "engine_states",
    "market_events",
    "trade_history"
    ],

    "timestamp":
    datetime.now(timezone.utc).isoformat()

    }



def run():

    print("="*30)
    print("GSIS DATABASE BRIDGE v1.0")
    print("="*30)

    initialize_database()

    while True:

        save_state()

        print("-"*30)
        print("GSIS DATABASE STATE")
        print(database_state())

        time.sleep(30)



if __name__ == "__main__":
    run()
