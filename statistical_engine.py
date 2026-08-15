"""
=========================================================
GSIS INSTITUTIONAL
STATISTICAL ENGINE
Version: 2.0
Managed Module Architecture
=========================================================
"""

import statistics
import math


class StatisticalEngine:


    def __init__(self):

        self.name = "Statistical Engine"

        self.status = "CREATED"

        self.history = []



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("GSIS STATISTICAL ENGINE ONLINE")
        print("==============================")



    def calculate_return(
            self,
            current,
            previous):


        if previous == 0:

            return 0


        return (

            (current - previous)

            /

            previous

        ) * 100



    def calculate_volatility(
            self,
            prices):


        if len(prices) < 2:

            return 0


        return statistics.stdev(
            prices
        )



    def analyze(
            self,
            candles):


        if not candles:

            return None



        closes = []


        for candle in candles.values():

            closes.append(

                candle["close"]

            )



        latest = closes[-1]


        previous = (

            closes[-2]

            if len(closes) > 1

            else latest

        )



        result = {


            "close":

            latest,


            "return_pct":

            round(

                self.calculate_return(

                    latest,

                    previous

                ),

                5

            ),



            "volatility":

            round(

                self.calculate_volatility(

                    closes

                ),

                5

            ),



            "samples":

            len(closes)


        }



        return result



    def update(
            self,
            candles):


        analysis = self.analyze(
            candles
        )


        if analysis:

            print(
                "STATISTICS:",
                analysis
            )


        return analysis



    def shutdown(self):

        self.status = "OFFLINE"

        print(
            "STATISTICAL ENGINE STOPPED"
        )
