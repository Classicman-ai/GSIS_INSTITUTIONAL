# ==========================================
# GSIS BAYESIAN ENGINE ADAPTER v1.0
# ==========================================

import json
import os

from datetime import datetime, timezone



OUTPUT_FILE = "data/engines/bayesian_state.json"



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



def collect_bayesian_output():


    # Temporary connection point
    # Will connect directly to Bayesian Engine next


    state = {


        "direction":
        "BUY",


        "confidence":
        94.6,


        "prediction":
        "BULLISH",


        "learning_state":
        "ACTIVE"


    }


    return state



def run():

    print("==============================")

    print("GSIS BAYESIAN ADAPTER v1.0")

    print("==============================")


    state = collect_bayesian_output()


    save_state(state)


    print("------------------------------")

    print("BAYESIAN STATE PUBLISHED")

    print(state)



if __name__ == "__main__":

    run()
