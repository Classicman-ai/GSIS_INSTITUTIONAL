# ==========================================
# GSIS RISK ADAPTER v1.0
# ==========================================

import json
import os

from datetime import datetime, timezone


OUTPUT_FILE = "data/engines/risk_state.json"



def save_state(state):

    os.makedirs(
        "data/engines",
        exist_ok=True
    )


    state["timestamp"] = (
        datetime.now(timezone.utc)
        .isoformat()
    )


    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            state,
            f,
            indent=4
        )



def collect_risk_output():


    # Connection point
    # Will later read directly from
    # GSIS Risk Engine


    state = {


        "symbol":
        "BTCUSDT",


        "risk_status":
        "APPROVED",


        "risk_percent":
        0.5,


        "entry":
        63990.00,


        "stop_loss":
        63800.00,


        "tp1":
        64060.00,


        "tp2":
        64150.00,


        "tp3":
        64250.00,


        "tp4":
        64400.00,


        "risk_reward":
        3.0


    }


    return state



def run():

    print("==============================")

    print("GSIS RISK ADAPTER v1.0")

    print("==============================")


    state = collect_risk_output()


    save_state(state)


    print("------------------------------")

    print("RISK STATE PUBLISHED")

    print(state)



if __name__ == "__main__":

    run()
