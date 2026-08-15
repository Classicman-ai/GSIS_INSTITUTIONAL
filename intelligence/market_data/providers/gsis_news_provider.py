import os
import requests

from dotenv import load_dotenv

from intelligence.market_data.gsis_provider_base import GSISProviderBase


class GSISNewsProvider(GSISProviderBase):

    def __init__(self):

        super().__init__("NEWS_API")

        load_dotenv(dotenv_path=".env")

        self.api_key = os.getenv("NEWS_API_KEY")

        self.base_url = "https://newsapi.org/v2"

        print("==============================")
        print("GSIS NEWS API PROVIDER v1.0 ONLINE")
        print("GLOBAL NEWS INTELLIGENCE ACTIVE")
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

            "status": "NOT SUPPORTED",

            "message": "News provider does not supply market prices."

        }


    def get_news(self, query="gold", page_size=10):

        try:

            response = requests.get(

                f"{self.base_url}/everything",

                params={

                    "q": query,

                    "language": "en",

                    "sortBy": "publishedAt",

                    "pageSize": page_size,

                    "apiKey": self.api_key

                },

                timeout=20

            )

            response.raise_for_status()

            data = response.json()

            return {

                "provider": self.name,

                "status": "SUCCESS",

                "total_results": data.get("totalResults", 0),

                "articles": data.get("articles", []),

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
    print("GSIS NEWS API PROVIDER TEST")
    print("==============================")

    provider = GSISNewsProvider()

    print(provider.connect())

    print(provider.health())

    print(provider.get_quote("XAUUSD"))

    print(provider.get_news("gold"))
