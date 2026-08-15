import json
import time
from pathlib import Path


print("==============================")
print("GSIS ORDER FLOW INTELLIGENCE ENGINE v2.0")
print("==============================")


DATA_DIR = "data/live"


FILES = {

    "1M": f"{DATA_DIR}/candle_history_1M.json",
    "5M": f"{DATA_DIR}/candle_history_5M.json",
    "15M": f"{DATA_DIR}/candle_history_15M.json"

}


OUTPUT = f"{DATA_DIR}/orderflow_state.json"



def load_data(tf):

    try:

        with open(FILES[tf], "r") as f:
            return json.load(f)

    except:

        return []



def calculate_flow(candles):

    if len(candles) < 10:

        return {

            "state":"INSUFFICIENT_DATA",
            "confidence":0

        }


    recent = candles[-10:]


    buy_volume = 0
    sell_volume = 0

    bullish = 0
    bearish = 0


    ranges = []
    bodies = []


    for c in recent:


        volume = float(c.get("volume",0))

        body = c["close"] - c["open"]

        candle_range = c["high"] - c["low"]


        ranges.append(abs(candle_range))
        bodies.append(abs(body))


        if body > 0:

            buy_volume += volume
            bullish += 1


        elif body < 0:

            sell_volume += volume
            bearish += 1



    total_volume = buy_volume + sell_volume


    if total_volume == 0:

        return {

            "state":"NO_VOLUME",
            "confidence":0

        }



    delta = (
        buy_volume - sell_volume
    ) / total_volume



    avg_range = sum(ranges)/len(ranges)

    avg_body = sum(bodies)/len(bodies)


    last = recent[-1]

    last_body = abs(
        last["close"] -
        last["open"]
    )

    last_range = (
        last["high"] -
        last["low"]
    )



    body_strength = 0


    if last_range > 0:

        body_strength = (
            last_body /
            last_range
        )



    displacement = False


    if (
        last_range > avg_range*1.5
        and
        body_strength > 0.7
    ):

        displacement = True



    absorption = False


    if (

        total_volume >
        (sum(
            [float(x.get("volume",0))
             for x in recent]
        )/10)*2

        and

        last_range < avg_range

    ):

        absorption = True



    if delta > 0.35:

        state = "BUYER_CONTROL"


    elif delta < -0.35:

        state = "SELLER_CONTROL"


    else:

        state = "BALANCED"



    confidence = int(
        abs(delta)*100
    )



    return {

        "state":state,

        "buy_volume":round(
            buy_volume,4
        ),

        "sell_volume":round(
            sell_volume,4
        ),

        "delta":round(
            delta,4
        ),

        "absorption":absorption,

        "displacement":displacement,

        "body_strength":round(
            body_strength,3
        ),

        "bullish_candles":bullish,

        "bearish_candles":bearish,

        "confidence":confidence

    }



def run_engine():


    while True:


        result={}


        for tf in FILES:


            candles=load_data(tf)

            result[tf]=calculate_flow(candles)



        state={


            "symbol":"BTCUSDT",

            "engine":
            "ORDER_FLOW_V2.0",


            "timeframes":
            result,


            "timestamp":
            time.time()


        }



        Path(DATA_DIR).mkdir(
            parents=True,
            exist_ok=True
        )


        with open(
            OUTPUT,
            "w"
        ) as f:


            json.dump(
                state,
                f,
                indent=4
            )



        print("------------------------------")
        print("GSIS ORDER FLOW STATE")
        print(state)



        time.sleep(30)



run_engine()
