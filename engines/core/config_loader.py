class ConfigLoader:

    def load(self):

        return {
            "trading_mode": "SWING",
            "min_confidence": 0.75,
            "max_risk": 0.05,
            "execution_mode": "SIMULATION",
            "primary_symbol": "BTCUSDT",
            "supported_symbols": [
                "BTCUSDT",
                "ETHUSDT",
                "XAUTUSDT",
                "XAUUSD",
                "EURUSD",
                "USDJPY"
            ]
        }


if __name__ == "__main__":

    loader = ConfigLoader()

    print("===============================")
    print("GSIS CONFIG LOADER v2.0")
    print("===============================")

    print(loader.load())
