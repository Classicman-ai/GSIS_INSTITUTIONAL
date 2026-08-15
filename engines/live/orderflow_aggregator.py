import time
from collections import deque
from data.live.live_market_buffer import read_market


class OrderFlowAggregator:

    def __init__(self):

        self.trades = deque(maxlen=500)

        self.buy_volume = 0.0
        self.sell_volume = 0.0

        self.last_price = None


    def update(self):

        data = read_market()

        if not data:
            return None


        trade = data["market"]

        price = trade["price"]
        quantity = trade["quantity"]
        buyer_is_maker = trade["buyer_is_maker"]


        self.last_price = price


        order = {
            "price": price,
            "quantity": quantity,
            "side": "SELL" if buyer_is_maker else "BUY",
            "time": time.time()
        }


        self.trades.append(order)


        if order["side"] == "BUY":
            self.buy_volume += quantity
        else:
            self.sell_volume += quantity



        total_volume = self.buy_volume + self.sell_volume


        if total_volume > 0:
            imbalance = (
                self.buy_volume - self.sell_volume
            ) / total_volume

        else:
            imbalance = 0



        delta = self.buy_volume - self.sell_volume



        if delta > 0:
            flow = "BUY_PRESSURE"

        elif delta < 0:
            flow = "SELL_PRESSURE"

        else:
            flow = "NEUTRAL"



        result = {

            "symbol": trade["symbol"],

            "price": self.last_price,

            "buy_volume": round(self.buy_volume,6),

            "sell_volume": round(self.sell_volume,6),

            "delta": round(delta,6),

            "imbalance": round(imbalance,4),

            "flow_bias": flow,

            "trade_count": len(self.trades)

        }


        return result



    def run(self):

        print("==============================")
        print("GSIS ORDER FLOW AGGREGATOR v1.0")
        print("==============================")


        while True:

            result = self.update()


            if result:

                print("------------------------------")
                print("SYMBOL:", result["symbol"])
                print("PRICE:", result["price"])
                print("BUY:", result["buy_volume"])
                print("SELL:", result["sell_volume"])
                print("DELTA:", result["delta"])
                print("IMBALANCE:", result["imbalance"])
                print("FLOW:", result["flow_bias"])
                print("TRADES:", result["trade_count"])


            time.sleep(1)



if __name__ == "__main__":

    engine = OrderFlowAggregator()

    engine.run()

