from datetime import datetime, timezone


class MarketDataEngine:

    def run(self, symbol):

        return {
            "engine": "GSIS MARKET DATA ENGINE",
            "version": "3.0",
            "symbol": symbol,
            "timestamp": datetime.now(timezone.utc).isoformat(),

            "market_data": {
                "price": 68500,
                "open": 64000,
                "high": 69000,
                "low": 63500,
                "volume": 15000
            },

            "status": "DATA_READY"
        }


if __name__ == "__main__":

    engine = MarketDataEngine()

    print(
        engine.run("BTCUSDT")
    )
