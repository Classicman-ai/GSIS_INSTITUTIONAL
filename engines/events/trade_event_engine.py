# ==========================================
# GSIS TRADE EVENT ENGINE v2.0
# WITH TRANSPARENCY BRIDGE
# ==========================================

import json
import os

from datetime import datetime, timezone

from engines.transparency.trade_transparency_engine import record_event


STATE_FILE = "data/execution/trade_state.json"
EVENT_FILE = "data/history/trade_events.json"



def load_state():

    if not os.path.exists(STATE_FILE):
        return None

    with open(STATE_FILE, "r") as f:
        return json.load(f)



def load_events():

    if not os.path.exists(EVENT_FILE):
        return []

    with open(EVENT_FILE, "r") as f:
        try:
            return json.load(f)

        except:
            return []



def save_events(events):

    with open(EVENT_FILE, "w") as f:

        json.dump(
            events,
            f,
            indent=4
        )



def event_exists(events, trade_id, event_name):

    for e in events:

        if (
            e.get("trade_id") == trade_id
            and e.get("event") == event_name
        ):
            return True

    return False



def create_event(name, value):

    events = load_events()

    state = load_state()


    if state is None:
        return



    trade_id = state.get("trade_id")


    if trade_id is None:
        return



    event = {

        "trade_id": trade_id,

        "symbol":
        state.get("symbol"),

        "event":
        name,

        "value":
        value,

        "timestamp":
        datetime.now(timezone.utc)
        .isoformat()

    }



    # Duplicate protection

    if event_exists(
        events,
        trade_id,
        name
    ):

        return



    # Save historical event

    events.append(event)

    save_events(events)



    # ==================================
    # TRANSPARENCY ENGINE BRIDGE
    # ==================================

    transparency_event = {

        "trade_id":
        event["trade_id"],

        "symbol":
        event["symbol"],

        "event":
        event["event"],

        "value":
        event["value"]

    }


    transparency_result = record_event(
        transparency_event
    )


    print("==============================")
    print("GSIS EVENT RECORDED")
    print(event)

    print("TRANSPARENCY STATUS")
    print(transparency_result)





def run():

    print("==============================")
    print("GSIS TRADE EVENT ENGINE v2.0")
    print("==============================")


    state = load_state()


    if state is None:

        print("NO ACTIVE TRADE")

        return



    # TP EVENTS

    if state.get("tp1") == "HIT":

        create_event(
            "TP1_HIT",
            "PROFIT_SECURED"
        )



    if state.get("tp2") == "HIT":

        create_event(
            "TP2_HIT",
            "TARGET_REACHED"
        )



    if state.get("tp3") == "HIT":

        create_event(
            "TP3_HIT",
            "TARGET_REACHED"
        )



    if state.get("tp4") == "HIT":

        create_event(
            "TP4_HIT",
            "TRADE_COMPLETED"
        )



    # BREAK EVEN PROTECTION

    if state.get("break_even") == True:

        create_event(
            "STOP_MOVED_BREAK_EVEN",
            "STOP_PROTECTED"
        )



    # FINAL COMPLETION EVENT

    if state.get("status") == "COMPLETED":

        create_event(
            "TRADE_COMPLETED",
            "SUCCESS"
        )




if __name__ == "__main__":

    run()
