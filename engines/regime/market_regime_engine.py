import json
import time
import statistics
from pathlib import Path


DATA_FILE = "data/live/candle_history_1H.json"

OUTPUT_FILE = "data/live/market_regime.json"


print("==============================")
print("GSIS MARKET REGIME ENGINE v1.0")
print("==============================")


def load_data():

    try:

        with open(DATA_FILE,"r") as f:
            return json.load(f)

    except:

        return []



def calculate_volatility(candles):

    ranges=[]

    for c in candles[-50:]:

        ranges.append(
            c["high"] - c["low"]
        )


    if len(ranges)==0:
        return 0


    return statistics.mean(ranges)



def detect_trend(candles):


    closes=[
        c["close"]
        for c in candles[-50:]
    ]


    if len(closes)<10:

        return "UNKNOWN"



    first=closes[0]

    last=closes[-1]


    change=((last-first)/first)*100



    if change > 1:

        return "BULLISH"



    if change < -1:

        return "BEARISH"



    return "SIDEWAYS"



def detect_market_phase(candles):


    if len(candles)<20:

        return "INSUFFICIENT_DATA"



    highs=[
        c["high"]
        for c in candles[-20:]
    ]


    lows=[
        c["low"]
        for c in candles[-20:]
    ]



    high_range=max(highs)-min(highs)

    avg_range=statistics.mean(
        [
            h-l
            for h,l in zip(highs,lows)
        ]
    )



    compression = (
        high_range < avg_range * 8
    )



    trend = detect_trend(candles)



    if compression and trend=="SIDEWAYS":

        return "ACCUMULATION"



    if trend=="SIDEWAYS":

        return "RANGE"



    if trend=="BULLISH":

        return "MARKUP"



    if trend=="BEARISH":

        return "MARKDOWN"



    return "UNKNOWN"



def expansion_state(candles):


    if len(candles)<20:

        return "UNKNOWN"



    recent = candles[-1]


    avg = statistics.mean(

        [
        c["high"]-c["low"]
        for c in candles[-20:]
        ]

    )



    current = (
        recent["high"]
        -
        recent["low"]
    )


    if current > avg*2:

        return "EXPANSION"



    return "NORMAL"




def confidence(regime,trend):


    score=0


    if regime!="UNKNOWN":
        score+=40


    if trend!="UNKNOWN":
        score+=30


    return score




def analyze():


    candles=load_data()


    trend=detect_trend(candles)


    regime=detect_market_phase(
        candles
    )


    volatility=calculate_volatility(
        candles
    )


    expansion=expansion_state(
        candles
    )


    result={


        "symbol":"BTCUSDT",


        "trend":
        trend,


        "regime":
        regime,


        "volatility":
        round(volatility,2),


        "expansion":
        expansion,


        "confidence":
        confidence(
            regime,
            trend
        ),


        "timestamp":
        time.time()


    }


    Path(
        "data/live"
    ).mkdir(
        exist_ok=True
    )


    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            result,
            f,
            indent=4
        )


    return result




while True:


    try:

        print("------------------------------")
        print("GSIS MARKET REGIME")

        print(
            analyze()
        )

        time.sleep(30)


    except KeyboardInterrupt:

        print("Stopping Regime Engine")
        break
