import json
import time


BUFFER = "data/live/market_buffer.json"


print("==============================")
print("GSIS ORDER FLOW BRIDGE v1.0")
print("==============================")


buy_volume = 0
sell_volume = 0
trade_count = 0


while True:

    try:

        with open(BUFFER,"r") as f:
            data=json.load(f)


        market=data["market"]

        price=float(market["price"])
        qty=float(market["quantity"])

        maker=market["buyer_is_maker"]


        trade_count += 1


        if maker:

            sell_volume += qty

        else:

            buy_volume += qty



        delta = buy_volume - sell_volume


        total = buy_volume + sell_volume


        if total > 0:

            imbalance = abs(delta)/total

        else:

            imbalance = 0



        if delta > 0:

            flow="BUY_PRESSURE"

        elif delta < 0:

            flow="SELL_PRESSURE"

        else:

            flow="NEUTRAL"



        orderflow = {

            "symbol":"BTCUSDT",

            "price":price,

            "buy_volume":round(buy_volume,6),

            "sell_volume":round(sell_volume,6),

            "delta":round(delta,6),

            "imbalance":round(imbalance,3),

            "flow":flow,

            "trades":trade_count,

            "timestamp":time.time()

        }


        with open(
        "data/live/orderflow.json","w") as f:

            json.dump(
                orderflow,
                f,
                indent=4
            )


        print(orderflow)


        time.sleep(1)



    except KeyboardInterrupt:

        print("Stopping Order Flow Bridge")
        break


    except Exception as e:

        print(e)
        time.sleep(2)
