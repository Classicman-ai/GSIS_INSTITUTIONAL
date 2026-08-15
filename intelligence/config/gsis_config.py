import os
from dotenv import load_dotenv
from datetime import datetime, timezone


load_dotenv(".env")


class GSISConfig:

    def __init__(self):

        self.timestamp = datetime.now(
            timezone.utc
        ).isoformat()

        self.keys = {

            "ALPHA_VANTAGE_API_KEY":
                os.getenv("ALPHA_VANTAGE_API_KEY"),

            "TWELVE_DATA_API_KEY":
                os.getenv("TWELVE_DATA_API_KEY"),

            "FINNHUB_API_KEY":
                os.getenv("FINNHUB_API_KEY"),

            "FMP_API_KEY":
                os.getenv("FMP_API_KEY"),

            "NEWS_API_KEY":
                os.getenv("NEWS_API_KEY")

        }


    def status(self):

        return {

            key: "AVAILABLE"
            if value
            else "MISSING"

            for key, value
            in self.keys.items()

        }


    def get(self, key):

        return self.keys.get(key)


    def health(self):

        return {

            "engine":
                "GSIS CONFIGURATION ENGINE",

            "status":
                "READY",

            "timestamp":
                self.timestamp,

            "keys":
                self.status()

        }


config = GSISConfig()


if __name__ == "__main__":

    print("==============================")
    print("GSIS CONFIGURATION ENGINE v2.0")
    print("==============================")

    print(config.health())
