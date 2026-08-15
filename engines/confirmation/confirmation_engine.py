import os
import json
import time
from datetime import datetime, timezone


ENGINE = "GSIS_CONFIRMATION_ENGINE_v2.1"

OUTPUT = "data/live/CONFIRMATION_state.json"


def now():
    return datetime.now(timezone.utc).isoformat()


def load(path):

    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}



def save(path,data):

    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    with open(path,"w") as f:
        json.dump(
            data,
            f,
            indent=4
        )



def analyze():

    score = 0
    signals = []


    # STRUCTURE ENGINE

    structure = load(
        "data/live/STRUCTURE_state.json"
    )


    s = structure.get(
        "state",
        {}
    )


    trend = s.get(
        "trend",
        "NEUTRAL"
    )


    if s.get("BOS"):

        score += 25

        signals.append(
            "BREAK_OF_STRUCTURE"
        )


    if s.get("CHOCH"):

        score += 25

        signals.append(
            "CHANGE_OF_CHARACTER"
        )


    if s.get("fair_value_gap") != "NONE":

        score += 15

        signals.append(
            "FAIR_VALUE_GAP"
        )


    if s.get("order_block") != "NONE":

        score += 15

        signals.append(
            "ORDER_BLOCK"
        )



    # ORDERFLOW ENGINE

    orderflow = load(
        "data/live/ORDERFLOW_state.json"
    )


    o = orderflow.get(
        "state",
        {}
    )


    imbalance = o.get(
        "imbalance",
        "NEUTRAL"
    )


    if imbalance in [
        "SELL",
        "BEARISH"
    ]:

        score += 20

        signals.append(
            "BEARISH_ORDERFLOW"
        )


    elif imbalance in [
        "BUY",
        "BULLISH"
    ]:

        score += 20

        signals.append(
            "BULLISH_ORDERFLOW"
        )



    # LIQUIDITY ENGINE

    liquidity = load(
        "data/live/liquidity_state.json"
    )


    liquidity_event = liquidity.get(
        "liquidity_state",
        "NONE"
    )


    if "SWEEP" in liquidity_event:

        score += 20

        signals.append(
            "LIQUIDITY_SWEEP"
        )



    confirmed = False


    if score >= 60:

        confirmed = True



    return {

        "confirmed": confirmed,

        "confirmation_score": score,

        "trend": trend,

        "signals": signals

    }



def run():

    print("==============================")
    print("GSIS CONFIRMATION ENGINE v2.1")
    print("==============================")


    while True:


        result = analyze()


        state = {

            "engine":ENGINE,

            "status":"ACTIVE",

            "heartbeat":time.time(),

            "timestamp":now(),

            "state":result

        }


        save(
            OUTPUT,
            state
        )


        print("------------------------------")
        print("GSIS CONFIRMATION STATE")
        print(state)


        time.sleep(30)



if __name__=="__main__":
    run()
