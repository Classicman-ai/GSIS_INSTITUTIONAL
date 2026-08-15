import os
import json
import time
from datetime import datetime, timezone

ENGINE = "CONFIRMATION"
STATE_FILE = "data/live/CONFIRMATION_state.json"

DECISION_FILE = "data/live/DECISION_state.json"
FUSION_FILE = "data/live/FUSION_state.json"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def read_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def confirmation_logic():

    decision = read_json(DECISION_FILE).get("state", {})
    fusion = read_json(FUSION_FILE).get("state", {})

    score = fusion.get("institutional_score", 0)
    trade_decision = decision.get("decision", "WAIT")

    confirmed = False
    reason = "INSUFFICIENT_CONFIRMATION"

    if trade_decision == "BUY" and score >= 60:
        confirmed = True
        reason = "BULLISH_CONFIRMED"

    elif trade_decision == "SELL" and score <= -60:
        confirmed = True
        reason = "BEARISH_CONFIRMED"

    return {
        "symbol": decision.get("symbol", "BTCUSDT"),
        "decision": trade_decision,
        "confirmed": confirmed,
        "reason": reason,
        "score": score
    }


def save_state():

    os.makedirs("data/live", exist_ok=True)

    payload = {
        "engine": ENGINE,
        "status": "ACTIVE",
        "heartbeat": time.time(),
        "timestamp": utc_now(),
        "state": confirmation_logic()
    }

    with open(STATE_FILE, "w") as f:
        json.dump(payload, f, indent=4)

    return payload


def run():

    print("==============================")
    print("GSIS CONFIRMATION BRIDGE v1.0")
    print("==============================")

    while True:

        state = save_state()

        print("------------------------------")
        print("GSIS CONFIRMATION STATE")
        print(state)

        time.sleep(30)


if __name__ == "__main__":
    run()
