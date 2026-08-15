import os
import time
import json
import subprocess
from datetime import datetime, timezone


ENGINE = "GSIS_CORE_SUPERVISOR_v3.0"


STATE_FILE = "data/live/supervisor_state.json"


ENGINES = [

    "engines.data.market_bridge",

    "engines.supervisor.health_monitor",

    "engines.scoring.regime_score_engine",

    "engines.bayesian.bayesian_engine",

    "engines.signal.master_signal_engine",

    "engines.confirmation.confirmation_engine",

    "engines.qualification.qualification_engine",

    "engines.risk.risk_engine",

    "engines.execution.execution_engine",

    "engines.report.report_engine"

]


processes = []



def now():

    return datetime.now(
        timezone.utc
    ).isoformat()



def save(data):

    os.makedirs(
        "data/live",
        exist_ok=True
    )

    with open(
        STATE_FILE,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )



def start_engine(module):

    try:

        p = subprocess.Popen(
            [
                "python",
                "-m",
                module
            ]
        )

        processes.append(
            {
                "module":module,
                "pid":p.pid
            }
        )


        print(
            "STARTED:",
            module
        )


    except Exception as e:

        print(
            "FAILED:",
            module,
            e
        )



def run():

    print("==============================")
    print("GSIS CORE SUPERVISOR v3.0")
    print("==============================")


    for engine in ENGINES:

        start_engine(
            engine
        )


    while True:


        state = {

            "engine":ENGINE,

            "status":"ACTIVE",

            "heartbeat":time.time(),

            "timestamp":now(),

            "running_engines":processes

        }


        save(
            state
        )


        print("------------------------------")
        print(
            "GSIS CORE STATUS"
        )

        print(
            state
        )


        time.sleep(30)



if __name__ == "__main__":

    run()
