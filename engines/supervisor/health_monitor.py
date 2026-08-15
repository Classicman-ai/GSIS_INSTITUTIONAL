"""
=========================================
GSIS HEALTH MONITOR ENGINE
Version : 2.0
=========================================
"""

import os
import json
import time

from engines.supervisor.engine_registry import ENGINES


# Health scoring
HEALTH_SCORE = {
    "ONLINE": 100,
    "STALE": 70,
    "SLEEPING": 30,
    "OFFLINE": 0,
    "ERROR": -20
}


def load_state(path):

    if not os.path.exists(path):
        return None

    try:
        with open(path, "r") as file:
            return json.load(file)

    except Exception:
        return "ERROR"



def get_timestamp(data):

    if not isinstance(data, dict):
        return None

    if "heartbeat" in data:
        return float(data["heartbeat"])

    if "timestamp" in data:
        return float(data["timestamp"])

    return None



def classify_engine(path):

    data = load_state(path)

    if data == "ERROR":
        return {
            "status": "ERROR",
            "age": None
        }


    if data is None:

        return {
            "status": "OFFLINE",
            "age": None
        }


    timestamp = get_timestamp(data)


    if timestamp is None:

        return {
            "status": "ERROR",
            "age": None
        }


    age = time.time() - timestamp


    if age < 60:

        status = "ONLINE"


    elif age < 300:

        status = "STALE"


    elif age < 3600:

        status = "SLEEPING"


    else:

        status = "OFFLINE"



    return {

        "status": status,
        "age": round(age, 2)

    }



def calculate_health(results):

    total = 0

    count = len(results)


    for engine in results.values():

        total += HEALTH_SCORE.get(
            engine["status"],
            0
        )


    if count == 0:
        return 0


    return round(total / count, 2)



def run_health_monitor():


    results = {}


    for name, info in ENGINES.items():

        results[name] = classify_engine(
            info["file"]
        )


    health = calculate_health(results)


    if health >= 90:

        system_status = "OPERATIONAL"

    elif health >= 60:

        system_status = "DEGRADED"

    else:

        system_status = "CRITICAL"



    return {

        "system_health": health,

        "system_status": system_status,

        "online": sum(
            1 for x in results.values()
            if x["status"] == "ONLINE"
        ),

        "stale": sum(
            1 for x in results.values()
            if x["status"] == "STALE"
        ),

        "sleeping": sum(
            1 for x in results.values()
            if x["status"] == "SLEEPING"
        ),

        "offline": sum(
            1 for x in results.values()
            if x["status"] == "OFFLINE"
        ),

        "errors": sum(
            1 for x in results.values()
            if x["status"] == "ERROR"
        ),

        "engines": results

    }



if __name__ == "__main__":


    print("==============================")
    print("GSIS HEALTH MONITOR v2.0")
    print("==============================")


    state = run_health_monitor()


    print("------------------------------")
    print("GSIS HEALTH STATE")
    print(state)
