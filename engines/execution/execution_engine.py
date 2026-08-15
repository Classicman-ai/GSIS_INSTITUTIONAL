import os
import json
import time
from datetime import datetime, timezone


ENGINE = "GSIS_EXECUTION_ENGINE_v3.0"

OUTPUT = "data/live/EXECUTION_state.json"


def now():
    return datetime.now(timezone.utc).isoformat()



def load(path):

    try:
        with open(path, "r") as f:
            return json.load(f)

    except:
        return {}



def save(path, data):

    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    with open(path, "w") as f:
        json.dump(
            data,
            f,
            indent=4
        )



def evaluate_execution():


    risk = load(
        "data/live/RISK_state.json"
    )


    r = risk.get(
        "state",
        {}
    )


    risk_status = r.get(
        "risk_status",
        "BLOCKED"
    )


    direction = r.get(
        "direction",
        "NONE"
    )


    entry = r.get(
        "entry",
        None
    )


    stop_loss = r.get(
        "stop_loss",
        None
    )


    take_profit = r.get(
        "take_profit",
        None
    )



    execution_status = "BLOCKED"

    order_instruction = "NO_ORDER"



    if risk_status == "APPROVED":


        execution_status = "READY"


        if direction == "LONG":

            order_instruction = "BUY"


        elif direction == "SHORT":

            order_instruction = "SELL"



    return {


        "symbol":"BTCUSDT",

        "execution_status":execution_status,

        "order_instruction":order_instruction,

        "risk_status":risk_status,

        "direction":direction,

        "entry":entry,

        "stop_loss":stop_loss,

        "take_profit":take_profit

    }



def run():

    print("==============================")
    print("GSIS EXECUTION ENGINE v3.0")
    print("==============================")


    while True:


        result = evaluate_execution()


        state = {


            "engine":ENGINE,

            "status":"ACTIVE",

            "heartbeat":time.time(),

            "timestamp":now(),

            "state":result

        }


        save(
            OUTPUT,
            state
        )


        print("------------------------------")
        print("GSIS EXECUTION STATE")
        print(state)


        time.sleep(30)



if __name__=="__main__":
    run()
