import os
import json
import time
from datetime import datetime, timezone

ENGINE = "DECISION"
STATE_FILE = "data/live/DECISION_state.json"
FUSION_FILE = "data/live/FUSION_state.json"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def read_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def make_decision():

    fusion = read_json(FUSION_FILE)

    state = fusion.get("state", {})

    score = state.get("institutional_score", 0)
    bias = state.get("bias", "NEUTRAL")

    decision = "WAIT"
    permission = "BLOCKED"
    confidence = abs(score)

    if bias == "BULLISH" and score >= 40:
        decision = "BUY"
        permission = "APPROVED"

    elif bias == "BEARISH" and score <= -40:
        decision = "SELL"
        permission = "APPROVED"

    return {
        "symbol": state.get("symbol", "BTCUSDT"),
        "decision": decision,
        "permission": permission,
        "bias": bias,
        "score": score,
        "confidence": confidence
    }


def save_state():

    os.makedirs("data/live", exist_ok=True)

    payload = {
        "engine": ENGINE,
        "status": "ACTIVE",
        "heartbeat": time.time(),
        "timestamp": utc_now(),
        "state": make_decision()
    }

    with open(STATE_FILE, "w") as f:
        json.dump(payload, f, indent=4)

    return payload


def run():

    print("==============================")
    print("GSIS DECISION BRIDGE v1.0")
    print("==============================")

    while True:

        output = save_state()

        print("------------------------------")
        print("GSIS DECISION STATE")
        print(output)

        time.sleep(30)


if __name__ == "__main__":
    run()
