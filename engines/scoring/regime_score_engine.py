import os
import json
import time
from datetime import datetime, timezone


ENGINE="GSIS_REGIME_SCORE_ENGINE_v1.1"

OUTPUT="data/live/regime_score.json"



def now():
    return datetime.now(timezone.utc).isoformat()



def load(path):

    try:
        with open(path,"r") as f:
            return json.load(f)
    except:
        return {}



def save(path,data):

    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    with open(path,"w") as f:
        json.dump(
            data,
            f,
            indent=4
        )



def calculate():

    score=0
    evidence=[]


    # HMM

    hmm=load(
        "data/live/hmm_state.json"
    )

    hmm_state=hmm.get(
        "state",
        {}
    )


    regime=hmm_state.get(
        "current_regime"
    )


    if regime=="MARKDOWN":

        score+=20
        evidence.append(
            "HMM_BEARISH_REGIME"
        )


    elif regime=="MARKUP":

        score-=20
        evidence.append(
            "HMM_BULLISH_REGIME"
        )



    # FUSION

    fusion=load(
        "data/live/FUSION_state.json"
    )

    fusion_state=fusion.get(
        "state",
        {}
    )


    fusion_regime=fusion_state.get(
        "regime"
    )


    orderflow=fusion_state.get(
        "orderflow"
    )


    if fusion_regime=="MARKDOWN":

        score+=15
        evidence.append(
            "FUSION_BEARISH_REGIME"
        )


    if orderflow in [
        "BEARISH",
        "SELL",
        "SHORT"
    ]:

        score+=20
        evidence.append(
            "BEARISH_ORDERFLOW"
        )


    elif orderflow in [
        "BULLISH",
        "BUY",
        "LONG"
    ]:

        score-=20
        evidence.append(
            "BULLISH_ORDERFLOW"
        )



    # BAYESIAN

    bayes=load(
        "data/live/bayesian_state.json"
    )


    bayes_state=bayes.get(
        "state",
        {}
    )


    market=bayes_state.get(
        "market",
        {}
    )


    bayes_regime=market.get(
        "regime"
    )


    confidence=market.get(
        "confidence",
        0
    )


    if bayes_regime=="MARKDOWN" and confidence>=50:

        score+=25

        evidence.append(
            "BAYESIAN_BEARISH"
        )



    if score>=40:

        bias="BEARISH"

    elif score<=-40:

        bias="BULLISH"

    else:

        bias="NEUTRAL"



    return {

        "score":score,
        "bias":bias,
        "evidence":evidence

    }



def run():

    print("==============================")
    print("GSIS REGIME SCORE ENGINE v1.1")
    print("==============================")


    while True:

        result=calculate()


        state={

            "engine":ENGINE,

            "status":"ACTIVE",

            "heartbeat":time.time(),

            "timestamp":now(),

            "state":result

        }


        save(
            OUTPUT,
            state
        )


        print("------------------------------")
        print("GSIS REGIME SCORE STATE")
        print(state)


        time.sleep(30)



if __name__=="__main__":
    run()
