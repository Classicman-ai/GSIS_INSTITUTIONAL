# ==========================================
# GSIS TRADE PROTECTION ENGINE v1.1
# ==========================================

import json
import os
from datetime import datetime, timezone


ACTIVE_TRADE = "data/execution/active_trade.json"

STATE_FILE = "data/protection/protection_state.json"


def load_trade():

    if not os.path.exists(ACTIVE_TRADE):
        return None

    with open(ACTIVE_TRADE, "r") as f:
        return json.load(f)



def save_state(data):

    os.makedirs(
        "data/protection",
        exist_ok=True
    )

    with open(
        STATE_FILE,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )



def main():

    print("==============================")
    print("GSIS TRADE PROTECTION ENGINE v1.1")
    print("==============================")


    trade = load_trade()


    timestamp = datetime.now(
        timezone.utc
    ).isoformat()


    if trade:

        state = {

            "protection": "ACTIVE",

            "new_entries": "BLOCKED",

            "reason":
            "ACTIVE_TRADE_EXISTS",

            "active_trade":
            trade.get(
                "trade_id"
            ),

            "symbol":
            trade.get(
                "symbol"
            ),

            "direction":
            trade.get(
                "direction"
            ),

            "timestamp":
            timestamp
        }


        print("------------------------------")
        print("TRADE PROTECTION ACTIVE")
        print(state)



    else:

        state = {

            "protection": "READY",

            "new_entries": "ALLOWED",

            "reason":
            "NO_ACTIVE_TRADE",

            "active_trade":
            None,

            "timestamp":
            timestamp
        }


        print("------------------------------")
        print("ENTRY AVAILABLE")
        print(state)



    save_state(state)



if __name__ == "__main__":

    main()
