import time
import json
import os
from datetime import datetime, timezone


ENGINE = "STRUCTURE"
SYMBOL = "BTCUSDT"

STATE_FILE = "data/live/STRUCTURE_state.json"


def utc_time():
    return datetime.now(timezone.utc).isoformat()


def create_structure_state():

    return {

        "symbol": SYMBOL,

        "trend": "NEUTRAL",

        "internal_structure": "RANGE",

        "external_structure": "RANGE",

        "BOS": False,

        "CHOCH": False,

        "liquidity_event": "NONE",

        "order_block": "NONE",

        "fair_value_gap": "NONE",

        "structure_score": 0

    }



def save_state():

    os.makedirs("data/live", exist_ok=True)

    payload = {

        "engine": ENGINE,

        "status": "ACTIVE",

        "heartbeat": time.time(),

        "timestamp": utc_time(),

        "state": create_structure_state()

    }


    with open(STATE_FILE, "w") as f:

        json.dump(
            payload,
            f,
            indent=4
        )


    return payload



def run():

    print("==============================")
    print("GSIS STRUCTURE BRIDGE v2.0")
    print("==============================")


    while True:

        state = save_state()

        print("------------------------------")
        print("GSIS STRUCTURE STATE")
        print(state)

        time.sleep(30)



if __name__ == "__main__":
    run()
