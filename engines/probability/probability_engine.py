import os
import json
import time
from datetime import datetime, timezone


ENGINE = "GSIS_PROBABILITY_ENGINE_v1.0"

OUTPUT = "data/live/probability_state.json"


def timestamp():
    return datetime.now(timezone.utc).isoformat()



def load_state(path):

    try:
        with open(path, "r") as f:
            return json.load(f)

    except:
        return {}



def clamp(value):

    if value < 0:
        return 0

    if value > 100:
        return 100

    return value



def calculate_probability():

    fusion = load_state(
        "data/live/FUSION_state.json"
    )

    orderflow = load_state(
        "data/live/ORDERFLOW_state.json"
    )

    decision = load_state(
        "data/live/DECISION_state.json"
    )


    score = 0
    evidence = []


    fusion_state = fusion.get(
        "state",
        {}
    )


    regime = fusion_state.get(
        "regime",
        "UNKNOWN"
    )


    institutional_score = fusion_state.get(
        "institutional_score",
        0
    )


    score += institutional_score


    if regime == "MARKUP":

        score += 25
        evidence.append(
            "BULLISH_REGIME"
        )


    elif regime == "MARKDOWN":

        score -= 25
        evidence.append(
            "BEARISH_REGIME"
        )


    order_state = orderflow.get(
        "state",
        {}
    )


    imbalance = order_state.get(
        "imbalance",
        "NEUTRAL"
    )


    if imbalance == "BUYING":

        score += 15
        evidence.append(
            "BUY_PRESSURE"
        )


    elif imbalance == "SELLING":

        score -= 15
        evidence.append(
            "SELL_PRESSURE"
        )


    decision_state = decision.get(
        "state",
        {}
    )


    decision_value = decision_state.get(
        "decision",
        "WAIT"
    )


    if decision_value == "BUY":

        score += 10
        evidence.append(
            "DECISION_BUY"
        )


    elif decision_value == "SELL":

        score -= 10
        evidence.append(
            "DECISION_SELL"
        )


    bullish_raw = 50 + score

    bearish_raw = 50 - score


    bullish = clamp(
        bullish_raw
    )

    bearish = clamp(
        bearish_raw
    )


    neutral = clamp(
        100 - abs(score)
    )


    total = bullish + bearish + neutral


    if total == 0:

        total = 1


    bullish = round(
        bullish / total * 100,
        2
    )

    bearish = round(
        bearish / total * 100,
        2
    )

    neutral = round(
        neutral / total * 100,
        2
    )


    if bearish > bullish:

        market_state = "BEARISH"

    elif bullish > bearish:

        market_state = "BULLISH"

    else:

        market_state = "NEUTRAL"



    return {

        "symbol": "BTCUSDT",

        "market_state": market_state,

        "bullish_probability": bullish,

        "bearish_probability": bearish,

        "neutral_probability": neutral,

        "confidence": max(
            bullish,
            bearish,
            neutral
        ),

        "score": score,

        "evidence": evidence

    }



def save_state():

    os.makedirs(
        "data/live",
        exist_ok=True
    )


    payload = {

        "engine": ENGINE,

        "status": "ACTIVE",

        "heartbeat": time.time(),

        "timestamp": timestamp(),

        "state": calculate_probability()

    }


    with open(
        OUTPUT,
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
    print("GSIS PROBABILITY ENGINE v1.0")
    print("==============================")


    while True:

        state = save_state()

        print("------------------------------")
        print("GSIS PROBABILITY STATE")

        print(state)

        time.sleep(30)



if __name__ == "__main__":
    run()
