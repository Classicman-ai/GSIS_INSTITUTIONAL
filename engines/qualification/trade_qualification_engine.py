import json
import time
import os


BASE = "data/live"


def load_json(filename):

    try:
        with open(
            os.path.join(BASE, filename),
            "r"
        ) as f:
            return json.load(f)

    except Exception:

        return {}



def qualify():

    master = load_json(
        "master_signal.json"
    )

    orderflow = load_json(
        "orderflow_state.json"
    )

    structure = load_json(
        "structure_state.json"
    )


    score = 0
    evidence = []


    regime = master.get(
        "regime",
        "UNKNOWN"
    )


    direction = "NONE"



    # REGIME CHECK

    if regime == "MARKDOWN":

        score -= 20
        evidence.append(
            "BEARISH_REGIME"
        )


    elif regime == "MARKUP":

        score += 20
        evidence.append(
            "BULLISH_REGIME"
        )



    # ORDER FLOW CHECK

    tfs = orderflow.get(
        "timeframes",
        {}
    )


    tf15 = tfs.get(
        "15M",
        {}
    )

    tf5 = tfs.get(
        "5M",
        {}
    )



    if tf15.get("state") == "SELLER_CONTROL":

        score -= 30
        evidence.append(
            "15M_SELLER_CONTROL"
        )


    if tf5.get("state") == "SELLER_CONTROL":

        score -= 20
        evidence.append(
            "5M_SELLER_CONFIRMATION"
        )


    if tf5.get("state") == "BUYER_CONTROL":

        evidence.append(
            "5M_BUYER_PRESSURE"
        )



    # STRUCTURE CHECK

    s = structure.get(
        "structure",
        {}
    )


    if s.get("CHOCH"):

        score += 25
        evidence.append(
            "CHOCH_CONFIRMED"
        )


    if s.get("BOS"):

        score += 25
        evidence.append(
            "BOS_CONFIRMED"
        )



    # QUALIFICATION LOGIC


    status = "WAIT"


    if score <= -70:

        direction = "SELL"
        status = "SELL_READY"


    elif score >= 70:

        direction = "BUY"
        status = "BUY_READY"


    else:

        status = "NO_TRADE"



    confidence = min(
        100,
        abs(score)
    )


    return {

        "engine":
        "GSIS_TRADE_QUALIFICATION_v1.0",

        "symbol":
        "BTCUSDT",

        "qualification":
        status,

        "direction":
        direction,

        "score":
        score,

        "confidence":
        confidence,

        "evidence":
        evidence,

        "timestamp":
        time.time()

    }



def run():

    print("==============================")
    print("GSIS TRADE QUALIFICATION ENGINE v1.0")
    print("==============================")


    while True:

        state = qualify()


        with open(
            f"{BASE}/qualification_state.json",
            "w"
        ) as f:

            json.dump(
                state,
                f,
                indent=4
            )


        print("------------------------------")
        print("GSIS QUALIFICATION STATE")
        print(state)


        time.sleep(15)



if __name__ == "__main__":

    run()
