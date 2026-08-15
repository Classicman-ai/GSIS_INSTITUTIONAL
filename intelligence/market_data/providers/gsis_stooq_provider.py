import sys
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from intelligence.market_data.gsis_provider_base import GSISProviderBase


print("==============================")
print("GSIS STOOQ PROVIDER v1.0 ONLINE")
print("PLACEHOLDER PROVIDER INITIALIZED")
print("==============================")


class GSISStooqProvider(GSISProviderBase):

    def __init__(self):
        super().__init__("STOOQ")
        self.status = "NOT CONFIGURED"

    def connect(self):
        self.last_check = self.timestamp()
        return {
            "provider": self.name,
            "status": self.status,
            "message": "Stooq provider is not implemented for XAUUSD.",
            "timestamp": self.last_check
        }

    def get_quote(self, symbol):
        return {
            "provider": self.name,
            "status": "UNSUPPORTED",
            "symbol": symbol,
            "message": "Live XAUUSD quotes are not supported by this provider."
        }

    def get_candles(self, symbol, timeframe="DAILY", limit=100):
        return {
            "provider": self.name,
            "status": "UNSUPPORTED",
            "symbol": symbol,
            "records": 0,
            "candles": []
        }

    def download_history(self, symbol, timeframe, start, end):
        return {
            "provider": self.name,
            "status": "UNSUPPORTED",
            "symbol": symbol,
            "records": 0,
            "candles": []
        }


if __name__ == "__main__":
    provider = GSISStooqProvider()

    print("==============================")
    print("GSIS STOOQ PROVIDER TEST")
    print("==============================")

    print(provider.connect())
    print(provider.health())
