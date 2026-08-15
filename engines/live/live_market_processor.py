import time
from data.live.live_market_buffer import read_market


class LiveMarketProcessor:

    def __init__(self):
        self.buy_volume = 0
        self.sell_volume = 0
        self.last_price = None


    def process(self):

        while True:

            data = read_market()

            if data:

                market = data["market"]

                price = market["price"]
                quantity = market["quantity"]
                buyer_maker = market["buyer_is_maker"]

                self.last_price = price


                if buyer_maker:
                    self.sell_volume += quantity
                else:
                    self.buy_volume += quantity


                delta = self.buy_volume - self.sell_volume


                print("==========================")
                print("GSIS LIVE MARKET PROCESSOR")
                print("==========================")
                print(f"PRICE: {price}")
                print(f"BUY VOLUME: {self.buy_volume:.6f}")
                print(f"SELL VOLUME: {self.sell_volume:.6f}")
                print(f"DELTA: {delta:.6f}")


                if delta > 0:
                    print("FLOW: BUY PRESSURE")
                elif delta < 0:
                    print("FLOW: SELL PRESSURE")
                else:
                    print("FLOW: NEUTRAL")


            time.sleep(1)



if __name__ == "__main__":

    engine = LiveMarketProcessor()
    engine.process()
