import os
import json
import time
from datetime import datetime, timezone


ENGINE = "GSIS_OUTCOME_VALIDATOR_ENGINE_v2.0"

OUTPUT = "data/live/outcome_validator_state.json"
MEMORY = "data/live/outcome_validation_memory.json"


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

    data = load_json(
        "data/live/master_signal.json",
        {}
    )

    state = data.get(
        "state",
        {}
    )

    return {

        "symbol":
            state.get(
                "symbol",
                "BTCUSDT"
            ),

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



def get_market():

    data = load_json(
        "data/live/market_buffer.json",
        {}
    )

    state = data.get(
        "state",
        {}
    )

    market = state.get(
        "market_data",
        {}
    )

    return {

        "open":
            market.get("open"),

        "close":
            market.get("close"),

        "timestamp":
            market.get("timestamp")

    }



def evaluate():

    memory = load_json(
        MEMORY,
        {
            "samples":0,
            "correct":0,
            "wrong":0,
            "accuracy":0
        }
    )


    prediction = get_prediction()

    market = get_market()


    result = "WAITING"


    direction = prediction["direction"]


    open_price = market["open"]

    close_price = market["close"]


    if open_price and close_price:


        change = close_price - open_price


        if direction == "LONG":

            if change > 0:
                result = "CORRECT"
                memory["correct"] += 1

            elif change < 0:
                result = "WRONG"
                memory["wrong"] += 1



        elif direction == "SHORT":

            if change < 0:
                result = "CORRECT"
                memory["correct"] += 1

            elif change > 0:
                result = "WRONG"
                memory["wrong"] += 1


        else:

            result = "NO_DIRECTION"


        memory["samples"] += 1



    if memory["samples"] > 0:

        memory["accuracy"] = round(
            (
                memory["correct"]
                /
                memory["samples"]
            )
            * 100,
            2
        )


    save_json(
        MEMORY,
        memory
    )


    return {

        "prediction":prediction,

        "market":market,

        "result":result,

        "performance":memory

    }



def run():

    print("==============================")
    print("GSIS OUTCOME VALIDATOR v2.0")
    print("==============================")


    while True:

        state = {

            "engine":ENGINE,

            "status":"ACTIVE",

            "heartbeat":time.time(),

            "timestamp":timestamp(),

            "state":evaluate()

        }


        save_json(
            OUTPUT,
            state
        )


        print("------------------------------")
        print("GSIS VALIDATOR STATE")
        print(state)


        time.sleep(60)



if __name__ == "__main__":
    run()
