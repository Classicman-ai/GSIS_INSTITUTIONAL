# ==========================================
# GSIS CONFIRMATION ADAPTER v1.0
# ==========================================

import json
import os

from datetime import datetime, timezone


OUTPUT_FILE = "data/engines/confirmation_state.json"



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



def collect_confirmation_output():


    # Connection point
    # Will later read directly from
    # GSIS CONFIRMATION ENGINE


    state = {

        "confirmed":
        True,


        "confirmation_score":
        95,


        "trend":
        "BULLISH",


        "signals":
        [
            "BOS_CONFIRMED",
            "LIQUIDITY_SWEEP",
            "STRUCTURE_ALIGNED"
        ]

    }


    return state



def run():

    print("==============================")

    print("GSIS CONFIRMATION ADAPTER v1.0")

    print("==============================")


    state = collect_confirmation_output()


    save_state(state)


    print("------------------------------")

    print("CONFIRMATION STATE PUBLISHED")

    print(state)



if __name__ == "__main__":

    run()
