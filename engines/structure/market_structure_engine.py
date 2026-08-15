import json
import time
from pathlib import Path


DATA_DIR = "data/live"


FILES = {

    "15M": f"{DATA_DIR}/candle_history_15M.json",
    "5M": f"{DATA_DIR}/candle_history_5M.json",
    "1H": f"{DATA_DIR}/candle_history_1H.json",
    "4H": f"{DATA_DIR}/candle_history_4H.json"

}


OUTPUT = f"{DATA_DIR}/structure_intelligence.json"


print("==============================")
print("GSIS STRUCTURE INTELLIGENCE ENGINE v7.0")
print("==============================")


def load(tf):

    try:

        with open(FILES[tf],"r") as f:
            return json.load(f)

    except:

        return []



def swings(candles):

    highs=[]
    lows=[]


    for i in range(2,len(candles)-2):

        h=candles[i]["high"]
        l=candles[i]["low"]


        if (
            h > candles[i-1]["high"]
            and h > candles[i-2]["high"]
            and h > candles[i+1]["high"]
            and h > candles[i+2]["high"]
        ):

            highs.append(
                {
                "type":"HIGH",
                "price":h,
                "index":i
                }
            )


        if (
            l < candles[i-1]["low"]
            and l < candles[i-2]["low"]
            and l < candles[i+1]["low"]
            and l < candles[i+2]["low"]
        ):

            lows.append(
                {
                "type":"LOW",
                "price":l,
                "index":i
                }
            )


    return highs,lows



def detect_bos(candles):

    highs,lows = swings(candles)


    result={

        "BOS":False,
        "CHOCH":False,
        "direction":"NONE"

    }


    if len(highs)==0 or len(lows)==0:

        return result



    price=candles[-1]["close"]


    last_high=highs[-1]["price"]
    last_low=lows[-1]["price"]



    if price > last_high:

        result["BOS"]=True
        result["direction"]="BULLISH"



    elif price < last_low:

        result["BOS"]=True
        result["direction"]="BEARISH"



    return result




def liquidity_sweep(candles):


    if len(candles)<5:

        return "NONE"



    last=candles[-1]


    previous_high=max(
        c["high"]
        for c in candles[-5:-1]
    )


    previous_low=min(
        c["low"]
        for c in candles[-5:-1]
    )


    if last["high"] > previous_high and last["close"] < previous_high:

        return "BUY_SIDE_LIQUIDITY_SWEEP"



    if last["low"] < previous_low and last["close"] > previous_low:

        return "SELL_SIDE_LIQUIDITY_SWEEP"



    return "NONE"




def fair_value_gap(candles):


    if len(candles)<3:

        return None


    a=candles[-3]
    c=candles[-1]


    if c["low"] > a["high"]:

        return {

        "type":"BULLISH_FVG",

        "low":a["high"],

        "high":c["low"]

        }



    if c["high"] < a["low"]:

        return {

        "type":"BEARISH_FVG",

        "low":c["high"],

        "high":a["low"]

        }



    return None





def analyze():


    data={}


    for tf in FILES:

        data[tf]=load(tf)



    structure_15=detect_bos(
        data["15M"]
    )


    structure_5=detect_bos(
        data["5M"]
    )


    sweep=liquidity_sweep(
        data["15M"]
    )


    fvg=fair_value_gap(
        data["15M"]
    )



    confidence=0



    if structure_15["BOS"]:
        confidence+=30


    if structure_5["BOS"]:
        confidence+=20


    if sweep!="NONE":
        confidence+=20


    if fvg:
        confidence+=20



    result={


        "symbol":"BTCUSDT",


        "4H_bias":
        "BULLISH" if data["4H"][-1]["close"] > data["4H"][0]["close"] else "BEARISH",


        "1H_bias":
        "BULLISH" if data["1H"][-1]["close"] > data["1H"][0]["close"] else "BEARISH",


        "15M_structure":
        structure_15,


        "5M_structure":
        structure_5,


        "liquidity":
        sweep,


        "FVG":
        fvg,


        "confidence":
        min(confidence,100),


        "timestamp":
        time.time()

    }


    Path(DATA_DIR).mkdir(
        exist_ok=True
    )


    with open(OUTPUT,"w") as f:

        json.dump(
            result,
            f,
            indent=4
        )


    return result




while True:


    try:

        print("------------------------------")
        print("GSIS STRUCTURE INTELLIGENCE v7.0")

        print(
            analyze()
        )

        time.sleep(15)


    except KeyboardInterrupt:

        print("Stopping GSIS Structure Intelligence")
        break
