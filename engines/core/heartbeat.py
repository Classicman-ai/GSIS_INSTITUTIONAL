"""
=========================================
GSIS HEARTBEAT CORE ENGINE
Version : 1.0
Purpose : Engine-to-Supervisor communication
=========================================
"""

import os
import json
import time
from datetime import datetime, timezone


LIVE_PATH = "data/live"



def write_heartbeat(engine, state=None, status="ACTIVE"):

    os.makedirs(
        LIVE_PATH,
        exist_ok=True
    )


    filename = engine.lower() + "_state.json"


    filepath = os.path.join(
        LIVE_PATH,
        filename
    )


    heartbeat_state = {

        "engine": engine,

        "status": status,

        "heartbeat": time.time(),

        "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "state": state or {}

    }


    with open(
        filepath,
        "w"
    ) as file:

        json.dump(
            heartbeat_state,
            file,
            indent=4
        )


    return heartbeat_state



if __name__ == "__main__":


    print("==============================")
    print("GSIS HEARTBEAT CORE v1.0")
    print("==============================")


    test = write_heartbeat(
        "TEST",
        {
            "message":
            "heartbeat operational"
        }
    )


    print(test)
