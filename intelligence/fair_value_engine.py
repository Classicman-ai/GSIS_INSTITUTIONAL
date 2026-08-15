"""
=========================================================
GSIS INSTITUTIONAL

FAIR VALUE & PRICE EFFICIENCY ENGINE

Version 1.0

Institutional Valuation Intelligence Layer

=========================================================
"""


from datetime import datetime



class FairValueEngine:


    def __init__(self):

        self.name = "Fair Value Engine"

        self.status = "CREATED"

        self.history = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("FAIR VALUE ENGINE ONLINE")
        print("==============================")





    def analyze(
            self,
            price_data):


        high = price_data.get(
            "high",
            0
        )


        low = price_data.get(
            "low",
            0
        )


        current = price_data.get(
            "current",
            0
        )



        if high == low:


            midpoint = current


        else:


            midpoint = (

                high + low

            ) / 2





        zone = "FAIR_VALUE"



        if current > midpoint:


            zone = "PREMIUM"



        elif current < midpoint:


            zone = "DISCOUNT"





        distance = abs(

            current - midpoint

        )



        report = {


            "timestamp":

            str(datetime.utcnow()),


            "current_price":

            current,


            "fair_value":

            midpoint,


            "zone":

            zone,


            "distance":

            distance

        }



        self.history.append(
            report
        )


        return report






    def latest(self):


        if self.history:

            return self.history[-1]


        return None
