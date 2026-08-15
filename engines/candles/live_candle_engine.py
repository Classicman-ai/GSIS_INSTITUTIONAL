import json
import time
from pathlib import Path


BUFFER_FILE = "data/live/market_buffer.json"
OUTPUT_DIR = "data/live"


print("==============================")
print("GSIS MULTI-TIMEFRAME CANDLE ENGINE v3.1")
print("==============================")


TIMEFRAMES = {

    "1M": 60,
    "5M": 300,
    "15M": 900,
    "1H": 3600,
    "4H": 14400,
    "1D": 86400

}


candles = {}

for tf in TIMEFRAMES:
    candles[tf] = None



def safe_read_market():

    try:

        with open(BUFFER_FILE, "r") as f:

            content = f.read().strip()

            if not content:
                return None


            data = json.loads(content)


            # Support both GSIS buffer formats

            if "market" in data:

                market = data["market"]

            else:

                market = data


            if "price" not in market:

                return None


            return {

                "symbol": market.get(
                    "symbol",
                    "BTCUSDT"
                ),

                "price": float(
                    market["price"]
                ),

                "quantity": float(
                    market.get(
                        "quantity",
                        0
                    )
                )

            }


    except Exception:

        return None



def analyze_candle(c):


    body = c["close"] - c["open"]

    candle_range = (
        c["high"] - c["low"]
    )


    if candle_range == 0:

        strength = 0

    else:

        strength = abs(body) / candle_range


    direction = (
        "BULLISH"
        if body > 0
        else "BEARISH"
    )


    return {

        "direction": direction,

        "body": round(
            body,
            2
        ),

        "range": round(
            candle_range,
            2
        ),

        "strength": round(
            strength,
            3
        )

    }



def save_candle(tf, candle):


    Path(
        OUTPUT_DIR
    ).mkdir(
        parents=True,
        exist_ok=True
    )


    filename = (
        f"{OUTPUT_DIR}/"
        f"candle_history_{tf}.json"
    )


    try:

        with open(
            filename,
            "r"
        ) as f:

            history = json.load(f)


    except:

        history = []


    history.append(
        candle
    )


    # Keep last 500 candles

    history = history[-500:]


    with open(
        filename,
        "w"
    ) as f:

        json.dump(
            history,
            f,
            indent=4
        )



def close_candle(tf):


    c = candles[tf]


    if c is None:

        return


    c["analysis"] = analyze_candle(c)

    c["timestamp"] = time.time()


    save_candle(
        tf,
        c
    )


    print("------------------------------")

    print(
        f"GSIS {tf} CANDLE CLOSED"
    )

    print(c)


    candles[tf] = None



def update_candle(tf, seconds, market):


    now = int(time.time())

    start = (
        now // seconds
    ) * seconds


    price = market["price"]

    volume = market["quantity"]



    if candles[tf] is None:


        candles[tf] = {

            "symbol":
                market["symbol"],

            "timeframe":
                tf,

            "open":
                price,

            "high":
                price,

            "low":
                price,

            "close":
                price,

            "volume":
                volume,

            "start":
                start

        }


        return



    c = candles[tf]


    if start != c["start"]:

        close_candle(tf)


        candles[tf] = {

            "symbol":
                market["symbol"],

            "timeframe":
                tf,

            "open":
                price,

            "high":
                price,

            "low":
                price,

            "close":
                price,

            "volume":
                volume,

            "start":
                start

        }


    else:


        c["high"] = max(
            c["high"],
            price
        )


        c["low"] = min(
            c["low"],
            price
        )


        c["close"] = price


        c["volume"] += volume



while True:


    try:


        market = safe_read_market()


        if market:


            for tf, seconds in TIMEFRAMES.items():

                update_candle(
                    tf,
                    seconds,
                    market
                )


        time.sleep(1)



    except KeyboardInterrupt:


        print(
            "Stopping GSIS Candle Engine"
        )

        break


    except Exception as e:


        print(
            "ERROR:",
            e
        )

        time.sleep(2)
