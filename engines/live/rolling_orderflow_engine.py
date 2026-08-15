import json
import time
from collections import deque


BUFFER_FILE = "data/live/market_buffer.json"
OUTPUT_FILE = "data/live/orderflow.json"


print("==============================")
print("GSIS ROLLING ORDER FLOW ENGINE v2.1")
print("==============================")


# Rolling trade window
trades = deque(maxlen=100)


def classify_trade(trade):
    """
    Binance trade classification:

    buyer_is_maker = False
        -> buyer initiated market order
        -> aggressive BUY

    buyer_is_maker = True
        -> seller initiated market order
        -> aggressive SELL
    """

    if trade["buyer_is_maker"]:
        return "SELL", trade["quantity"]

    else:
        return "BUY", trade["quantity"]



while True:

    try:

        # Read live Binance buffer

        with open(BUFFER_FILE, "r") as f:
            data = json.load(f)



        market = data["market"]



        trade = {

            "price": float(market["price"]),

            "quantity": float(market["quantity"]),

            "buyer_is_maker": market["buyer_is_maker"],

            "time": time.time()

        }



        # Add latest trade

        trades.append(trade)



        buy_volume = 0.0

        sell_volume = 0.0



        # Calculate rolling order flow

        for t in trades:


            side, qty = classify_trade(t)


            if side == "BUY":

                buy_volume += qty


            else:

                sell_volume += qty



        delta = buy_volume - sell_volume



        total_volume = buy_volume + sell_volume



        if total_volume > 0:

            imbalance = delta / total_volume

        else:

            imbalance = 0



        # Flow classification

        if imbalance > 0.20:

            flow = "STRONG_BUY_PRESSURE"


        elif imbalance > 0.05:

            flow = "BUY_PRESSURE"


        elif imbalance < -0.20:

            flow = "STRONG_SELL_PRESSURE"


        elif imbalance < -0.05:

            flow = "SELL_PRESSURE"


        else:

            flow = "BALANCED"



        # Final GSIS order-flow output

        output = {


            "symbol": "BTCUSDT",


            "price": float(market["price"]),


            "window_trades": len(trades),


            "buy_volume": round(buy_volume,8),


            "sell_volume": round(sell_volume,8),


            "delta": round(delta,8),


            "imbalance": round(imbalance,3),


            "flow": flow,


            "timestamp": time.time()

        }



        # Save for other GSIS engines

        with open(OUTPUT_FILE, "w") as f:

            json.dump(
                output,
                f,
                indent=4
            )



        # Console display

        print("------------------------------")
        print("GSIS LIVE ORDER FLOW")
        print(output)



    except Exception as e:

        print("ERROR:", e)



    time.sleep(1)
