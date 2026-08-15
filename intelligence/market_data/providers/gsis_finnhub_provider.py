import os
import datetime
import requests

from dotenv import load_dotenv

from intelligence.market_data.gsis_provider_base import (
    GSISProviderBase
)


class GSISFinnhubProvider(GSISProviderBase):


    def __init__(self):

        super().__init__("FINNHUB")

        load_dotenv(dotenv_path=".env")

        self.api_key = os.getenv(
            "FINNHUB_API_KEY"
        )

        self.base_url = "https://finnhub.io/api/v1"

        print("==============================")
        print("GSIS FINNHUB PROVIDER v1.0 ONLINE")
        print("MARKET INTELLIGENCE ENGINE ACTIVE")
        print("==============================")


    def connect(self):

        if not self.api_key:

            self.status = "API KEY MISSING"

            return {
                "provider": self.name,
                "status": self.status,
                "timestamp": self.timestamp()
            }

        self.status = "CONNECTED"
        self.last_check = self.timestamp()

        return {
            "provider": self.name,
            "status": self.status,
            "timestamp": self.last_check
        }


    def health(self):

        return {
            "provider": self.name,
            "status": self.status,
            "last_check": self.last_check
        }


    def normalize_symbol(self, symbol):

        symbol = symbol.upper().replace("/", "")

        mapping = {
            "XAUUSD": None
        }

        return mapping.get(symbol)


    def get_quote(self, symbol):

        finnhub_symbol = self.normalize_symbol(symbol)

        if finnhub_symbol is None:

            return {

                "provider": self.name,

                "symbol": symbol,

                "status": "NOT SUPPORTED",

                "message":
                "Finnhub does not provide direct XAU/USD spot quotes."

            }

        try:

            response = requests.get(

                f"{self.base_url}/quote",

                params={

                    "symbol": finnhub_symbol,

                    "token": self.api_key

                },

                timeout=15

            )

            data = response.json()

            return {

                "provider": self.name,

                "symbol": finnhub_symbol,

                "price": data.get("c"),

                "open": data.get("o"),

                "high": data.get("h"),

                "low": data.get("l"),

                "previous_close": data.get("pc"),

                "timestamp": self.timestamp()

            }

        except Exception as e:

            return {

                "provider": self.name,

                "status": "ERROR",

                "error": str(e)

            }


    def get_market_news(self, category="general"):

        try:

            response = requests.get(

                f"{self.base_url}/news",

                params={

                    "category": category,

                    "token": self.api_key

                },

                timeout=20

            )

            data = response.json()

            return {

                "provider": self.name,

                "status": "SUCCESS",

                "articles": len(data),

                "news": data[:10],

                "timestamp": self.timestamp()

            }

        except Exception as e:

            return {

                "provider": self.name,

                "status": "ERROR",

                "error": str(e)

            }


if __name__ == "__main__":

    print("==============================")
    print("GSIS FINNHUB PROVIDER TEST")
    print("==============================")

    provider = GSISFinnhubProvider()

    print(provider.connect())

    print(provider.health())

    print(provider.get_quote("XAUUSD"))

    print(provider.get_market_news())
