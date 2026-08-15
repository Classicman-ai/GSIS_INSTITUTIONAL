import json
import time


ORDERFLOW_FILE = "data/live/orderflow.json"


print("==============================")
print("GSIS ORDER FLOW INTELLIGENCE v1.0")
print("==============================")


previous_delta = 0
previous_price = None


while True:

    try:

        with open(ORDERFLOW_FILE, "r") as f:
            data = json.load(f)


        price = float(data["price"])
        delta = float(data["delta"])
        imbalance = float(data["imbalance"])
        flow = data["flow"]


        intelligence = "NO_SIGNAL"


        price_change = 0

        if previous_price is not None:
            price_change = price - previous_price



        # BUY CONDITIONS

        if (
            delta > 0
            and imbalance > 0.20
            and price_change > 0
        ):

            intelligence = "BULLISH_CONTINUATION"



        elif (
            delta > 0
            and imbalance > 0.20
            and price_change <= 0
        ):

            intelligence = "BUY_ABSORPTION"



        # SELL CONDITIONS

        elif (
            delta < 0
            and imbalance < -0.20
            and price_change < 0
        ):

            intelligence = "BEARISH_CONTINUATION"



        elif (
            delta < 0
            and imbalance < -0.20
            and price_change >= 0
        ):

            intelligence = "SELL_ABSORPTION"



        # EXHAUSTION

        elif (
            abs(delta) < abs(previous_delta)
        ):

            intelligence = "FLOW_EXHAUSTION"



        output = {

            "symbol": data["symbol"],

            "price": price,

            "flow": flow,

            "delta": delta,

            "imbalance": imbalance,

            "price_change": round(price_change,2),

            "intelligence": intelligence,

            "timestamp": time.time()

        }


        print("------------------------------")
        print("GSIS FLOW INTELLIGENCE")
        print(output)



        previous_delta = delta
        previous_price = price


    except Exception as e:

        print("ERROR:", e)


    time.sleep(1)
