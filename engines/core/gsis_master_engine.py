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



def get_regime():

    hmm = load_json(
        "hmm_regime_state.json"
    )

    return (
        hmm.get("current_regime")
        or hmm.get("regime")
        or hmm.get("hmm_regime")
        or "UNKNOWN"
    )



def get_hmm_confidence():

    hmm = load_json(
        "hmm_regime_state.json"
    )

    return hmm.get(
        "confidence",
        0
    )



def get_orderflow():

    data = load_json(
        "orderflow_state.json"
    )

    score = 0
    evidence = []

    timeframes = data.get(
        "timeframes",
        {}
    )


    tf15 = timeframes.get(
        "15M",
        {}
    )

    tf5 = timeframes.get(
        "5M",
        {}
    )


    if tf15.get("state") == "BUYER_CONTROL":

        score += 40
        evidence.append(
            "15M_BUYER_CONTROL"
        )


    elif tf15.get("state") == "SELLER_CONTROL":

        score -= 40
        evidence.append(
            "15M_SELLER_CONTROL"
        )


    if tf5.get("state") == "BUYER_CONTROL":

        score += 20
        evidence.append(
            "5M_BUYER_CONTROL"
        )


    elif tf5.get("state") == "SELLER_CONTROL":

        score -= 20
        evidence.append(
            "5M_SELLER_CONTROL"
        )


    return score, evidence



def get_structure():

    data = load_json(
        "structure_state.json"
    )


    structure = data.get(
        "structure",
        {}
    )


    score = structure.get(
        "structure_score",
        0
    )


    evidence = []


    if structure.get("BOS"):

        evidence.append(
            "BOS"
        )


    if structure.get("CHOCH"):

        evidence.append(
            "CHOCH"
        )


    return score, evidence



def analyze():

    score = 0
    evidence = []


    regime = get_regime()

    hmm_confidence = get_hmm_confidence()


    if regime == "MARKUP":

        score += 25
        evidence.append(
            "HMM_MARKUP"
        )


    elif regime == "MARKDOWN":

        score -= 25
        evidence.append(
            "HMM_MARKDOWN"
        )


    elif regime == "ACCUMULATION":

        score += 10
        evidence.append(
            "HMM_ACCUMULATION"
        )


    elif regime == "DISTRIBUTION":

        score -= 10
        evidence.append(
            "HMM_DISTRIBUTION"
        )



    order_score, order_evidence = get_orderflow()

    score += order_score
    evidence += order_evidence



    structure_score, structure_evidence = get_structure()

    score += structure_score
    evidence += structure_evidence



    direction = "NONE"

    status = "BLOCKED"



    if score >= 70:

        direction = "BUY"
        status = "EXECUTE_READY"


    elif score <= -70:

        direction = "SELL"
        status = "EXECUTE_READY"


    elif abs(score) >= 40:

        status = "WATCH"



    quality = min(
        100,
        abs(score) + hmm_confidence
    )



    return {

        "engine":
        "GSIS_MASTER_ORCHESTRATOR_v4.0",


        "symbol":
        "BTCUSDT",


        "regime":
        regime,


        "hmm_confidence":
        hmm_confidence,


        "institutional_score":
        score,


        "quality":
        quality,


        "direction":
        direction,


        "status":
        status,


        "evidence":
        evidence,


        "timestamp":
        time.time()

    }



def save(state):

    os.makedirs(
        BASE,
        exist_ok=True
    )


    with open(
        f"{BASE}/master_signal.json",
        "w"
    ) as f:

        json.dump(
            state,
            f,
            indent=4
        )



def run():

    print("==============================")
    print("GSIS MASTER ORCHESTRATOR v4.0")
    print("==============================")


    while True:

        state = analyze()


        save(state)


        print("------------------------------")
        print("GSIS MASTER SIGNAL")
        print(state)


        time.sleep(15)



if __name__ == "__main__":

    run()
