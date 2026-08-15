# ==========================================
# GSIS TRADE LIFECYCLE MANAGER v1.0
# ==========================================

import json
import os

from datetime import datetime, timezone


TRADE_FILE = "data/execution/active_trade.json"
STATE_FILE = "data/execution/trade_state.json"



def load_trade():

    if not os.path.exists(TRADE_FILE):
        return None

    with open(TRADE_FILE,"r") as f:
        return json.load(f)



def save_state(state):

    os.makedirs(
        "data/execution",
        exist_ok=True
    )

    with open(
        STATE_FILE,
        "w"
    ) as f:

        json.dump(
            state,
            f,
            indent=4
        )



def manage_trade():


    trade = load_trade()


    if trade is None:

        return {
            "status":"NO_ACTIVE_TRADE"
        }



    state = {


        "trade_id":
        trade["trade_id"],


        "symbol":
        trade["symbol"],


        "direction":
        trade["direction"],


        "status":
        "MONITORING",


        "tp1":
        "WAITING",


        "tp2":
        "WAITING",


        "tp3":
        "WAITING",


        "tp4":
        "WAITING",


        "stop_loss":
        "ACTIVE",


        "break_even":
        False,


        "last_update":
        datetime.now(timezone.utc)
        .isoformat()

    }


    save_state(state)


    return state



def run():

    print("==============================")

    print("GSIS TRADE LIFECYCLE MANAGER v1.0")

    print("==============================")


    result = manage_trade()


    print("------------------------------")

    print(result)



if __name__ == "__main__":

    run()
