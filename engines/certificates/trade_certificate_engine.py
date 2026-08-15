# ==========================================
# GSIS TRADE CERTIFICATE ENGINE v2.0
# TRANSPARENT VERIFICATION PROTOCOL
# ==========================================

import json
import os

from datetime import datetime, timezone


TRADE_STATE = "data/execution/trade_state.json"
EVENT_FILE = "data/history/trade_events.json"
DELIVERY_FILE = "data/transparency/telegram_delivery.json"

OUTPUT_DIR = "data/certificates"


def load_json(path, default):

    if not os.path.exists(path):
        return default

    try:
        with open(path, "r") as f:
            return json.load(f)

    except Exception:
        return default



def save_certificate(trade_id, certificate):

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    path = f"{OUTPUT_DIR}/{trade_id}.json"

    with open(path, "w") as f:

        json.dump(
            certificate,
            f,
            indent=4
        )



def run():

    print("==============================")
    print("GSIS TRADE CERTIFICATE ENGINE v2.0")
    print("TRANSPARENT VERIFICATION PROTOCOL")
    print("==============================")


    state = load_json(
        TRADE_STATE,
        {}
    )

    events = load_json(
        EVENT_FILE,
        []
    )

    deliveries = load_json(
        DELIVERY_FILE,
        []
    )


    trade_id = state.get(
        "trade_id"
    )


    if not trade_id:

        print("NO TRADE FOUND")
        return



    symbol = state.get(
        "symbol"
    )

    direction = state.get(
        "direction"
    )



    required_events = [
        "TP1_HIT",
        "TP2_HIT",
        "TP3_HIT",
        "TP4_HIT",
        "STOP_MOVED_BREAK_EVEN",
        "TRADE_COMPLETED"
    ]


    event_status = {}

    for event in required_events:

        found = False

        for e in events:

            if (
                e.get("trade_id") == trade_id
                and e.get("event") == event
            ):
                found = True


        event_status[event] = (
            "VERIFIED"
            if found
            else "MISSING"
        )



    delivery_count = 0

    delivered_events = []


    for d in deliveries:

        if (
            d.get("trade_id") == trade_id
            and d.get("telegram_status") == "DELIVERED"
        ):

            delivery_count += 1

            delivered_events.append(
                d.get("event")
            )



    all_events_verified = all(
        value == "VERIFIED"
        for value in event_status.values()
    )


    delivery_verified = (
        delivery_count >= 6
    )



    if (
        all_events_verified
        and delivery_verified
    ):

        verdict = "SUCCESSFUL"

    else:

        verdict = "INCOMPLETE - DELIVERY FAILURE"



    certificate = {

        "certificate_engine":
        "GSIS_TRADE_CERTIFICATE_ENGINE_v2.0",


        "trade_id":
        trade_id,


        "symbol":
        symbol,


        "direction":
        direction,


        "trade_status":
        state.get(
            "status",
            "UNKNOWN"
        ),


        "event_verification":
        event_status,


        "telegram_delivery":
        {

            "messages_confirmed":
            delivery_count,

            "delivered_events":
            delivered_events,

            "verification":
            (
                "PASSED"
                if delivery_verified
                else "FAILED"
            )

        },


        "final_verdict":
        verdict,


        "generated":
        datetime.now(
            timezone.utc
        ).isoformat()

    }



    save_certificate(
        trade_id,
        certificate
    )


    print(certificate)



if __name__ == "__main__":

    run()
