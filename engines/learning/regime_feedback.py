import os
import json
import time
from datetime import datetime, timezone


ENGINE = "GSIS_REGIME_FEEDBACK_ENGINE_v1.0"

OUTPUT = "data/live/regime_feedback.json"

REGIME_MEMORY = "data/live/regime_memory.json"

OUTCOME_MEMORY = "data/live/outcome_validation_memory.json"



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



def build_feedback():

    regime_data = load_json(
        REGIME_MEMORY,
        {}
    )

    outcome = load_json(
        OUTCOME_MEMORY,
        {}
    )


    current_regime = regime_data.get(
        "current_regime",
        "UNKNOWN"
    )


    statistics = regime_data.get(
        "regime_statistics",
        {}
    )


    current_stats = statistics.get(
        current_regime,
        {
            "samples":0,
            "wins":0,
            "losses":0,
            "accuracy":0
        }
    )


    samples = outcome.get(
        "samples",
        0
    )


    accuracy = outcome.get(
        "accuracy",
        0
    )


    recommendation = "COLLECTING_DATA"


    if samples >= 20:

        if accuracy >= 70:
            recommendation = "INCREASE_CONFIDENCE"

        elif accuracy <= 40:
            recommendation = "REDUCE_CONFIDENCE"

        else:
            recommendation = "MAINTAIN"



    return {

        "engine":ENGINE,

        "status":"ACTIVE",

        "heartbeat":time.time(),

        "timestamp":timestamp(),

        "feedback":{

            "active_regime":
                current_regime,

            "regime_statistics":
                current_stats,

            "global_accuracy":
                accuracy,

            "total_samples":
                samples,

            "model_action":
                recommendation

        }

    }



def run():

    print("==============================")
    print("GSIS REGIME FEEDBACK ENGINE v1.0")
    print("==============================")


    while True:

        state = build_feedback()

        save_json(
            OUTPUT,
            state
        )


        print("------------------------------")
        print("GSIS FEEDBACK STATE")
        print(state)


        time.sleep(60)



if __name__ == "__main__":
    run()
