import json
import os

from engines.transparency.event_validator import (
    validate_event,
    timestamp
)


EVENT_FILE = "data/transparency/event_ledger.json"
JOURNAL_FILE = "data/transparency/trade_journal.json"
STATE_FILE = "data/transparency/transparency_state.json"


def load_file(path):

    if not os.path.exists(path):
        return []

    with open(path, "r") as f:
        try:
            return json.load(f)
        except:
            return []


def save_file(path, data):

    with open(path, "w") as f:
        json.dump(
            data,
            f,
            indent=4
        )


def record_event(event):

    if not validate_event(event):
        return {
            "status":"REJECTED",
            "reason":"INVALID_EVENT"
        }


    events = load_file(EVENT_FILE)

    event["verified"] = True
    event["timestamp"] = timestamp()

    events.append(event)

    save_file(
        EVENT_FILE,
        events
    )


    update_state(event)


    return {
        "status":"RECORDED",
        "event":event["event"]
    }



def create_trade_report(trade):

    journal = load_file(JOURNAL_FILE)

    journal.append(trade)

    save_file(
        JOURNAL_FILE,
        journal
    )



def update_state(event):

    state = {

        "engine":
        "GSIS_TRANSPARENCY_ENGINE_v1.0",

        "status":
        "ONLINE",

        "last_trade":
        event.get("trade_id"),

        "last_event":
        event.get("event"),

        "event_verified":
        True,

        "timestamp":
        timestamp()
    }


    save_file(
        STATE_FILE,
        state
    )



if __name__ == "__main__":

    print("==============================")
    print("GSIS TRANSPARENCY ENGINE v1.0")
    print("==============================")

    test_event = {

        "trade_id":
        "GSIS-TEST-001",

        "symbol":
        "BTCUSDT",

        "event":
        "TRADE_OPENED"
    }


    print(
        record_event(test_event)
    )
