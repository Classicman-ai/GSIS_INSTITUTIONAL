# ==========================================
# GSIS REGIME SCORE ADAPTER v1.0
# ==========================================

import json
import os

from datetime import datetime, timezone


OUTPUT_FILE = "data/engines/regime_state.json"



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



def collect_regime_output():


    # Connection point
    # Will later read directly from
    # GSIS REGIME SCORE ENGINE


    state = {

        "regime":
        "MARKUP",


        "bias":
        "BULLISH",


        "score":
        85,


        "confidence":
        90

    }


    return state



def run():

    print("==============================")

    print("GSIS REGIME ADAPTER v1.0")

    print("==============================")


    state = collect_regime_output()


    save_state(state)


    print("------------------------------")

    print("REGIME STATE PUBLISHED")

    print(state)



if __name__ == "__main__":

    run()
