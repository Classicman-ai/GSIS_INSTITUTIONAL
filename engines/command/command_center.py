import time
import json
import os
from datetime import datetime, timezone


ENGINE = "GSIS_COMMAND_CENTER_v1.0"
SYMBOL = "BTCUSDT"

BASE = "data/live"


def load_json(filename):

    path = os.path.join(BASE, filename)

    try:
        with open(path, "r") as f:
            return json.load(f)

    except Exception:
        return {}



def analyze():

    hmm = load_json("hmm_regime_state.json")
    decision = load_json("decision_state.json")
    confirmation = load_json("confirmation_state.json")
    risk = load_json("risk_state.json")
    execution = load_json("execution_state.json")


    regime = hmm.get(
        "current_regime",
        "UNKNOWN"
    )

    confidence = hmm.get(
        "confidence",
        0
    )


    score = decision.get(
        "score",
        0
    )


    direction = decision.get(
        "direction",
        "NONE"
    )


    confirmation_status = confirmation.get(
        "confirmation",
        "FAILED"
    )


    risk_status = risk.get(
        "risk_status",
        "BLOCKED"
    )


    execution_status = execution.get(
        "execution_status",
        "BLOCKED"
    )


    evidence = []


    if regime != "UNKNOWN":
        evidence.append(
            "HMM_" + regime
        )


    if confirmation_status == "CONFIRMED":
        evidence.append(
            "CONFIRMATION_PASS"
        )


    if risk_status == "APPROVED":
        evidence.append(
            "RISK_APPROVED"
        )


    if execution_status == "READY":

        status = "EXECUTE"


    elif confirmation_status == "PARTIAL":

        status = "WATCH"


    else:

        status = "BLOCKED"



    if direction not in ["BUY", "SELL"]:

        direction = "NONE"



    return {

        "engine": ENGINE,

        "symbol": SYMBOL,

        "regime": regime,

        "hmm_confidence": confidence,

        "institutional_score": score,

        "direction": direction,

        "status": status,

        "confirmation": confirmation_status,

        "risk_status": risk_status,

        "execution_status": execution_status,

        "evidence": evidence,

        "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()

    }



def run():

    print("==============================")
    print(ENGINE)
    print("==============================")


    while True:

        state = analyze()

        print("------------------------------")
        print("GSIS COMMAND CENTER STATE")
        print(state)

        time.sleep(15)



if __name__ == "__main__":

    run()
