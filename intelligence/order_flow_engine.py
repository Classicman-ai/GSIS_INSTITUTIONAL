"""
=========================================================
GSIS INSTITUTIONAL

ORDER FLOW INTELLIGENCE ENGINE

Version 1.0

Institutional Market Microstructure Layer

=========================================================
"""


from datetime import datetime



class OrderFlowEngine:


    def __init__(self):

        self.name = "Order Flow Intelligence Engine"

        self.status = "CREATED"

        self.history = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("ORDER FLOW INTELLIGENCE ENGINE ONLINE")
        print("==============================")





    def analyze(
            self,
            candle_data):


        volume = candle_data.get(
            "volume",
            0
        )


        buy_volume = candle_data.get(
            "buy_volume",
            0
        )


        sell_volume = candle_data.get(
            "sell_volume",
            0
        )


        price_change = candle_data.get(
            "price_change",
            0
        )



        total = buy_volume + sell_volume



        if total > 0:


            buy_pressure = (

                buy_volume / total

            ) * 100


            sell_pressure = (

                sell_volume / total

            ) * 100



        else:


            buy_pressure = 50

            sell_pressure = 50





        condition = "BALANCED"



        if buy_pressure > 65:

            condition = "BUY_DOMINANCE"



        elif sell_pressure > 65:

            condition = "SELL_DOMINANCE"





        absorption = False



        if volume > 0 and abs(price_change) < 0.1:


            absorption = True





        report = {


            "timestamp":

            str(datetime.utcnow()),


            "buy_pressure":

            round(
                buy_pressure,
                2
            ),


            "sell_pressure":

            round(
                sell_pressure,
                2
            ),


            "condition":

            condition,


            "absorption":

            absorption

        }



        self.history.append(
            report
        )


        return report






    def latest(self):


        if self.history:

            return self.history[-1]


        return None
