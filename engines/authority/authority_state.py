# ==========================================
# GSIS AUTHORITY STATE BRIDGE v1.0
# ==========================================

import json
import os
from datetime import datetime, timezone


STATE_FILE = "data/authority/authority_state.json"



def create_state():

    if not os.path.exists(STATE_FILE):

        state = {

            "symbol": None,

            "direction": "NONE",

            "confidence": 0,

            "setup": "NONE",

            "timeframe": None,

            "regime": "UNKNOWN",

            "bayesian": "UNKNOWN",

            "confirmation": False,

            "risk_status": "UNKNOWN",

            "timestamp":
            datetime.now(timezone.utc).isoformat()

        }


        save_state(state)



def save_state(state):

    with open(STATE_FILE,"w") as f:

        json.dump(
            state,
            f,
            indent=4
        )



def load_state():

    create_state()


    with open(STATE_FILE,"r") as f:

        return json.load(f)



def update_state(key,value):

    state = load_state()

    state[key] = value

    state["timestamp"] = (
        datetime.now(timezone.utc)
        .isoformat()
    )

    save_state(state)



if __name__ == "__main__":

    create_state()

    print("==============================")

    print("GSIS AUTHORITY STATE BRIDGE v1.0")

    print("==============================")

    print(load_state())
