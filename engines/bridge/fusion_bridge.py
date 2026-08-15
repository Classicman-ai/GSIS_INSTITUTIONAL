import time
import json
import os
from datetime import datetime, timezone


ENGINE = "FUSION"
SYMBOL = "BTCUSDT"

STATE_FILE = "data/live/FUSION_state.json"


def utc_time():
    return datetime.now(timezone.utc).isoformat()


def read_engine(path):

    try:
        with open(path, "r") as f:
            return json.load(f)

    except Exception:
        return {}



def calculate_fusion():


    hmm = read_engine(
        "data/live/HMM_state.json"
    )

    orderflow = read_engine(
        "data/live/ORDERFLOW_state.json"
    )

    structure = read_engine(
        "data/live/STRUCTURE_state.json"
    )


    regime = (
        hmm.get("state", {})
        .get("current_regime",
        "UNKNOWN")
    )


    trend = (
        structure.get("state", {})
        .get("trend",
        "NEUTRAL")
    )


    imbalance = (
        orderflow.get("state", {})
        .get("imbalance",
        "NEUTRAL")
    )


    score = 0
    evidence = []


    if regime == "MARKDOWN":
        score -= 30
        evidence.append(
            "HMM_BEARISH_REGIME"
        )

    if regime == "MARKUP":
        score += 30
        evidence.append(
            "HMM_BULLISH_REGIME"
        )


    if trend == "DOWN":
        score -= 25
        evidence.append(
            "STRUCTURE_SELL"
        )

    if trend == "UP":
        score += 25
        evidence.append(
            "STRUCTURE_BUY"
        )


    if imbalance == "BUY":
        score += 20
        evidence.append(
            "ORDERFLOW_BUY"
        )

    if imbalance == "SELL":
        score -= 20
        evidence.append(
            "ORDERFLOW_SELL"
        )


    if score >= 40:
        bias = "BULLISH"

    elif score <= -40:
        bias = "BEARISH"

    else:
        bias = "NEUTRAL"


    return {

        "symbol": SYMBOL,

        "institutional_score": score,

        "bias": bias,

        "regime": regime,

        "trend": trend,

        "orderflow": imbalance,

        "evidence": evidence

    }



def write_state():

    os.makedirs(
        "data/live",
        exist_ok=True
    )


    payload = {

        "engine": ENGINE,

        "status": "ACTIVE",

        "heartbeat": time.time(),

        "timestamp": utc_time(),

        "state": calculate_fusion()

    }


    with open(
        STATE_FILE,
        "w"
    ) as f:
        json.dump(
            payload,
            f,
            indent=4
        )


    return payload



def run():

    print("==============================")
    print("GSIS FUSION BRIDGE v1.0")
    print("==============================")


    while True:

        state = write_state()

        print("------------------------------")
        print("GSIS FUSION STATE")
        print(state)

        time.sleep(30)



if __name__ == "__main__":
    run()
