"""
=========================================================
GSIS INSTITUTIONAL

PORTFOLIO INTELLIGENCE & ASSET ALLOCATION ENGINE
Version: 1.0

Institutional Portfolio Control Layer

Controls:
- Asset exposure
- Capital allocation
- Correlation awareness
- Portfolio risk

=========================================================
"""


class PortfolioEngine:


    def __init__(self):

        self.name = "Portfolio Intelligence Engine"

        self.status = "CREATED"


        self.assets = {}


        self.max_exposure = {


            "XAUTUSDT": 0.40,

            "BTCUSDT": 0.30,

            "EURUSD": 0.20,

            "GBPUSD": 0.20,

            "US500": 0.30,

            "NAS100": 0.30

        }



    def initialize(self):

        self.status = "ONLINE"


        print("==============================")

        print(
            "PORTFOLIO INTELLIGENCE ENGINE ONLINE"
        )

        print("==============================")



    def register_asset(
            self,
            symbol,
            allocation):


        self.assets[symbol] = {


            "allocation":

            allocation,


            "status":

            "ACTIVE"

        }


        return self.assets[symbol]



    def check_exposure(
            self,
            symbol,
            exposure):


        limit = self.max_exposure.get(

            symbol,

            0.10

        )


        if exposure > limit:


            return {


                "status":

                "BLOCKED",


                "reason":

                "EXPOSURE LIMIT EXCEEDED"

            }



        return {


            "status":

            "APPROVED",


            "remaining":

            limit - exposure

        }



    def allocate_capital(
            self,
            account_balance,
            symbol,
            percentage):


        allocation = (

            account_balance *

            percentage

            /

            100

        )


        return {


            "symbol":

            symbol,


            "allocation":

            round(
                allocation,
                2
            )

        }



    def portfolio_summary(self):


        return {


            "assets":

            self.assets,


            "status":

            self.status

        }



    def shutdown(self):

        self.status = "OFFLINE"


        print(
            "PORTFOLIO ENGINE STOPPED"
        )
