# ==========================================
# GSIS EXECUTION EVENT BRIDGE v1.0
# EXECUTION -> TRANSPARENCY LEDGER
# ==========================================

import json
import os

from datetime import datetime, timezone


STATE_FILE = "data/execution/trade_state.json"
EVENT_FILE = "data/history/trade_events.json"


print("==============================")
print("GSIS EXECUTION EVENT BRIDGE v1.0")
print("==============================")


def load_json(path):

    if not os.path.exists(path):
        return {}

    try:

        with open(path,"r") as f:
            return json.load(f)

    except:

        return {}



def save_json(path,data):

    with open(path,"w") as f:
        json.dump(
            data,
            f,
            indent=4
        )



def load_events():

    data = load_json(
        EVENT_FILE
    )

    if not isinstance(data,list):

        return []

    return data



def event_exists(trade_id,event):

    events = load_events()


    for e in events:

        if (
            e.get("trade_id")==trade_id
            and e.get("event")==event
        ):

            return True


    return False



def create_event(
    trade_id,
    symbol,
    event,
    value
):

    if event_exists(
        trade_id,
        event
    ):

        return



    events = load_events()


    record = {

        "trade_id":trade_id,

        "symbol":symbol,

        "event":event,

        "value":value,

        "verified":True,

        "timestamp":
        datetime.now(timezone.utc).isoformat()

    }


    events.append(record)


    save_json(
        EVENT_FILE,
        events
    )


    print(record)



def run():


    state = load_json(
        STATE_FILE
    )


    if not state:

        print("NO EXECUTION STATE")

        return



    trade_id = state.get(
        "trade_id"
    )


    symbol = state.get(
        "symbol"
    )


    if not trade_id:

        print("NO ACTIVE TRADE")

        return



    checks = {


        "tp1":
        "TP1_HIT",


        "tp2":
        "TP2_HIT",


        "tp3":
        "TP3_HIT",


        "tp4":
        "TP4_HIT"

    }



    for key,event in checks.items():

        if state.get(key) == "HIT":

            create_event(

                trade_id,
                symbol,
                event,
                "TARGET_REACHED"

            )



    if state.get("break_even"):

        create_event(

            trade_id,
            symbol,
            "STOP_MOVED_BREAK_EVEN",
            "STOP_PROTECTED"

        )



    if state.get("status") == "COMPLETED":

        create_event(

            trade_id,
            symbol,
            "TRADE_COMPLETED",
            "SUCCESS"

        )



if __name__=="__main__":

    run()
