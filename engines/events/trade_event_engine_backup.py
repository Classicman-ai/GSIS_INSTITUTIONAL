# ==========================================
# GSIS TRADE EVENT ENGINE v1.0
# ==========================================

import json
import os

from datetime import datetime, timezone


STATE_FILE = "data/execution/trade_state.json"
EVENT_FILE = "data/history/trade_events.json"



def load_state():

    if not os.path.exists(STATE_FILE):
        return None

    with open(STATE_FILE,"r") as f:
        return json.load(f)



def load_events():

    if not os.path.exists(EVENT_FILE):
        return []

    with open(EVENT_FILE,"r") as f:
        return json.load(f)



def save_events(events):

    with open(EVENT_FILE,"w") as f:
        json.dump(
            events,
            f,
            indent=4
        )



def create_event(name, value):

    events = load_events()

    state = load_state()


    if state is None:
        return



    event = {

        "trade_id":
        state["trade_id"],

        "symbol":
        state["symbol"],

        "event":
        name,

        "value":
        value,

        "timestamp":
        datetime.now(timezone.utc)
        .isoformat()

    }


    # prevent duplicate events

    exists = False

    for e in events:

        if (
            e["trade_id"] == event["trade_id"]
            and e["event"] == event["event"]
        ):
            exists = True



    if not exists:

        events.append(event)

        save_events(events)

        print("EVENT RECORDED")

        print(event)



def run():

    print("==============================")
    print("GSIS TRADE EVENT ENGINE v1.0")
    print("==============================")


    state = load_state()


    if state is None:

        print("NO ACTIVE TRADE")
        return



    if state["tp1"] == "HIT":

        create_event(
            "TP1_HIT",
            "PROFIT_SECURED"
        )


    if state["tp2"] == "HIT":

        create_event(
            "TP2_HIT",
            "TARGET_REACHED"
        )


    if state["tp3"] == "HIT":

        create_event(
            "TP3_HIT",
            "TARGET_REACHED"
        )


    if state["tp4"] == "HIT":

        create_event(
            "TP4_HIT",
            "TRADE_COMPLETED"
        )



if __name__ == "__main__":

    run()
