import json
import time
from pathlib import Path
from urllib.request import urlopen


OUTPUT_DIR = "data/live"

SYMBOL = "BTCUSDT"


print("==============================")
print("GSIS HISTORICAL BOOTSTRAP ENGINE v1.0")
print("==============================")


TIMEFRAMES = {

    "5M": "5m",
    "15M": "15m",
    "1H": "1h",
    "4H": "4h",
    "1D": "1d"

}


LIMIT = 500



def fetch_binance(tf):

    url = (
        "https://api.binance.com/api/v3/klines?"
        f"symbol={SYMBOL}"
        f"&interval={tf}"
        f"&limit={LIMIT}"
    )


    try:

        response = urlopen(
            url,
            timeout=10
        )

        data = json.loads(
            response.read()
        )


        candles = []


        for c in data:


            candles.append({

                "symbol": SYMBOL,

                "timeframe": tf,

                "open":
                    float(c[1]),

                "high":
                    float(c[2]),

                "low":
                    float(c[3]),

                "close":
                    float(c[4]),

                "volume":
                    float(c[5]),

                "timestamp":
                    c[0] / 1000

            })


        return candles


    except Exception as e:

        print(
            "FETCH ERROR:",
            e
        )

        return []



def save(tf,data):

    Path(
        OUTPUT_DIR
    ).mkdir(
        parents=True,
        exist_ok=True
    )


    file = (
        f"{OUTPUT_DIR}/"
        f"candle_history_{tf}.json"
    )


    with open(file,"w") as f:

        json.dump(
            data,
            f,
            indent=4
        )



    print(
        "SAVED",
        tf,
        len(data),
        "candles"
    )




for name,interval in TIMEFRAMES.items():


    print("------------------------------")

    print(
        "Downloading",
        name
    )


    candles = fetch_binance(
        interval
    )


    if candles:

        save(
            name,
            candles
        )


    time.sleep(1)



print("------------------------------")
print("GSIS HISTORICAL BOOTSTRAP COMPLETE")
print("------------------------------")
