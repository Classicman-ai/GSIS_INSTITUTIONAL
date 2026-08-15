import time
import sqlite3
import os
from collections import Counter


DB_PATH = "database/gsis_intelligence.db"


print("==============================")
print("GSIS SELF OPTIMIZATION ENGINE v1.0")
print("==============================")


def load_states():

    if not os.path.exists(DB_PATH):
        return []

    try:

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
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

        conn.close()

        return rows

    except Exception:

        return []



def analyze(states):

    if not states:

        return {

            "optimization_status": "NO_DATA",
            "recommendation": "WAIT_FOR_DATA"

        }



    blocked = 0
    executed = 0

    regimes = []
    directions = []
    scores = []
    confidence = []

    failure_reasons = []



    for state in states:

        regime = state[0]
        direction = state[1]
        status = state[2]


        regimes.append(regime)
        directions.append(direction)


        try:

            scores.append(float(state[3]))
            confidence.append(float(state[4]))

        except:

            pass



        if status == "BLOCKED":

            blocked += 1


            if regime == "MARKDOWN":
                failure_reasons.append(
                    "BEARISH_REGIME"
                )


            if direction == "NONE":
                failure_reasons.append(
                    "NO_DIRECTION"
                )



        elif status == "EXECUTED":

            executed += 1



    avg_confidence = 0

    if confidence:

        avg_confidence = round(
            sum(confidence) /
            len(confidence),
            2
        )



    avg_score = 0

    if scores:

        avg_score = round(
            sum(scores) /
            len(scores),
            2
        )



    dominant_failure = "NONE"

    if failure_reasons:

        dominant_failure = (
            Counter(failure_reasons)
            .most_common(1)[0][0]
        )



    recommendations = []


    if blocked == len(states):

        recommendations.append(
            "Increase signal qualification before execution"
        )


    if avg_confidence < 60:

        recommendations.append(
            "Require stronger market confirmation"
        )


    if dominant_failure == "BEARISH_REGIME":

        recommendations.append(
            "Wait for regime transition or confirmed continuation"
        )


    if dominant_failure == "NO_DIRECTION":

        recommendations.append(
            "Improve directional scoring model"
        )



    readiness = round(

        avg_confidence * 0.5
        +
        (executed / len(states) * 100) * 0.5,

        2

    )



    return {

        "engine":
            "GSIS_SELF_OPTIMIZATION_v1.0",

        "total_states":
            len(states),

        "executed":
            executed,

        "blocked":
            blocked,

        "average_score":
            avg_score,

        "average_confidence":
            avg_confidence,

        "dominant_regime":
            Counter(regimes)
            .most_common(1)[0][0],

        "dominant_failure":
            dominant_failure,

        "system_readiness":
            readiness,

        "recommendations":
            recommendations

    }



def run():

    while True:

        states = load_states()

        result = analyze(states)

        print("------------------------------")
        print("GSIS OPTIMIZATION STATE")
        print(result)

        time.sleep(60)



if __name__ == "__main__":

    run()
