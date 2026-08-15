"""
=========================================================
GSIS INSTITUTIONAL
DATA ENGINE
Version: 2.1

Resilient Market Data Layer
=========================================================
"""


import time
from datetime import datetime

from binance.client import Client



class DataEngine:


    def __init__(self):

        self.symbol = "XAUTUSDT"

        self.client = None

        self.connected = False



    def initialize(self):

        print("==============================")
        print("GSIS DATA ENGINE ONLINE")
        print("Asset:", self.symbol)
        print("==============================")


        self.connect()



    def connect(self):

        try:

            self.client = Client()

            self.connected = True

            print(
                "BINANCE DATA CONNECTION ONLINE"
            )


        except Exception as e:

            self.connected = False

            print(
                "BINANCE CONNECTION FAILED:",
                e
            )



    def get_data(self):


        if not self.connected:


            self.connect()


            if not self.connected:

                return None



        try:


            ticker = self.client.get_symbol_ticker(

                symbol=self.symbol

            )


            price = float(

                ticker["price"]

            )


            server_time = self.client.get_server_time()


            market_time = datetime.fromtimestamp(

                server_time["serverTime"] / 1000

            )


            data = {


                "symbol":

                self.symbol,


                "price":

                price,


                "time":

                str(market_time)

            }


            print(

                "DATA:",

                self.symbol,

                "| PRICE:",

                price,

                "| TIME:",

                market_time

            )


            return data



        except Exception as e:


            print(

                "DATA ERROR:",

                e

            )


            self.connected = False


            return None
