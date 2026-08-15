import os
import time
import json
import sqlite3
from datetime import datetime, timezone


DB_PATH = "data/gsis.db"
STATE_PATH = "data/live/database.json"


def heartbeat():
    os.makedirs("data/live", exist_ok=True)

    state = {
        "engine": "DATABASE",
        "status": "ACTIVE",
        "heartbeat": time.time(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": DB_PATH
    }

    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=4)

    return state


def initialize():

    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        timeframe TEXT,
        price REAL,
        timestamp TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS signals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        direction TEXT,
        score REAL,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def run():

    print("==============================")
    print("GSIS DATABASE ENGINE v1.0")
    print("==============================")

    initialize()

    while True:

        state = heartbeat()

        print("------------------------------")
        print("GSIS DATABASE STATE")
        print(state)

        time.sleep(30)


if __name__ == "__main__":
    run()
