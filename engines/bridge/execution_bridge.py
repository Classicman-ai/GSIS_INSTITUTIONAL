import os
import json
import time
from datetime import datetime, timezone


ENGINE = "GSIS_EXECUTION_BRIDGE_v2.0"

STATE_FILE = "data/live/EXECUTION_state.json"
RISK_FILE = "data/live/RISK_state.json"


def utc_now():
    return datetime.now(timezone.utc).isoformat()



def load_json(path):

    try:
        with open(path, "r") as file:
            return json.load(file)

    except Exception:
        return {}



def generate_execution():

    risk_data = load_json(RISK_FILE)

    risk_state = risk_data.get("state", {})


    symbol = risk_state.get(
        "symbol",
        "BTCUSDT"
    )


    risk_status = risk_state.get(
        "risk_status",
        "BLOCKED"
    )


    direction = risk_state.get(
        "direction",
        "NONE"
    )


    entry = risk_state.get(
        "entry",
        None
    )


    stop_loss = risk_state.get(
        "stop_loss",
        None
    )


    take_profit = risk_state.get(
        "take_profit",
        None
    )


    execution_status = "BLOCKED"

    order_instruction = "NO_ORDER"



    if risk_status == "APPROVED" and direction != "NONE":

        execution_status = "READY"

        order_instruction = {

            "symbol": symbol,

            "action": direction,

            "entry": entry,

            "stop_loss": stop_loss,

            "take_profit": take_profit

        }



    return {

        "symbol": symbol,

        "execution_status": execution_status,

        "order_instruction": order_instruction,

        "risk_status": risk_status,

        "direction": direction,

        "entry": entry,

        "stop_loss": stop_loss,

        "take_profit": take_profit

    }




def save_state():

    os.makedirs(
        "data/live",
        exist_ok=True
    )


    payload = {

        "engine": ENGINE,

        "status": "ACTIVE",

        "heartbeat": time.time(),

        "timestamp": utc_now(),

        "state": generate_execution()

    }



    with open(
        STATE_FILE,
        "w"
    ) as file:

        json.dump(
            payload,
            file,
            indent=4
        )


    return payload




def run():

    print("==============================")
    print("GSIS EXECUTION BRIDGE v2.0")
    print("==============================")


    while True:

        state = save_state()

        print("------------------------------")
        print("GSIS EXECUTION STATE")

        print(state)


        time.sleep(30)



if __name__ == "__main__":
    run()
