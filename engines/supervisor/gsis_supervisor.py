"""
=========================================
GSIS SUPERVISOR ENGINE
Version : 2.0
=========================================
"""

import json
import os
import time
from datetime import datetime, timezone

from engines.supervisor.health_monitor import run_health_monitor
from engines.supervisor.watchdog import run_watchdog



OUTPUT = "data/live/supervisor_state.json"



def save_state(state):

    os.makedirs(
        "data/live",
        exist_ok=True
    )

    with open(
        OUTPUT,
        "w"
    ) as file:

        json.dump(
            state,
            file,
            indent=4
        )



def build_supervisor():

    health = run_health_monitor()

    watchdog = run_watchdog()


    state = {

        "engine":
        "GSIS_SUPERVISOR_v2.0",


        "timestamp":
        datetime.now(
            timezone.utc
        ).isoformat(),


        "system_health":
        health["system_health"],


        "system_status":
        health["system_status"],


        "online":
        health["online"],


        "stale":
        health["stale"],


        "sleeping":
        health["sleeping"],


        "offline":
        health["offline"],


        "errors":
        health["errors"],


        "watchdog_actions":
        watchdog["actions"],


        "engines":
        health["engines"]

    }


    return state



def run():

    print("==============================")
    print("GSIS SUPERVISOR v2.0")
    print("==============================")


    while True:


        state = build_supervisor()


        save_state(state)


        print("------------------------------")
        print("GSIS SUPERVISOR STATE")

        print(state)



        time.sleep(30)



if __name__ == "__main__":

    run()
