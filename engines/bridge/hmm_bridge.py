import os
import json
import time
from datetime import datetime, timezone


ENGINE_NAME = "GSIS_HMM_BRIDGE_v3.0"
SYMBOL = "BTCUSDT"

INPUT_FILE = "data/live/hmm_regime_state.json"
OUTPUT_FILE = "data/live/HMM_state.json"


def utc_time():
    return datetime.now(timezone.utc).isoformat()


def load_hmm_state():

    if os.path.exists(INPUT_FILE):

        try:
            with open(INPUT_FILE, "r") as f:
                return json.load(f)

        except Exception:
            pass


    # fallback state

    return {
        "symbol": SYMBOL,
        "current_regime": "UNKNOWN",
        "probabilities": {},
        "confidence": 0,
        "features": {}
    }



def write_heartbeat(state):

    os.makedirs("data/live", exist_ok=True)

    heartbeat_state = {

        "engine": "HMM",

        "status": "ACTIVE",

        "heartbeat": time.time(),

        "timestamp": utc_time(),

        "state": state

    }


    with open(OUTPUT_FILE, "w") as f:
        json.dump(
            heartbeat_state,
            f,
            indent=4
        )


    return heartbeat_state



def run():

    print("==============================")
    print("GSIS HMM BRIDGE ENGINE v3.0")
    print("==============================")


    while True:

        hmm_state = load_hmm_state()

        output = write_heartbeat(hmm_state)


        print("------------------------------")
        print("GSIS HMM BRIDGE STATE")

        print(output)


        time.sleep(30)



if __name__ == "__main__":

    run()
