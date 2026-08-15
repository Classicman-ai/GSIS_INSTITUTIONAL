import json
import time
from pathlib import Path


print("==============================")
print("GSIS INSTITUTIONAL FUSION ENGINE v9.1")
print("==============================")


DATA = Path("data/live")

OUTPUT = DATA / "institutional_fusion_state.json"


SOURCES = {

    "hmm": DATA / "hmm_regime_state.json",

    "structure": DATA / "market_structure_state.json",

    "liquidity": DATA / "liquidity_state.json",

    "orderflow": DATA / "orderflow_state.json"

}



def load_file(path):

    try:

        with open(path, "r") as f:

            return json.load(f)

    except:

        return {}



def hmm_analysis(data):

    regime = data.get(
        "current_regime",
        "UNKNOWN"
    )


    score = {

        "MARKUP": 25,

        "MARKDOWN": -25,

        "ACCUMULATION": 15,

        "DISTRIBUTION": -15,

        "RANGE": 0

    }


    return score.get(regime,0), regime



def structure_analysis(data):

    score = 0


    internal = data.get(
        "internal_structure",
        ""
    )


    if internal == "BULLISH":
        score += 20


    if internal == "BEARISH":
        score -= 20


    if data.get("BOS"):
        score += 15


    if data.get("CHOCH"):
        score += 10


    return score



def liquidity_analysis(data):

    state=data.get(
        "liquidity_state",
        ""
    )


    if state=="SELL_SIDE_LIQUIDITY_ZONE":

        return 15


    if state=="BUY_SIDE_LIQUIDITY_ZONE":

        return -15


    if state=="DUAL_LIQUIDITY_RANGE":

        return 0


    return 0



def orderflow_analysis(data):

    score=0


    tf=data.get(
        "timeframes",
        {}
    )


    m5=tf.get(
        "5M",
        {}
    )


    m15=tf.get(
        "15M",
        {}
    )


    if m5.get("state")=="BUYER_CONTROL":
        score += 15


    if m5.get("state")=="SELLER_CONTROL":
        score -= 15


    if m15.get("state")=="BUYER_CONTROL":
        score += 10


    if m15.get("state")=="SELLER_CONTROL":
        score -= 10


    if m5.get("absorption"):
        score += 5


    if m15.get("absorption"):
        score -= 5


    if m5.get("displacement"):
        score += 10


    return score



def decision(score):


    if score >= 50:

        return (
            "STRONG_BULLISH",
            "EXECUTE_LONG"
        )


    if score >= 25:

        return (
            "BULLISH_DEVELOPING",
            "WAIT_PULLBACK"
        )


    if score <= -50:

        return (
            "STRONG_BEARISH",
            "EXECUTE_SHORT"
        )


    if score <= -25:

        return (
            "BEARISH_DEVELOPING",
            "WAIT_RALLY"
        )


    return (
        "NEUTRAL_RANGE",
        "NO_TRADE"
    )



def probability(score):

    bull = 50 + score

    if bull > 95:
        bull = 95

    if bull < 5:
        bull = 5


    return bull,100-bull



def run():


    while True:


        hmm = load_file(
            SOURCES["hmm"]
        )

        structure = load_file(
            SOURCES["structure"]
        )

        liquidity = load_file(
            SOURCES["liquidity"]
        )

        orderflow = load_file(
            SOURCES["orderflow"]
        )


        hmm_score,regime = hmm_analysis(hmm)


        total = (

            hmm_score

            +

            structure_analysis(structure)

            +

            liquidity_analysis(liquidity)

            +

            orderflow_analysis(orderflow)

        )


        state,permission = decision(total)


        bull,bear = probability(total)


        result={


            "symbol":"BTCUSDT",

            "engine":
            "GSIS_INSTITUTIONAL_FUSION_v9.1",


            "institutional_state":
            state,


            "fusion_score":
            total,


            "bull_probability":
            bull,


            "bear_probability":
            bear,


            "execution_permission":
            permission,


            "hmm_regime":
            regime,


            "components":{


                "structure_score":
                structure_analysis(structure),


                "liquidity_score":
                liquidity_analysis(liquidity),


                "orderflow_score":
                orderflow_analysis(orderflow)

            },


            "timestamp":
            time.time()

        }


        DATA.mkdir(
            parents=True,
            exist_ok=True
        )


        with open(
            OUTPUT,
            "w"
        ) as f:

            json.dump(
                result,
                f,
                indent=4
            )


        print("------------------------------")
        print("GSIS INSTITUTIONAL STATE")
        print(result)


        time.sleep(30)



if __name__=="__main__":

    run()
