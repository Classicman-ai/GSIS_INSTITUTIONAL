import sqlite3
import time
import os
from collections import Counter


DB_PATH = "database/gsis_intelligence.db"


print("==============================")
print("GSIS PERFORMANCE ANALYTICS ENGINE v1.0")
print("==============================")


def connect_db():

    if not os.path.exists(DB_PATH):
        return None

    return sqlite3.connect(DB_PATH)



def load_states():

    conn = connect_db()

    if conn is None:
        return []

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT
                timestamp,
                symbol,
                regime,
                direction,
                status,
                score,
                confidence,
                data
            FROM gsis_states
            ORDER BY timestamp ASC
            """
        )

        rows = cursor.fetchall()

    except Exception:

        rows = []

    conn.close()

    return rows



def analyze(states):

    total = len(states)

    if total == 0:

        return {

            "total_states": 0,
            "system_readiness": 0,
            "message": "NO DATA"

        }



    regimes = []
    statuses = []
    directions = []
    scores = []
    confidence = []


    for s in states:

        regimes.append(s[2])
        directions.append(s[3])
        statuses.append(s[4])

        try:
            scores.append(float(s[5]))
            confidence.append(float(s[6]))

        except:

            pass



    blocked = statuses.count("BLOCKED")
    watch = statuses.count("WATCH")
    executed = statuses.count("EXECUTED")



    avg_score = round(
        sum(scores) / len(scores),2
    ) if scores else 0



    avg_confidence = round(
        sum(confidence) / len(confidence),2
    ) if confidence else 0



    block_rate = round(
        (blocked / total) * 100,
        2
    )



    readiness = round(

        (
            avg_confidence * 0.4
            +
            (100 - block_rate) * 0.4
            +
            min(abs(avg_score),100) * 0.2

        ),

        2

    )



    return {

        "total_states": total,

        "executed": executed,

        "watch_states": watch,

        "blocked": blocked,

        "block_rate": block_rate,

        "average_score": avg_score,

        "average_confidence": avg_confidence,

        "dominant_regime":
            Counter(regimes).most_common(1)[0][0],

        "dominant_direction":
            Counter(directions).most_common(1)[0][0],

        "system_readiness": readiness

    }



def run():

    while True:

        states = load_states()

        result = analyze(states)


        print("------------------------------")

        print("GSIS PERFORMANCE STATE")

        print(result)


        time.sleep(30)



if __name__ == "__main__":

    run()
