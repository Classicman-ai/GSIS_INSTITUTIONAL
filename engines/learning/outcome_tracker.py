import os
import json
import time
from datetime import datetime, timezone


ENGINE = "GSIS_OUTCOME_TRACKER_ENGINE_v1.0"

OUTPUT = "data/live/outcome_state.json"
MEMORY = "data/live/outcome_memory.json"


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



def get_prediction():

    bayes = load_json(
        "data/live/bayesian_state.json",
        {}
    )

    state = bayes.get(
        "state",
        {}
    )

    prediction = state.get(
        "prediction_state",
        {}
    )


    return prediction



def evaluate_prediction():

    memory = load_json(
        MEMORY,
        {
            "total_predictions":0,
            "correct":0,
            "wrong":0,
            "accuracy":0
        }
    )


    prediction = get_prediction()


    market_state = prediction.get(
        "market_state",
        "UNKNOWN"
    )


    confidence = prediction.get(
        "bearish_probability",
        0
    )


    result = "PENDING"


    # Placeholder evaluation layer.
    # Future version connects candle outcome engine.

    if market_state == "BEARISH" and confidence >= 60:

        result = "MONITORING_SHORT_BIAS"


    memory["total_predictions"] += 1


    if memory["total_predictions"] > 0:

        memory["accuracy"] = round(
            (
                memory["correct"]
                /
                memory["total_predictions"]
            ) * 100,
            2
        )


    save_json(
        MEMORY,
        memory
    )


    return {

        "prediction": prediction,

        "evaluation": result,

        "statistics": {

            "samples":
                memory["total_predictions"],

            "correct":
                memory["correct"],

            "wrong":
                memory["wrong"],

            "accuracy":
                memory["accuracy"]

        }

    }



def save_state():

    payload = {

        "engine":ENGINE,

        "status":"ACTIVE",

        "heartbeat":time.time(),

        "timestamp":timestamp(),

        "state":
            evaluate_prediction()

    }


    save_json(
        OUTPUT,
        payload
    )


    return payload



def run():

    print("==============================")
    print("GSIS OUTCOME TRACKER ENGINE v1.0")
    print("==============================")


    while True:

        state = save_state()

        print("------------------------------")
        print("GSIS OUTCOME STATE")

        print(state)

        time.sleep(60)



if __name__ == "__main__":
    run()
