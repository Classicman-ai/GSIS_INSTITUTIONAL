import os
import json
import time
from datetime import datetime, timezone


ENGINE = "GSIS_REGIME_MEMORY_ENGINE_v1.2"

OUTPUT = "data/live/regime_memory.json"

SOURCES = [
    "data/live/bayesian_state.json",
    "data/live/BAYESIAN_state.json",
    "data/live/hmm_state.json",
    "data/live/HMM_state.json",
    "data/live/regime_memory.json"
]


def now():
    return datetime.now(timezone.utc).isoformat()


def load(path):

    try:
        with open(path,"r") as f:
            return json.load(f)

    except:
        return {}



def save(path,data):

    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    with open(path,"w") as f:
        json.dump(
            data,
            f,
            indent=4
        )



def detect_regime():

    for source in SOURCES:

        data = load(source)

        if not data:
            continue


        checks = [

            data.get("current_regime"),

            data.get("regime"),

            data.get("last_regime"),

            data.get("state",{}).get("regime"),

            data.get("state",{}).get("market",{}).get("regime"),

            data.get("prediction",{}).get("regime")

        ]


        for value in checks:

            if value:

                return value



    return "UNKNOWN"



def build():

    regime = detect_regime()


    return {

        "engine":ENGINE,

        "status":"ACTIVE",

        "heartbeat":time.time(),

        "timestamp":now(),

        "current_regime":regime,

        "regime_statistics":{

            "last_regime":regime,

            "MARKUP":{
                "samples":0,
                "wins":0,
                "losses":0,
                "accuracy":0
            },

            "MARKDOWN":{
                "samples":0,
                "wins":0,
                "losses":0,
                "accuracy":0
            },

            "RANGE":{
                "samples":0,
                "wins":0,
                "losses":0,
                "accuracy":0
            }

        }

    }



def run():

    print("==============================")
    print("GSIS REGIME MEMORY ENGINE v1.2")
    print("==============================")


    while True:

        state = build()

        save(
            OUTPUT,
            state
        )


        print("------------------------------")
        print("GSIS REGIME MEMORY STATE")
        print(state)


        time.sleep(60)



if __name__=="__main__":
    run()
