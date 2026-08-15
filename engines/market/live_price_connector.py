# ==========================================
# GSIS LIVE PRICE CONNECTOR ENGINE v1.0
# ==========================================

import json
import urllib.request
import time

from datetime import datetime, timezone


STATE_FILE = "data/market/live_price.json"


def get_price():

    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

    try:

        response = urllib.request.urlopen(
            url,
            timeout=10
        )

        data = json.loads(
            response.read().decode()
        )

        return float(data["price"])


    except Exception as e:

        print("PRICE FEED ERROR:", e)

        return None



def save_price(price):

    import os

    os.makedirs(
        "data/market",
        exist_ok=True
    )


    state = {

        "symbol": "BTCUSDT",

        "price": price,

        "timestamp":
        datetime.now(timezone.utc)
        .isoformat()

    }


    with open(
        STATE_FILE,
        "w"
    ) as f:

        json.dump(
            state,
            f,
            indent=4
        )



def run():

    print("==============================")
    print("GSIS LIVE PRICE CONNECTOR v1.0")
    print("==============================")


    price = get_price()


    if price:

        save_price(price)

        print("------------------------------")
        print("BTCUSDT LIVE PRICE:", price)



if __name__ == "__main__":

    run()
