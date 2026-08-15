# ==========================================
# GSIS PRICE MONITOR ENGINE v1.1
# LIVE MODE
# ==========================================

import json
import os
from datetime import datetime, timezone


TRADE_FILE = "data/execution/active_trade.json"
STATE_FILE = "data/execution/trade_state.json"
PRICE_FILE = "data/market/live_price.json"


def load_json(file):

    if not os.path.exists(file):
        return None

    with open(file, "r") as f:
        return json.load(f)



def save_state(state):

    with open(
        STATE_FILE,
        "w"
    ) as f:

        json.dump(
            state,
            f,
            indent=4
        )



def monitor():

    trade = load_json(TRADE_FILE)
    state = load_json(STATE_FILE)
    market = load_json(PRICE_FILE)


    if trade is None or market is None:

        print("NO DATA AVAILABLE")
        return



    price = market["price"]

    direction = trade["direction"]


    print("==============================")
    print("GSIS PRICE MONITOR ENGINE v1.1")
    print("==============================")

    print("------------------------------")
    print("LIVE PRICE:", price)



    if direction == "BUY":


        # TP1

        if price >= 64060:

            if state["tp1"] != "HIT":

                state["tp1"] = "HIT"
                state["break_even"] = True
                state["stop_loss"] = "BREAK_EVEN"

                print("🎯 TP1 HIT")
                print("STATUS: PROFIT SECURED")
                print("SL MOVED TO BREAK EVEN")



        # TP2

        if price >= 64150:

            if state["tp2"] != "HIT":

                state["tp2"] = "HIT"

                print("🎯 TP2 HIT")



        # TP3

        if price >= 64250:

            if state["tp3"] != "HIT":

                state["tp3"] = "HIT"

                print("🎯 TP3 HIT")



        # TP4

        if price >= 64400:

            if state["tp4"] != "HIT":

                state["tp4"] = "HIT"
                state["status"] = "COMPLETED"

                print("🎯 TP4 HIT")
                print("STATUS: TRADE COMPLETED")



        # Stop Loss

        if price <= 63800:

            state["status"] = "STOPPED"

            print("🛑 STOP LOSS HIT")



    state["last_price"] = price

    state["last_update"] = (
        datetime.now(timezone.utc)
        .isoformat()
    )


    save_state(state)



def run():

    monitor()



if __name__ == "__main__":

    run()
