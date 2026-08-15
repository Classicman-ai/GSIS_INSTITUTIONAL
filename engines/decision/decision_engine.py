import json
import time
import os


print("==============================")
print("GSIS DECISION INTELLIGENCE ENGINE v3.0")
print("==============================")


BASE = "data/live"


def load_json(path, default=None):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return default or {}


def get_hmm():
    return load_json(
        f"{BASE}/hmm_regime_state.json",
        {}
    )


def get_fusion():
    return load_json(
        f"{BASE}/institutional_fusion_state.json",
        {}
    )


def get_orderflow():
    return load_json(
        f"{BASE}/orderflow_state.json",
        {}
    )


def get_liquidity():
    return load_json(
        f"{BASE}/liquidity_state.json",
        {}
    )


def decision_engine():

    hmm = get_hmm()
    fusion = get_fusion()
    orderflow = get_orderflow()
    liquidity = get_liquidity()


    regime = (
        fusion.get(
            "hmm_regime",
            hmm.get("regime","UNKNOWN")
        )
    )


    fusion_score = fusion.get(
        "institutional_score",
        fusion.get("fusion_score",0)
    )


    bull = 50
    bear = 50
    score = 0

    evidence = []


    # REGIME ANALYSIS

    if regime == "MARKUP":
        score += 20
        bull += 15
        evidence.append("HMM_MARKUP")

    elif regime == "MARKDOWN":
        score -= 20
        bear += 15
        evidence.append("HMM_MARKDOWN")


    # FUSION SCORE

    score += fusion_score


    # ORDER FLOW

    of_state = str(
        orderflow.get(
            "state",
            ""
        )
    )


    if "BUYER" in of_state:
        score += 15
        bull += 10
        evidence.append("BUYER_ORDERFLOW")


    elif "SELLER" in of_state:
        score -= 15
        bear += 10
        evidence.append("SELLER_ORDERFLOW")


    # LIQUIDITY

    liq_state = str(
        liquidity.get(
            "liquidity_state",
            ""
        )
    )


    if "SELL" in liq_state:
        score -= 10
        bear += 5
        evidence.append("SELL_LIQUIDITY")


    elif "BUY" in liq_state:
        score += 10
        bull += 5
        evidence.append("BUY_LIQUIDITY")


    bull = max(0,min(100,bull))
    bear = max(0,min(100,bear))


    if score >= 50 and bull > bear:

        decision = "BUY_SETUP"
        permission = "WAIT_CONFIRMATION"


    elif score <= -50 and bear > bull:

        decision = "SELL_SETUP"
        permission = "WAIT_CONFIRMATION"


    else:

        decision = "WAIT"
        permission = "BLOCK"


    confidence = abs(score)


    state = {

        "engine":
        "GSIS_DECISION_ENGINE_v3.0",

        "decision":
        decision,

        "score":
        score,

        "regime":
        regime,

        "bull_probability":
        bull,

        "bear_probability":
        bear,

        "confidence":
        confidence,

        "execution_permission":
        permission,

        "evidence":
        evidence,

        "timestamp":
        time.time()

    }


    os.makedirs(BASE,exist_ok=True)

    with open(
        f"{BASE}/decision_state.json",
        "w"
    ) as f:
        json.dump(
            state,
            f,
            indent=4
        )


    return state



def run():

    while True:

        state = decision_engine()

        print("------------------------------")
        print("GSIS DECISION STATE")
        print(state)

        time.sleep(15)



if __name__ == "__main__":
    run()
