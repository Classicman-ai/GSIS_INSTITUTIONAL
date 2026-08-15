import sqlite3
import json
import time
import os
from datetime import datetime, timezone


DB_PATH = "database/gsis_intelligence.db"
LIVE_PATH = "data/live"


os.makedirs("database", exist_ok=True)



def initialize():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gsis_states (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp REAL,
        datetime TEXT,
        symbol TEXT,
        engine TEXT,
        regime TEXT,
        direction TEXT,
        status TEXT,
        score REAL,
        confidence REAL,
        data TEXT
    )
    """)

    conn.commit()
    conn.close()



def load_json(filename):

    path = os.path.join(
        LIVE_PATH,
        filename
    )

    try:

        with open(path, "r") as f:

            return json.load(f)

    except Exception:

        return {}



def collect_state():

    files = [

        "hmm_regime_state.json",
        "master_signal.json",
        "risk_state.json",
        "execution_state.json"

    ]


    result = {}


    for file in files:

        data = load_json(file)

        if data:

            result[file] = data


    return result



def save_state():

    state = collect_state()


    if not state:

        return None



    regime = "UNKNOWN"
    direction = "NONE"
    status = "UNKNOWN"
    score = 0
    confidence = 0



    for name, data in state.items():


        if "current_regime" in data:

            regime = data["current_regime"]


        if "regime" in data:

            regime = data["regime"]


        if "direction" in data:

            direction = data["direction"]


        if "execution_status" in data:

            status = data["execution_status"]


        if "institutional_score" in data:

            score = data["institutional_score"]


        if "confidence" in data:

            confidence = data["confidence"]



    timestamp = time.time()


    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO gsis_states
        (
            timestamp,
            datetime,
            symbol,
            engine,
            regime,
            direction,
            status,
            score,
            confidence,
            data
        )
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        (
            timestamp,
            datetime.now(timezone.utc).isoformat(),
            "BTCUSDT",
            "GSIS_DATABASE_LOGGER_v1.0",
            regime,
            direction,
            status,
            score,
            confidence,
            json.dumps(state)
        )
    )


    conn.commit()

    conn.close()



    return {

        "engine":
        "GSIS_DATABASE_LOGGER_v1.0",

        "symbol":
        "BTCUSDT",

        "regime":
        regime,

        "direction":
        direction,

        "status":
        status,

        "saved":
        True,

        "timestamp":
        timestamp

    }



def run():

    initialize()


    print("==============================")
    print("GSIS DATABASE LOGGER ENGINE v1.0")
    print("==============================")


    while True:

        result = save_state()


        print("------------------------------")
        print("GSIS DATABASE STATE")
        print(result)


        time.sleep(15)



if __name__ == "__main__":

    run()
