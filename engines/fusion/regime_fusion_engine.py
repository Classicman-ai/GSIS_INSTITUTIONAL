import json
import time
from pathlib import Path


HMM_FILE = "data/live/regime_memory.json"
STRUCTURE_FILE = "data/live/structure_memory.json"
OUTPUT_FILE = "data/live/fusion_state.json"


print("==============================")
print("GSIS REGIME FUSION ENGINE v4.0")
print("==============================")


def safe_load(file):

    try:

        with open(file, "r") as f:
            return json.load(f)

    except:

        return {}



def classify_alignment(
        regime,
        structure
):


    score = 0


    # HMM contribution

    if regime == "MARKUP":
        score += 30

    elif regime == "MARKDOWN":
        score -= 30



    # Structure contribution

    trend = structure.get(
        "trend",
        "UNKNOWN"
    )


    if trend == "BULLISH":

        score += 30


    elif trend == "BEARISH":

        score -= 30



    return score



def decision(score):


    if score >= 60:

        return (
            "BULLISH_CONTINUATION",
            "BUY_PULLBACKS"
        )


    elif score <= -60:

        return (
            "BEARISH_CONTINUATION",
            "SELL_RALLIES"
        )


    elif score > 0:

        return (
            "BULLISH_DEVELOPING",
            "WAIT_CONFIRMATION"
        )


    elif score < 0:

        return (
            "BEARISH_DEVELOPING",
            "WAIT_CONFIRMATION"
        )


    else:

        return (
            "NEUTRAL",
            "NO_TRADE"
        )



def run():


    hmm = safe_load(
        HMM_FILE
    )


    structure = safe_load(
        STRUCTURE_FILE
    )


    regime = hmm.get(
        "last_regime",
        "UNKNOWN"
    )


    score = classify_alignment(
        regime,
        structure
    )


    state, action = decision(
        score
    )


    confidence = min(
        abs(score),
        100
    )


    output = {


        "symbol":
        "BTCUSDT",


        "regime":
        regime,


        "structure":
        structure,


        "market_state":
        state,


        "execution_mode":
        action,


        "fusion_score":
        score,


        "confidence":
        confidence,


        "timestamp":
        time.time()

    }


    Path(
        "data/live"
    ).mkdir(
        parents=True,
        exist_ok=True
    )


    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            output,
            f,
            indent=4
        )


    return output



while True:

    try:

        print("------------------------------")

        print(
            "GSIS FUSION STATE"
        )

        print(
            run()
        )


        time.sleep(30)


    except KeyboardInterrupt:

        print(
            "Stopping GSIS Fusion Engine"
        )

        break
