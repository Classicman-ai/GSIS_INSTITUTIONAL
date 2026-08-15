import os
import json
import subprocess
import time
from datetime import datetime, timezone


BASE=os.path.expanduser("~/GSIS")

STATUS_FILE=os.path.join(
    BASE,
    "data/system/auto_recovery.json"
)

LOG_FILE=os.path.join(
    BASE,
    "data/system/logs/recovery.log"
)


SERVICES={

    "master_daemon":
    "engines.core.gsis_daemon",

    "watchdog":
    "engines.system.watchdog_engine",

    "supervisor":
    "engines.system.service_supervisor"

}



def now():

    return datetime.now(
        timezone.utc
    ).isoformat()



def log(msg):

    os.makedirs(
        os.path.dirname(LOG_FILE),
        exist_ok=True
    )

    with open(
        LOG_FILE,
        "a"
    ) as f:

        f.write(
            now()+" "+msg+"\n"
        )



def is_running(module):

    try:

        result=subprocess.check_output(
            [
                "pgrep",
                "-af",
                module
            ]
        ).decode()

        return module in result

    except:

        return False



def restart(module):

    log(
        "RESTARTING "+module
    )

    subprocess.Popen(
        [
            "python",
            "-m",
            module
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )



def monitor():

    state={

        "system":"ONLINE",

        "recovery":"ACTIVE",

        "engines":{},

        "timestamp":now()

    }


    for name,module in SERVICES.items():

        if is_running(module):

            state["engines"][name]="RUNNING"

        else:

            state["engines"][name]="RESTARTED"

            restart(module)



    os.makedirs(
        os.path.dirname(STATUS_FILE),
        exist_ok=True
    )


    with open(
        STATUS_FILE,
        "w"
    ) as f:

        json.dump(
            state,
            f,
            indent=4
        )


    print("==============================")
    print("GSIS AUTO RECOVERY ENGINE v1.1")
    print("==============================")
    print(json.dumps(state,indent=4))



if __name__=="__main__":

    while True:

        monitor()

        time.sleep(60)
