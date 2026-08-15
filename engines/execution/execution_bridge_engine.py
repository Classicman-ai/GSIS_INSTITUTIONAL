import json
import time
import os


BASE = "data/live"


def load_json(filename):

    try:
        with open(
            os.path.join(BASE, filename),
            "r"
        ) as f:
            return json.load(f)

    except Exception:
        return {}



def execution_check():

    risk = load_json(
        "risk_state.json"
    )


    symbol = risk.get(
        "symbol",
        "BTCUSDT"
    )


    status = risk.get(
        "risk_status",
        "BLOCKED"
    )


    direction = risk.get(
        "direction",
        "NONE"
    )


    order = "NO_ORDER"


    execution_status = "BLOCKED"



    if status == "APPROVED":

        execution_status = "READY"


        if direction == "BUY":

            order = "OPEN_LONG"


        elif direction == "SELL":

            order = "OPEN_SHORT"



    state = {

        "engine":
        "GSIS_EXECUTION_BRIDGE_ENGINE_v3.0",


        "symbol":
        symbol,


        "execution_status":
        execution_status,


        "order_instruction":
        order,


        "direction":
        direction,


        "risk_status":
        status,


        "timestamp":
        time.time()

    }


    return state



def run():

    print("==============================")
    print("GSIS EXECUTION BRIDGE ENGINE v3.0")
    print("==============================")


    while True:

        state = execution_check()


        with open(
            f"{BASE}/execution_state.json",
            "w"
        ) as f:

            json.dump(
                state,
                f,
                indent=4
            )


        print("------------------------------")
        print("GSIS EXECUTION STATE")
        print(state)


        time.sleep(15)



if __name__ == "__main__":

    run()
