import json
import os
import time


BUFFER_FILE = "data/live/market_buffer.json"


def update_market(data):
    os.makedirs("data/live", exist_ok=True)

    payload = {
        "timestamp": time.time(),
        "market": data
    }

    with open(BUFFER_FILE, "w") as f:
        json.dump(payload, f, indent=4)


def read_market():
    if not os.path.exists(BUFFER_FILE):
        return None

    with open(BUFFER_FILE, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    print("GSIS LIVE MARKET BUFFER READY")
