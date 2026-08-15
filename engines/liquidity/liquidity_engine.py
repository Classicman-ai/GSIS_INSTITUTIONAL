import json
import time
from pathlib import Path


CANDLE_FILE = "data/live/candle_history_5M.json"
OUTPUT_FILE = "data/live/liquidity_state.json"


print("==============================")
print("GSIS LIQUIDITY INTELLIGENCE ENGINE v6.6")
print("==============================")


def load_candles():

    try:
        with open(CANDLE_FILE, "r") as f:
            return json.load(f)

    except:
        return []



def get_liquidity_levels(candles):

    highs = []
    lows = []

    for c in candles[-50:]:

        highs.append(float(c["high"]))
        lows.append(float(c["low"]))

    if not highs:
        return None, None

    return max(highs), min(lows)



def detect_liquidity_clusters(candles):

    highs = []
    lows = []

    for c in candles[-30:]:

        highs.append(float(c["high"]))
        lows.append(float(c["low"]))


    equal_high = 0
    equal_low = 0


    for i in range(len(highs)-1):

        if abs(highs[i] - highs[i+1]) <= 20:
            equal_high += 1


        if abs(lows[i] - lows[i+1]) <= 20:
            equal_low += 1


    return equal_high, equal_low



def detect_sweep(candle, high, low):

    candle_high = float(candle["high"])
    candle_low = float(candle["low"])
    close = float(candle["close"])


    if high:

        if candle_high > high and close < high:

            return "BUY_SIDE_LIQUIDITY_SWEPT"



    if low:

        if candle_low < low and close > low:

            return "SELL_SIDE_LIQUIDITY_SWEPT"



    return "NO_SWEEP"



def calculate_strength(high_count, low_count):

    total = high_count + low_count


    if total == 0:

        return 0


    strength = min(
        total / 10,
        1
    )


    return round(
        strength,
        2
    )



def analyze():


    candles = load_candles()


    if len(candles) < 10:

        return {
            "status":
            "INSUFFICIENT_DATA"
        }



    current = candles[-1]


    price = float(
        current["close"]
    )


    swing_high, swing_low = get_liquidity_levels(
        candles
    )


    high_cluster, low_cluster = detect_liquidity_clusters(
        candles
    )


    sweep = detect_sweep(
        current,
        swing_high,
        swing_low
    )


    strength = calculate_strength(
        high_cluster,
        low_cluster
    )



    # Institutional classification

    if sweep != "NO_SWEEP":

        state = sweep


    elif high_cluster > 0 and low_cluster > 0:

        state = "DUAL_LIQUIDITY_RANGE"


    elif high_cluster > 0:

        state = "BUY_SIDE_LIQUIDITY_ZONE"


    elif low_cluster > 0:

        state = "SELL_SIDE_LIQUIDITY_ZONE"


    else:

        state = "NO_LIQUIDITY"



    if state == "SELL_SIDE_LIQUIDITY_ZONE":

        bias = "BULLISH_LIQUIDITY_TARGET"


    elif state == "BUY_SIDE_LIQUIDITY_ZONE":

        bias = "BEARISH_LIQUIDITY_TARGET"


    elif state == "SELL_SIDE_LIQUIDITY_SWEPT":

        bias = "POSSIBLE_BULLISH_REVERSAL"


    elif state == "BUY_SIDE_LIQUIDITY_SWEPT":

        bias = "POSSIBLE_BEARISH_REVERSAL"


    else:

        bias = "NEUTRAL"



    result = {

        "symbol":
        current["symbol"],

        "price":
        price,

        "liquidity_state":
        state,

        "liquidity_bias":
        bias,

        "swing_high":
        swing_high,

        "swing_low":
        swing_low,

        "high_clusters":
        high_cluster,

        "low_clusters":
        low_cluster,

        "strength":
        strength,

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
            result,
            f,
            indent=4
        )


    return result



while True:

    try:

        print("------------------------------")
        print("GSIS LIQUIDITY STATE")
        print(analyze())

        time.sleep(30)


    except KeyboardInterrupt:

        print("Stopping GSIS Liquidity Engine")
        break
