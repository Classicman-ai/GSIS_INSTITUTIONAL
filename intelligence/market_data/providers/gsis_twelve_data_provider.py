import os
import requests
import datetime

from dotenv import load_dotenv

from intelligence.market_data.gsis_provider_base import (
    GSISProviderBase
)


class GSISTwelveDataProvider(GSISProviderBase):


    def __init__(self):

        super().__init__(
            "TWELVE_DATA"
        )

        load_dotenv(
            dotenv_path=".env"
        )

        self.api_key = os.getenv(
            "TWELVE_DATA_API_KEY"
        )

        self.base_url = (
            "https://api.twelvedata.com"
        )


        print("==============================")
        print("GSIS TWELVE DATA PROVIDER v2.0 ONLINE")
        print("LIVE MARKET DATA ENGINE ACTIVE")
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

            "status": "CONNECTED",

            "timestamp": self.last_check

        }





    def health(self):


        return {

            "provider": self.name,

            "status": self.status,

            "last_check": self.last_check

        }





    def normalize_symbol(
        self,
        symbol
    ):


        symbol = symbol.upper()


        if symbol == "XAUUSD":

            return "XAU/USD"


        return symbol





    def get_quote(
        self,
        symbol
    ):


        if not self.api_key:


            return {

                "provider": self.name,

                "status": "API KEY MISSING"

            }




        symbol = self.normalize_symbol(
            symbol
        )



        try:


            response = requests.get(

                f"{self.base_url}/price",

                params={

                    "symbol": symbol,

                    "apikey": self.api_key

                },

                timeout=15

            )



            data = response.json()



            if "price" not in data:


                return {

                    "provider": self.name,

                    "symbol": symbol,

                    "status": "PRICE UNAVAILABLE",

                    "response": data

                }




            return {


                "provider": self.name,


                "symbol": symbol,


                "price": float(

                    data["price"]

                ),


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
    print("GSIS TWELVE DATA TEST")
    print("==============================")


    provider = GSISTwelveDataProvider()


    print(

        provider.connect()

    )


    print(

        provider.health()

    )


    print(

        provider.get_quote(
            "XAUUSD"
        )

    )
