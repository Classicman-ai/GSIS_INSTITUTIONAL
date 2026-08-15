"""
=========================================================
GSIS INSTITUTIONAL
FEATURE ENGINE
Version: 2.0

Market State Feature Extraction
=========================================================
"""


import math



class FeatureEngine:


    def __init__(self):

        self.name = "Feature Engine"

        self.status = "CREATED"



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("GSIS FEATURE ENGINE ONLINE")
        print("==============================")



    def calculate_features(
            self,
            statistics):


        if not statistics:

            return None



        close = statistics.get(
            "close",
            0
        )


        return_pct = statistics.get(
            "return_pct",
            0
        )


        volatility = statistics.get(
            "volatility",
            0
        )


        # Basic market classification

        if return_pct > 0:

            direction = "BULLISH"

        elif return_pct < 0:

            direction = "BEARISH"

        else:

            direction = "NEUTRAL"



        # Volatility state

        if volatility == 0:

            volatility_state = "LOW"


        elif volatility > 5:

            volatility_state = "HIGH"


        else:

            volatility_state = "NORMAL"



        features = {


            "close":

            close,


            "return_pct":

            return_pct,


            "volatility":

            volatility,


            "direction":

            direction,


            "volatility_state":

            volatility_state



        }


        return features



    def update(
            self,
            statistics):


        features = self.calculate_features(
            statistics
        )


        if features:

            print(
                "FEATURES:",
                features
            )


        return features



    def shutdown(self):

        self.status = "OFFLINE"

        print(
            "FEATURE ENGINE STOPPED"
        )
