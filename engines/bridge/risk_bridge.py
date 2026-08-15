import os
import json
import time
from datetime import datetime, timezone


ENGINE = "GSIS_RISK_BRIDGE_v2.0"

STATE_FILE = "data/live/RISK_state.json"
QUALIFICATION_FILE = "data/live/QUALIFICATION_state.json"
FUSION_FILE = "data/live/FUSION_state.json"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def load_json(path):

    try:
        with open(path, "r") as file:
            return json.load(file)

    except Exception:
        return {}



def get_market_context():

    fusion = load_json(FUSION_FILE)

    state = fusion.get("state", {})

    return {

        "regime": state.get("regime", "UNKNOWN"),
        "bias": state.get("bias", "NEUTRAL"),
        "score": state.get("institutional_score", 0)

    }



def calculate_risk():


    qualification_data = load_json(QUALIFICATION_FILE)

    qualification_state = qualification_data.get("state", {})


    market = get_market_context()


    symbol = qualification_state.get(
        "symbol",
        "BTCUSDT"
    )


    qualification = qualification_state.get(
        "qualification",
        "NO_TRADE"
    )


    institutional_score = qualification_state.get(
        "institutional_score",
        market["score"]
    )


    regime = market["regime"]

    bias = market["bias"]


    status = "BLOCKED"

    direction = "NONE"


    entry = None
    stop_loss = None
    take_profit = None


    risk_percent = 1.0
    risk_reward = 0



    # GSIS qualification gate

    if qualification in ["A+", "A", "B"]:


        if institutional_score >= 50:

            direction = "BUY"
            status = "APPROVED"


        elif institutional_score <= -50:

            direction = "SELL"
            status = "APPROVED"



        if status == "APPROVED":

            risk_reward = 3



    return {


        "symbol": symbol,

        "risk_status": status,

        "direction": direction,

        "qualification": qualification,

        "institutional_score": institutional_score,

        "market_regime": regime,

        "market_bias": bias,

        "risk_percent": risk_percent,

        "risk_reward": risk_reward,

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

        "state": calculate_risk()

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
    print("GSIS RISK BRIDGE v2.0")
    print("==============================")


    while True:


        state = save_state()


        print("------------------------------")
        print("GSIS RISK STATE")

        print(state)


        time.sleep(30)




if __name__ == "__main__":

    run()
