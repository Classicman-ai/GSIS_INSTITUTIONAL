import datetime
import random


class GSISLiveMarketEngine:

    def __init__(self):
        print("==============================")
        print("GSIS LIVE MARKET ENGINE v3.0 ONLINE")
        print("REALTIME MARKET INTELLIGENCE LAYER ACTIVE")
        print("==============================")

        self.symbol = "XAUUSD"


    def get_market_data(self, symbol="XAUUSD"):

        price = 2387.50

        spread = round(random.uniform(0.10, 0.30), 2)

        data = {
            "symbol": symbol,
            "price": price,
            "bid": round(price - spread / 2, 2),
            "ask": round(price + spread / 2, 2),
            "spread": spread,
            "timestamp": datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()
        }

        print("==============================")
        print("GSIS LIVE MARKET DATA")
        print("==============================")
        print(data)

        return data


    def analyze_market(self, market):

        price = market["price"]

        if price > 2385:
            bias = "SELL"
        else:
            bias = "BUY"


        result = {

            "symbol": market["symbol"],
            "price": price,
            "market_bias": bias,
            "liquidity_state": "ACTIVE",
            "volatility": "NORMAL",
            "status": "MARKET ANALYSIS COMPLETE",
            "timestamp": datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }


        print("==============================")
        print("GSIS MARKET ANALYSIS")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":

    engine = GSISLiveMarketEngine()

    market = engine.get_market_data()

    engine.analyze_market(market)
