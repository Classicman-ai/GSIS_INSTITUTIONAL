import os
import json
import time
from datetime import datetime, timezone


ENGINE = "GSIS_ALERT_ENGINE_v1.0"

STATE_FILE = "data/live/alert_state.json"


def now():
    return datetime.now(timezone.utc).isoformat()


def load_report():

    try:
        with open(
            "data/live/REPORT_state.json",
            "r"
        ) as f:
            return json.load(f)

    except:

        return {}



def create_alert():

    report = load_report()

    state = report.get(
        "state",
        {}
    )


    alerts = []


    if state.get("risk_status") == "BLOCKED":

        alerts.append(
            "TRADE BLOCKED BY RISK ENGINE"
        )


    if state.get("decision") == "WAIT":

        alerts.append(
            "WAITING FOR MARKET CONFIRMATION"
        )


    if state.get("execution_status") == "BLOCKED":

        alerts.append(
            "EXECUTION LOCKED"
        )


    return {

        "symbol":
        state.get(
            "symbol",
            "BTCUSDT"
        ),

        "alerts":
        alerts,

        "severity":
        "NORMAL"
        if len(alerts) < 3
        else "WARNING"

    }



def save_state():

    os.makedirs(
        "data/live",
        exist_ok=True
    )


    payload = {

        "engine":
        ENGINE,

        "status":
        "ACTIVE",

        "heartbeat":
        time.time(),

        "timestamp":
        now(),

        "state":
        create_alert()

    }


    with open(
        STATE_FILE,
        "w"
    ) as f:

        json.dump(
            payload,
            f,
            indent=4
        )


    return payload



def run():

    print("==============================")
    print("GSIS ALERT ENGINE v1.0")
    print("==============================")


    while True:

        state = save_state()

        print("------------------------------")
        print("GSIS ALERT STATE")
        print(state)

        time.sleep(30)



if __name__ == "__main__":
    run()
