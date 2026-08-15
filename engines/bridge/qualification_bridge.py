import os
import json
import time
from datetime import datetime, timezone

ENGINE = "QUALIFICATION"
STATE_FILE = "data/live/QUALIFICATION_state.json"

CONFIRMATION_FILE = "data/live/CONFIRMATION_state.json"
FUSION_FILE = "data/live/FUSION_state.json"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def read_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def qualify():

    confirmation = read_json(CONFIRMATION_FILE).get("state", {})
    fusion = read_json(FUSION_FILE).get("state", {})

    confirmed = confirmation.get("confirmed", False)
    score = fusion.get("institutional_score", 0)

    qualification = "NO_TRADE"
    quality = 0

    if confirmed:
        quality = min(abs(score), 100)

        if quality >= 80:
            qualification = "A+"

        elif quality >= 70:
            qualification = "A"

        elif quality >= 60:
            qualification = "B"

        else:
            qualification = "REJECT"

    return {
        "symbol": confirmation.get("symbol", "BTCUSDT"),
        "confirmed": confirmed,
        "institutional_score": score,
        "quality": quality,
        "qualification": qualification
    }


def save_state():

    os.makedirs("data/live", exist_ok=True)

    payload = {
        "engine": ENGINE,
        "status": "ACTIVE",
        "heartbeat": time.time(),
        "timestamp": utc_now(),
        "state": qualify()
    }

    with open(STATE_FILE, "w") as f:
        json.dump(payload, f, indent=4)

    return payload


def run():

    print("==============================")
    print("GSIS QUALIFICATION BRIDGE v1.0")
    print("==============================")

    while True:

        state = save_state()

        print("------------------------------")
        print("GSIS QUALIFICATION STATE")
        print(state)

        time.sleep(30)


if __name__ == "__main__":
    run()
