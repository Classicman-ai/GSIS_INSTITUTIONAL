import json
import time
import os


print("==============================")
print("GSIS STRUCTURE INTELLIGENCE ENGINE v2.0")
print("==============================")


CANDLE_FILE = "data/live/candle_history_1M.json"


def load_candles():

    try:
        with open(CANDLE_FILE,"r") as f:
            return json.load(f)

    except:
        return []


def analyze_structure():

    candles = load_candles()

    if len(candles) < 10:

        return {
            "engine":"GSIS_STRUCTURE_ENGINE_v2.0",
            "status":"INSUFFICIENT_DATA",
            "timestamp":time.time()
        }


    recent = candles[-20:]


    highs = [
        float(c.get("high",0))
        for c in recent
    ]

    lows = [
        float(c.get("low",0))
        for c in recent
    ]


    closes = [
        float(c.get("close",0))
        for c in recent
    ]


    current = closes[-1]


    swing_high=max(highs)
    swing_low=min(lows)


    previous_high=max(highs[:-5])
    previous_low=min(lows[:-5])


    BOS=False
    CHOCH=False


    if current > previous_high:
        BOS=True


    if current < previous_low:
        CHOCH=True



    bullish_count=0
    bearish_count=0


    for c in recent:

        o=float(c.get("open",0))
        cl=float(c.get("close",0))


        if cl>o:
            bullish_count+=1

        elif cl<o:
            bearish_count+=1



    displacement=False

    last_range=float(recent[-1]["high"])-float(recent[-1]["low"])


    avg_range=sum(
        float(x["high"])-float(x["low"])
        for x in recent
    )/len(recent)


    if last_range > avg_range*1.8:
        displacement=True



    if BOS:
        trend="BULLISH"

    elif CHOCH:
        trend="BEARISH"

    else:
        trend="RANGE"



    score=0


    if BOS:
        score+=40

    if CHOCH:
        score-=40

    if bullish_count>bearish_count:
        score+=20

    elif bearish_count>bullish_count:
        score-=20


    if displacement:
        score+=20



    return {

        "engine":
        "GSIS_STRUCTURE_ENGINE_v2.0",

        "symbol":
        "BTCUSDT",

        "structure":{

            "trend":trend,

            "BOS":BOS,

            "CHOCH":CHOCH,

            "displacement":displacement,

            "swing_high":swing_high,

            "swing_low":swing_low,

            "current_price":current,

            "bullish_candles":bullish_count,

            "bearish_candles":bearish_count,

            "structure_score":score
        },

        "timestamp":time.time()
    }



def run():

    while True:

        state=analyze_structure()

        print("------------------------------")
        print("GSIS STRUCTURE STATE")
        print(state)

        time.sleep(30)



if __name__=="__main__":
    run()
