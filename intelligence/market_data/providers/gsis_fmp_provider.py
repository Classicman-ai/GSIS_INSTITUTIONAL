import os
import requests

from dotenv import load_dotenv

from intelligence.market_data.gsis_provider_base import GSISProviderBase


class GSISFMPProvider(GSISProviderBase):

    def __init__(self):

        super().__init__("FMP")

        load_dotenv(dotenv_path=".env")

        self.api_key = os.getenv("FMP_API_KEY")

        self.base_url = "https://financialmodelingprep.com/stable"

        print("==============================")
        print("GSIS FMP PROVIDER v1.0 ONLINE")
        print("FINANCIAL DATA ENGINE ACTIVE")
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


    def get_quote(self, symbol):

        return {

            "provider": self.name,

            "symbol": symbol,

            "status": "NOT SUPPORTED",

            "message":
            "FMP is not used as a primary XAU/USD spot price provider."

        }


    def get_company_profile(self, ticker):

        try:

            response = requests.get(

                f"{self.base_url}/profile",

                params={

                    "symbol": ticker,

                    "apikey": self.api_key

                },

                timeout=20

            )

            data = response.json()

            return {

                "provider": self.name,

                "ticker": ticker,

                "profile": data,

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
    print("GSIS FMP PROVIDER TEST")
    print("==============================")

    provider = GSISFMPProvider()

    print(provider.connect())

    print(provider.health())

    print(provider.get_quote("XAUUSD"))

    print(provider.get_company_profile("AAPL"))
