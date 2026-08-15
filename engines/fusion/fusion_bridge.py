# ==========================================
# GSIS ENGINE FUSION BRIDGE v1.1
# LIVE ENGINE READER
# ==========================================

import json
import os
from datetime import datetime, timezone


AUTHORITY_STATE = "data/authority/authority_state.json"


ENGINE_PATHS = {

    "regime":
    "data/engines/regime_state.json",

    "bayesian":
    "data/engines/bayesian_state.json",

    "confirmation":
    "data/engines/confirmation_state.json",

    "qualification":
    "data/engines/qualification_state.json",

    "risk":
    "data/engines/risk_state.json"

}



def read_state(path):

    if not os.path.exists(path):

        return {}

    with open(path,"r") as f:

        return json.load(f)



def write_authority(state):

    os.makedirs(
        "data/authority",
        exist_ok=True
    )


    state["timestamp"] = (
        datetime.now(timezone.utc)
        .isoformat()
    )


    with open(
        AUTHORITY_STATE,
        "w"
    ) as f:

        json.dump(
            state,
            f,
            indent=4
        )



def build_fusion_state():


    regime = read_state(
        ENGINE_PATHS["regime"]
    )

    bayesian = read_state(
        ENGINE_PATHS["bayesian"]
    )

    confirmation = read_state(
        ENGINE_PATHS["confirmation"]
    )

    qualification = read_state(
        ENGINE_PATHS["qualification"]
    )

    risk = read_state(
        ENGINE_PATHS["risk"]
    )



    state = {


        "symbol":

        qualification.get(
            "symbol",
            "BTCUSDT"
        ),



        "direction":

        qualification.get(
            "direction",
            "NONE"
        ),



        "confidence":

        bayesian.get(
            "confidence",
            0
        ),



        "setup":

        qualification.get(
            "qualification",
            "NONE"
        ),



        "timeframe":

        "M15",



        "regime":

        regime.get(
            "bias",
            "UNKNOWN"
        ),



        "bayesian":

        bayesian.get(
            "direction",
            "UNKNOWN"
        ),



        "confirmation":

        confirmation.get(
            "confirmed",
            False
        ),



        "risk_status":

        risk.get(
            "risk_status",
            "UNKNOWN"
        )


    }


    return state



def run():

    print("==============================")
    print("GSIS ENGINE FUSION BRIDGE v1.1")
    print("==============================")


    state = build_fusion_state()


    write_authority(state)


    print("------------------------------")
    print("LIVE AUTHORITY STATE UPDATED")
    print(state)



if __name__ == "__main__":

    run()
