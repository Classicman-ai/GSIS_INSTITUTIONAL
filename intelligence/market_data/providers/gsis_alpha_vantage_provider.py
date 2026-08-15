import datetime
import requests

from intelligence.config.gsis_config import config

from intelligence.market_data.gsis_provider_base import (
    GSISProviderBase
)


class GSISAlphaVantageProvider(GSISProviderBase):


    def __init__(self):

        super().__init__(
            "ALPHA_VANTAGE"
        )

        self.api_key = config.get(
            "ALPHA_VANTAGE_API_KEY"
        )

        self.base_url = (
            "https://www.alphavantage.co/query"
        )


        print("==============================")
        print("GSIS ALPHA VANTAGE PROVIDER v6.0 ONLINE")
        print("CENTRAL CONFIG + VALIDATION ENGINE ACTIVE")
        print("==============================")



    def timestamp(self):

        return datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()



    def connect(self):

        if self.api_key:

            self.status = "CONNECTED"

        else:

            self.status = "MISSING_API_KEY"


        self.last_check = self.timestamp()


        return {

            "provider": self.name,

            "status": self.status,

            "timestamp": self.last_check

        }



    def get_quote(
        self,
        symbol="XAUUSD"
    ):

        try:


            if not self.api_key:


                return {

                    "provider": self.name,

                    "symbol": symbol,

                    "status": "MISSING_API_KEY",

                    "price": None,

                    "timestamp": self.timestamp()

                }



            params = {

                "function":
                "TIME_SERIES_DAILY",

                "symbol":
                symbol,

                "outputsize":
                "compact",

                "apikey":
                self.api_key

            }



            response = requests.get(
                self.base_url,
                params=params,
                timeout=20
            )


            data = response.json()



            series = data.get(
                "Time Series (Daily)"
            )



            if not series:


                return {

                    "provider": self.name,

                    "symbol": symbol,

                    "status": "NO_DATA",

                    "message": data,

                    "price": None,

                    "timestamp": self.timestamp()

                }



            latest = sorted(
                series.keys()
            )[-1]


            candle = series[
                latest
            ]



            price = float(
                candle.get(
                    "4. close",
                    0
                )
            )



            if price <= 0:


                return {

                    "provider": self.name,

                    "symbol": symbol,

                    "status": "INVALID_PRICE",

                    "price": None,

                    "timestamp": self.timestamp()

                }



            self.status = "CONNECTED"



            return {

                "provider":
                self.name,

                "symbol":
                symbol,

                "date":
                latest,

                "open":
                float(candle.get("1. open", 0)),

                "high":
                float(candle.get("2. high", 0)),

                "low":
                float(candle.get("3. low", 0)),

                "price":
                price,

                "volume":
                candle.get("5. volume", "0"),

                "status":
                "VALID",

                "timestamp":
                self.timestamp()

            }



        except Exception as error:


            return {

                "provider":
                self.name,

                "symbol":
                symbol,

                "status":
                "ERROR",

                "message":
                str(error),

                "price":
                None,

                "timestamp":
                self.timestamp()

            }



if __name__ == "__main__":


    print("==============================")
    print("GSIS ALPHA VANTAGE TEST")
    print("==============================")


    provider = GSISAlphaVantageProvider()


    print(
        provider.connect()
    )


    print(
        provider.get_quote(
            "XAUUSD"
        )
    )
