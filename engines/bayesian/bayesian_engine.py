import os
import json
import time
from datetime import datetime, timezone


ENGINE = "GSIS_BAYESIAN_ADAPTIVE_LEARNING_ENGINE_v2.0"

OUTPUT = "data/live/bayesian_state.json"

OUTCOME_MEMORY = "data/live/outcome_validation_memory.json"

SIGNAL_FILE = "data/live/master_signal.json"

HMM_FILE = "data/live/HMM_state.json"



def timestamp():
    return datetime.now(timezone.utc).isoformat()



def load_json(path, default):

    try:
        with open(path, "r") as f:
            return json.load(f)

    except:
        return default



def save_json(path, data):

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



def calculate_bayesian_adjustment():

    memory = load_json(
        OUTCOME_MEMORY,
        {
            "samples":0,
            "correct":0,
            "wrong":0,
            "accuracy":0
        }
    )


    samples = memory.get(
        "samples",
        0
    )

    accuracy = memory.get(
        "accuracy",
        0
    )


    if samples < 5:

        adjustment = 0

        learning = "INSUFFICIENT_HISTORY"


    else:

        if accuracy >= 60:

            adjustment = 10
            learning = "POSITIVE_LEARNING"


        elif accuracy <= 40:

            adjustment = -10
            learning = "NEGATIVE_LEARNING"


        else:

            adjustment = 0
            learning = "NEUTRAL_LEARNING"



    return {

        "samples":samples,

        "accuracy":accuracy,

        "confidence_adjustment":adjustment,

        "learning_state":learning

    }



def get_market_state():

    hmm = load_json(
        HMM_FILE,
        {}
    )


    state = hmm.get(
        "state",
        {}
    )


    return {

        "regime":
            state.get(
                "current_regime",
                "UNKNOWN"
            ),

        "confidence":
            state.get(
                "confidence",
                0
            )

    }



def get_prediction():

    signal = load_json(
        SIGNAL_FILE,
        {}
    )


    state = signal.get(
        "state",
        {}
    )


    return {

        "direction":
            state.get(
                "direction",
                "NONE"
            ),

        "signal":
            state.get(
                "signal",
                "WAIT"
            ),

        "confidence":
            state.get(
                "confidence",
                0
            )

    }



def build_state():

    bayes = calculate_bayesian_adjustment()

    market = get_market_state()

    prediction = get_prediction()


    adjusted_confidence = (

        prediction["confidence"]

        +

        bayes["confidence_adjustment"]

    )


    if adjusted_confidence > 100:
        adjusted_confidence = 100


    if adjusted_confidence < 0:
        adjusted_confidence = 0



    return {

        "engine":ENGINE,

        "status":"ACTIVE",

        "heartbeat":time.time(),

        "timestamp":timestamp(),

        "state":{

            "market":market,

            "prediction":prediction,

            "bayesian_learning":bayes,

            "adjusted_confidence":
                adjusted_confidence

        }

    }



def run():

    print("==============================")
    print("GSIS BAYESIAN ADAPTIVE LEARNING ENGINE v2.0")
    print("==============================")


    while True:

        state = build_state()


        save_json(
            OUTPUT,
            state
        )


        print("------------------------------")
        print("GSIS BAYESIAN STATE")

        print(state)


        time.sleep(60)



if __name__ == "__main__":
    run()
