"""
=========================================================
GSIS INSTITUTIONAL

LIQUIDITY MAPPING INTELLIGENCE ENGINE

Version 1.0

Institutional Liquidity Detection Layer

=========================================================
"""


from datetime import datetime



class LiquidityMappingEngine:


    def __init__(self):

        self.name = "Liquidity Mapping Engine"

        self.status = "CREATED"

        self.maps = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("LIQUIDITY MAPPING ENGINE ONLINE")
        print("==============================")





    def analyze(
            self,
            candles):


        liquidity_zones = []


        highs = [

            candle.get("high")

            for candle in candles

        ]


        lows = [

            candle.get("low")

            for candle in candles

        ]



        # Equal highs detection

        for i in range(len(highs)-1):


            if highs[i] == highs[i+1]:


                liquidity_zones.append({

                    "type":

                    "BUY_SIDE_LIQUIDITY",


                    "price":

                    highs[i],


                    "strength":

                    "HIGH"

                })





        # Equal lows detection

        for i in range(len(lows)-1):


            if lows[i] == lows[i+1]:


                liquidity_zones.append({

                    "type":

                    "SELL_SIDE_LIQUIDITY",


                    "price":

                    lows[i],


                    "strength":

                    "HIGH"

                })





        report = {


            "timestamp":

            str(datetime.utcnow()),


            "zones":

            liquidity_zones,


            "count":

            len(liquidity_zones)

        }



        self.maps.append(
            report
        )


        return report






    def latest(self):


        if self.maps:

            return self.maps[-1]


        return None
