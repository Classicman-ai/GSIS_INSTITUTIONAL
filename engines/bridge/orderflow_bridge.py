import os
import json
import time
from datetime import datetime, timezone


ENGINE_NAME = "GSIS_ORDERFLOW_BRIDGE_v1.0"

SYMBOL = "BTCUSDT"

OUTPUT_FILE = "data/live/ORDERFLOW_state.json"


def utc_time():
    return datetime.now(timezone.utc).isoformat()



def generate_orderflow_state():

    return {

        "symbol": SYMBOL,

        "buy_pressure": 0.0,

        "sell_pressure": 0.0,

        "delta": 0.0,

        "imbalance": "NEUTRAL",

        "status": "ACTIVE"

    }



def write_state():

    os.makedirs("data/live", exist_ok=True)


    state = {

        "engine": "ORDERFLOW",

        "status": "ACTIVE",

        "heartbeat": time.time(),

        "timestamp": utc_time(),

        "state": generate_orderflow_state()

    }


    with open(OUTPUT_FILE,"w") as f:
        json.dump(state,f,indent=4)


    return state



def run():

    print("==============================")
    print("GSIS ORDERFLOW BRIDGE v1.0")
    print("==============================")


    while True:

        state = write_state()

        print("------------------------------")
        print("GSIS ORDERFLOW STATE")
        print(state)

        time.sleep(30)



if __name__ == "__main__":
    run()
