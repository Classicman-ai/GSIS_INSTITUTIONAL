"""
=========================================================
GSIS INSTITUTIONAL

INSTITUTIONAL MARKET MICROSTRUCTURE ENGINE
Version: 1.0

Analyzes:
- Price pressure
- Liquidity voids
- Absorption
- Market participation

=========================================================
"""


class MicrostructureEngine:


    def __init__(self):

        self.name = "Institutional Microstructure Engine"

        self.status = "CREATED"

        self.previous_price = None



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")

        print(
            "MICROSTRUCTURE ENGINE ONLINE"
        )

        print("==============================")



    def analyze(self, market_data):


        if not market_data:

            return None



        price = market_data.get(
            "price"
        )


        result = {


            "price":

            price,


            "pressure":

            "NEUTRAL",


            "liquidity_void":

            False,


            "absorption":

            False

        }



        if self.previous_price:


            change = (

                price -

                self.previous_price

            )



            if change > 0:


                result["pressure"] = "BUYING"



            elif change < 0:


                result["pressure"] = "SELLING"



            movement = abs(change)



            if movement > 20:


                result["liquidity_void"] = True



        self.previous_price = price


        return result



    def detect_absorption(
            self,
            pressure,
            price_change):


        if pressure == "BUYING" and price_change <= 0:


            return True



        if pressure == "SELLING" and price_change >= 0:


            return True



        return False



    def shutdown(self):

        self.status = "OFFLINE"


        print(
            "MICROSTRUCTURE ENGINE STOPPED"
        )
