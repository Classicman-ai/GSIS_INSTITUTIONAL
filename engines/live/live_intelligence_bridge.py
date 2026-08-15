import json
import time


ORDERFLOW_FILE = "data/live/orderflow.json"
OUTPUT_FILE = "data/live/market_context.json"


print("==============================")
print("GSIS LIVE INTELLIGENCE BRIDGE v1.0")
print("==============================")


while True:

    try:

        with open(ORDERFLOW_FILE, "r") as f:
            orderflow = json.load(f)


        price = float(orderflow["price"])
        delta = float(orderflow["delta"])
        imbalance = float(orderflow["imbalance"])
        flow = orderflow["flow"]


        # Determine strength

        if abs(imbalance) >= 0.50:

            strength = "EXTREME"


        elif abs(imbalance) >= 0.20:

            strength = "STRONG"


        elif abs(imbalance) >= 0.05:

            strength = "MODERATE"


        else:

            strength = "WEAK"



        # Market bias

        if delta > 0 and imbalance > 0.05:

            market_bias = "BULLISH"


        elif delta < 0 and imbalance < -0.05:

            market_bias = "BEARISH"


        else:

            market_bias = "NEUTRAL"



        # Execution state

        if strength in ["STRONG", "EXTREME"]:

            execution_state = "CONFIRMATION_REQUIRED"


        elif strength == "MODERATE":

            execution_state = "WAIT_CONFIRMATION"


        else:

            execution_state = "NO_EDGE"



        context = {

            "symbol": orderflow["symbol"],

            "price": price,

            "orderflow": flow,

            "delta": delta,

            "imbalance": imbalance,

            "strength": strength,

            "market_bias": market_bias,

            "execution_state": execution_state,

            "timestamp": time.time()

        }



        with open(OUTPUT_FILE, "w") as f:

            json.dump(
                context,
                f,
                indent=4
            )


        print("------------------------------")
        print("GSIS MARKET CONTEXT")
        print(context)



    except Exception as e:

        print("ERROR:", e)



    time.sleep(1)
