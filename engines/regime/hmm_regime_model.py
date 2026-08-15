import json
import time
from pathlib import Path
import numpy as np


CANDLE_FILE = "data/live/candle_history_1H.json"
MEMORY_FILE = "data/live/regime_memory.json"


print("==============================")
print("GSIS HMM REGIME ENGINE v3.0")
print("==============================")


STATES = [
    "ACCUMULATION",
    "MARKUP",
    "DISTRIBUTION",
    "MARKDOWN",
    "RANGE",
    "EXPANSION"
]


TRANSITIONS = {

"ACCUMULATION":{
"ACCUMULATION":0.70,
"MARKUP":0.20,
"RANGE":0.10
},

"MARKUP":{
"MARKUP":0.70,
"EXPANSION":0.15,
"DISTRIBUTION":0.10,
"RANGE":0.05
},

"DISTRIBUTION":{
"DISTRIBUTION":0.65,
"MARKDOWN":0.20,
"RANGE":0.15
},

"MARKDOWN":{
"MARKDOWN":0.70,
"ACCUMULATION":0.10,
"RANGE":0.20
},

"RANGE":{
"RANGE":0.65,
"ACCUMULATION":0.20,
"EXPANSION":0.15
},

"EXPANSION":{
"EXPANSION":0.50,
"MARKUP":0.30,
"MARKDOWN":0.20
}

}



def load_candles():

    try:

        with open(CANDLE_FILE,"r") as f:

            return json.load(f)

    except:

        return []



def load_memory():

    try:

        with open(MEMORY_FILE,"r") as f:

            return json.load(f)

    except:

        return {

        "last_regime":"UNKNOWN"

        }



def save_memory(data):

    Path(
        "data/live"
    ).mkdir(
        parents=True,
        exist_ok=True
    )


    with open(
        MEMORY_FILE,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )



def calculate_features(candles):


    closes=np.array(
        [
        float(x["close"])
        for x in candles[-50:]
        ]
    )


    if len(closes)<20:

        return None


    returns=np.diff(closes)/closes[:-1]


    trend=(closes[-1]-closes[0])/closes[0]


    volatility=np.std(returns)


    return {

    "trend":round(float(trend),6),

    "volatility":
    round(float(volatility),6)

    }



def emission_model(features):


    trend=features["trend"]

    volatility=features["volatility"]


    score={

    "ACCUMULATION":0.1,
    "MARKUP":0.1,
    "DISTRIBUTION":0.1,
    "MARKDOWN":0.1,
    "RANGE":0.1,
    "EXPANSION":0.1

    }



    if trend>0.01:

        score["MARKUP"]+=0.6


    elif trend<-0.01:

        score["MARKDOWN"]+=0.6


    else:

        score["RANGE"]+=0.4



    if volatility>0.004:

        score["EXPANSION"]+=0.3



    total=sum(score.values())


    for x in score:

        score[x]=round(
            score[x]/total,
            3
        )


    return score



def run():


    candles=load_candles()


    features=calculate_features(
        candles
    )


    if features is None:

        return {
        "status":"WAITING_DATA"
        }


    memory=load_memory()


    previous=memory["last_regime"]


    emission=emission_model(
        features
    )


    current=max(
        emission,
        key=emission.get
    )


    transition_strength=0


    if previous in TRANSITIONS:

        transition_strength=TRANSITIONS[previous].get(
            current,
            0
        )


    transition="NO_CHANGE"


    if previous!="UNKNOWN" and previous!=current:

        transition=(
        previous+
        "_TO_"+
        current
        )


    confidence=round(
        emission[current]*100,
        2
    )


    trade_mode="WAIT"


    if current=="MARKUP":

        trade_mode="BUY_PULLBACKS"


    elif current=="MARKDOWN":

        trade_mode="SELL_RALLIES"


    elif current=="RANGE":

        trade_mode="NO_TRADE"


    result={

    "symbol":"BTCUSDT",

    "current_regime":current,

    "previous_regime":previous,

    "transition":transition,

    "transition_strength":
    transition_strength,

    "probabilities":emission,

    "confidence":confidence,

    "trade_mode":trade_mode,

    "features":features,

    "timestamp":time.time()

    }


    save_memory(
        {
        "last_regime":current
        }
    )


    return result



while True:


    try:

        print("------------------------------")
        print("GSIS HMM REGIME v3.0")
        print(run())

        time.sleep(30)


    except KeyboardInterrupt:

        print("Stopping GSIS HMM v3.0")
        break
