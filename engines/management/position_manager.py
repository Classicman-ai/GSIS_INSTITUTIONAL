import os
import json
from datetime import datetime, timezone


BASE_DIR = os.path.expanduser("~/GSIS")

ACTIVE_TRADE_FILE = os.path.join(
    BASE_DIR,
    "data/execution/active_trade.json"
)

TRADE_STATE_FILE = os.path.join(
    BASE_DIR,
    "data/execution/trade_state.json"
)

POSITION_STATE_FILE = os.path.join(
    BASE_DIR,
    "data/execution/position_management.json"
)


def load_json(path):
    if not os.path.exists(path):
        return None

    with open(path, "r") as file:
        return json.load(file)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as file:
        json.dump(data, file, indent=4)


def manage_position():

    print("==============================")
    print("GSIS POSITION MANAGEMENT ENGINE v1.0")
    print("==============================")

    trade = load_json(ACTIVE_TRADE_FILE)

    if not trade:

        print("------------------------------")
        print("NO ACTIVE TRADE")
        return


    trade_id = trade.get("trade_id")
    symbol = trade.get("symbol")
    direction = trade.get("direction")


    state = load_json(TRADE_STATE_FILE)


    management = {
        "trade_id": trade_id,
        "symbol": symbol,
        "direction": direction,
        "position_status": "ACTIVE",
        "tp1": "MONITORED",
        "tp2": "MONITORED",
        "tp3": "MONITORED",
        "tp4": "MONITORED",
        "stop_loss": "PROTECTED",
        "break_even": True,
        "trailing_stop": "READY",
        "last_update": datetime.now(timezone.utc).isoformat()
    }


    if state:

        if state.get("status") == "COMPLETED":
            management["position_status"] = "COMPLETED"


    save_json(
        POSITION_STATE_FILE,
        management
    )


    print("------------------------------")
    print("POSITION MANAGEMENT ACTIVE")

    print(management)


if __name__ == "__main__":
    manage_position()
