import os
import json
import time
from datetime import datetime, timezone


ENGINE = "GSIS_RISK_ENGINE_v3.0"

OUTPUT = "data/live/RISK_state.json"


def now():
    return datetime.now(timezone.utc).isoformat()


def load(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}


def save(path, data):

    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    with open(path, "w") as f:
        json.dump(
            data,
            f,
            indent=4
        )


def calculate_risk():

    qualification = load(
        "data/live/QUALIFICATION_state.json"
    )

    confirmation = load(
        "data/live/CONFIRMATION_state.json"
    )

    market = load(
        "data/live/market_context.json"
    )


    q = qualification.get(
        "state",
        {}
    )

    c = confirmation.get(
        "state",
        {}
    )


    grade = q.get(
        "qualification",
        "NO_TRADE"
    )

    direction = q.get(
        "direction",
        "NONE"
    )

    score = q.get(
        "qualification_score",
        0
    )

    confirmed = c.get(
        "confirmed",
        False
    )


    risk_status = "BLOCKED"

    entry = None
    stop_loss = None
    take_profit = None

    risk_reward = 0


    if grade in ["A_SETUP", "B_SETUP"] and confirmed:

        risk_status = "APPROVED"

        price = market.get(
            "price",
            None
        )

        entry = price


        if price and direction == "SHORT":

            stop_loss = round(
                price * 1.005,
                2
            )

            take_profit = round(
                price * 0.985,
                2
            )

            risk_reward = 3


        elif price and direction == "LONG":

            stop_loss = round(
                price * 0.995,
                2
            )

            take_profit = round(
                price * 1.015,
                2
            )

            risk_reward = 3



    return {

        "symbol": "BTCUSDT",

        "risk_status": risk_status,

        "direction": direction,

        "qualification": grade,

        "qualification_score": score,

        "confirmation": confirmed,

        "risk_percent": 1.0,

        "risk_reward": risk_reward,

        "entry": entry,

        "stop_loss": stop_loss,

        "take_profit": take_profit

    }



def run():

    print("==============================")
    print("GSIS RISK ENGINE v3.0")
    print("==============================")


    while True:

        result = calculate_risk()


        state = {

            "engine": ENGINE,

            "status": "ACTIVE",

            "heartbeat": time.time(),

            "timestamp": now(),

            "state": result

        }


        save(
            OUTPUT,
            state
        )


        print("------------------------------")
        print("GSIS RISK STATE")
        print(state)


        time.sleep(30)



if __name__ == "__main__":
    run()
