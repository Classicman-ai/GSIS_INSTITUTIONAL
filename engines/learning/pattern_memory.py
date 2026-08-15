import os
import json
import time
from datetime import datetime, timezone


ENGINE = "GSIS_PATTERN_MEMORY_ENGINE_v1.0"

OUTPUT = "data/live/pattern_memory.json"

OUTCOME_FILE = "data/live/outcome_validation_memory.json"

BAYES_FILE = "data/live/bayesian_state.json"



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



def build_memory():

    outcome = load_json(
        OUTCOME_FILE,
        {
            "samples":0,
            "correct":0,
            "wrong":0,
            "accuracy":0
        }
    )


    bayes = load_json(
        BAYES_FILE,
        {}
    )


    samples = outcome.get(
        "samples",
        0
    )

    correct = outcome.get(
        "correct",
        0
    )

    wrong = outcome.get(
        "wrong",
        0
    )


    accuracy = outcome.get(
        "accuracy",
        0
    )


    confidence_history = {

        "high_confidence": {
            "samples":0,
            "wins":0,
            "accuracy":0
        },

        "medium_confidence": {
            "samples":0,
            "wins":0,
            "accuracy":0
        },

        "low_confidence": {
            "samples":0,
            "wins":0,
            "accuracy":0
        }

    }


    if samples >= 10:

        if accuracy >= 70:

            learning_state = "STRONG_MODEL"

        elif accuracy >= 50:

            learning_state = "STABLE_MODEL"

        else:

            learning_state = "WEAK_MODEL"


    else:

        learning_state = "COLLECTING_DATA"



    return {

        "engine":ENGINE,

        "status":"ACTIVE",

        "heartbeat":time.time(),

        "timestamp":timestamp(),

        "memory":{

            "total_samples":samples,

            "correct_predictions":correct,

            "wrong_predictions":wrong,

            "historical_accuracy":accuracy,

            "learning_state":
                learning_state,

            "confidence_history":
                confidence_history,

            "bayesian_link":
                bayes.get(
                    "state",
                    {}
                )

        }

    }



def run():

    print("==============================")
    print("GSIS PATTERN MEMORY ENGINE v1.0")
    print("==============================")


    while True:

        state = build_memory()


        save_json(
            OUTPUT,
            state
        )


        print("------------------------------")
        print("GSIS MEMORY STATE")
        print(state)


        time.sleep(60)



if __name__ == "__main__":
    run()
