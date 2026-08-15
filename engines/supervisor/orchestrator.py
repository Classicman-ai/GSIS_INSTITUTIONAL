import os
import time
import json
import subprocess
from datetime import datetime, timezone


ENGINE = "GSIS_ORCHESTRATOR_v1.0"


ENGINES = {

    "HMM": "engines.bridge.hmm_bridge",
    "ORDERFLOW": "engines.bridge.orderflow_bridge",
    "STRUCTURE": "engines.bridge.structure_bridge",
    "FUSION": "engines.bridge.fusion_bridge",
    "DECISION": "engines.bridge.decision_bridge",
    "CONFIRMATION": "engines.bridge.confirmation_bridge",
    "QUALIFICATION": "engines.bridge.qualification_bridge",
    "RISK": "engines.bridge.risk_bridge",
    "EXECUTION": "engines.bridge.execution_bridge",
    "REPORT": "engines.bridge.report_bridge",
    "DATABASE": "engines.database.database_engine",
    "ALERT": "engines.alert.alert_engine"

}


PROCESS = {}


def timestamp():
    return datetime.now(timezone.utc).isoformat()



def start_engine(name, module):

    if name in PROCESS:
        if PROCESS[name].poll() is None:
            return "RUNNING"


    try:

        p = subprocess.Popen(
            [
                "python",
                "-m",
                module
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        PROCESS[name] = p

        return "STARTED"


    except Exception as e:

        return str(e)



def check_processes():

    state = {}

    for name, module in ENGINES.items():

        status = start_engine(
            name,
            module
        )

        state[name] = status


    return state



def save_state(data):

    os.makedirs(
        "data/live",
        exist_ok=True
    )


    payload = {

        "engine": ENGINE,

        "status": "ACTIVE",

        "heartbeat": time.time(),

        "timestamp": timestamp(),

        "state": data

    }


    with open(
        "data/live/orchestrator_state.json",
        "w"
    ) as f:

        json.dump(
            payload,
            f,
            indent=4
        )


    return payload



def run():

    print("==============================")
    print("GSIS ORCHESTRATOR v1.0")
    print("==============================")


    while True:

        state = check_processes()

        payload = save_state(state)

        print("------------------------------")
        print("GSIS ORCHESTRATOR STATE")
        print(payload)

        time.sleep(60)



if __name__ == "__main__":
    run()
