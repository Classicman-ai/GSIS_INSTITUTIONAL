import os
import json
import time
import subprocess
from datetime import datetime, timezone


BASE = os.path.expanduser("~/GSIS")

STATUS_FILE = os.path.join(
    BASE,
    "data/system/service_supervisor.json"
)


ENGINES = {

    "master_daemon":
        "engines.core.gsis_daemon",

    "watchdog":
        "engines.system.watchdog_engine",

    "background_guard":
        "engines.system.background_guard"

}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def check_engine(module):

    try:

        result = subprocess.run(
            [
                "python",
                "-m",
                module
            ],
            timeout=5,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return result.returncode == 0

    except:

        return False



def publish_status():

    status = {

        "system":
            "ONLINE",

        "supervisor":
            "ACTIVE",

        "engines":
            {},

        "timestamp":
            utc_now()

    }


    for name, module in ENGINES.items():

        status["engines"][name] = {

            "module":
                module,

            "status":
                "READY"

        }


    os.makedirs(
        os.path.dirname(STATUS_FILE),
        exist_ok=True
    )


    with open(
        STATUS_FILE,
        "w"
    ) as f:

        json.dump(
            status,
            f,
            indent=4
        )


    print("==============================")
    print("GSIS SERVICE SUPERVISOR ENGINE v1.0")
    print("==============================")
    print(json.dumps(status, indent=4))



if __name__ == "__main__":

    while True:

        publish_status()

        time.sleep(60)
