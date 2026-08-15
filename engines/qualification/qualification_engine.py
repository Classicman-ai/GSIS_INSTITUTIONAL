import os
import json
import time
from datetime import datetime, timezone


ENGINE = "GSIS_QUALIFICATION_ENGINE_v2.0"

OUTPUT = "data/live/QUALIFICATION_state.json"


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



def evaluate():


    score = 0
    conditions = []



    # REGIME SCORE

    regime = load(
        "data/live/regime_score.json"
    )


    regime_state = regime.get(
        "state",
        {}
    )


    regime_score = regime_state.get(
        "score",
        0
    )


    bias = regime_state.get(
        "bias",
        "NEUTRAL"
    )


    if regime_score >= 50:

        score += 40

        conditions.append(
            "BEARISH_REGIME_CONFIRMED"
        )


    elif regime_score <= -50:

        score += 40

        conditions.append(
            "BULLISH_REGIME_CONFIRMED"
        )



    # CONFIRMATION SCORE

    confirmation = load(
        "data/live/CONFIRMATION_state.json"
    )


    confirmation_state = confirmation.get(
        "state",
        {}
    )


    confirmation_score = confirmation_state.get(
        "confirmation_score",
        0
    )


    confirmed = confirmation_state.get(
        "confirmed",
        False
    )


    if confirmed:

        score += 40

        conditions.append(
            "MARKET_CONFIRMATION_ACTIVE"
        )


    elif confirmation_score > 0:

        score += 10

        conditions.append(
            "PARTIAL_CONFIRMATION"
        )



    # BAYESIAN CONFIDENCE

    bayesian = load(
        "data/live/bayesian_state.json"
    )


    bayes_state = bayesian.get(
        "state",
        {}
    )


    prediction = bayes_state.get(
        "prediction",
        {}
    )


    confidence = prediction.get(
        "confidence",
        0
    )


    if confidence >= 65:

        score += 20

        conditions.append(
            "BAYESIAN_CONFIDENCE"
        )



    # FINAL GRADE


    if score >= 80:

        grade = "A_SETUP"

    elif score >= 60:

        grade = "B_SETUP"

    elif score >= 40:

        grade = "C_SETUP"

    else:

        grade = "NO_TRADE"



    direction = "NONE"


    if bias == "BEARISH":

        direction = "SHORT"

    elif bias == "BULLISH":

        direction = "LONG"



    return {

        "symbol":"BTCUSDT",

        "qualification":grade,

        "qualification_score":score,

        "direction":direction,

        "regime_bias":bias,

        "regime_score":regime_score,

        "confirmation_score":confirmation_score,

        "conditions":conditions

    }



def run():

    print("==============================")
    print("GSIS QUALIFICATION ENGINE v2.0")
    print("==============================")


    while True:


        result = evaluate()


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
        print("GSIS QUALIFICATION STATE")
        print(state)


        time.sleep(30)



if __name__=="__main__":
    run()
