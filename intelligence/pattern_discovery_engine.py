"""
=========================================================
GSIS INSTITUTIONAL
PATTERN DISCOVERY ENGINE
Version: 1.0

Automatic Market Pattern Identification
=========================================================
"""


import uuid
from datetime import datetime



class PatternDiscoveryEngine:


    def __init__(self):

        self.name = "Pattern Discovery Engine"

        self.status = "CREATED"



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("PATTERN DISCOVERY ENGINE ONLINE")
        print("==============================")



    def generate_pattern_id(self):

        return (

            "PAT-"

            +

            str(uuid.uuid4())[:8].upper()

        )



    def classify_direction(
            self,
            features):


        return_pct = features.get(

            "return_pct",

            0

        )


        if return_pct > 0:

            return "BULLISH"


        elif return_pct < 0:

            return "BEARISH"


        else:

            return "NEUTRAL"



    def classify_volatility(
            self,
            features):


        volatility = features.get(

            "volatility",

            0

        )


        if volatility > 5:

            return "HIGH_VOLATILITY"


        elif volatility == 0:

            return "LOW_VOLATILITY"


        else:

            return "NORMAL_VOLATILITY"



    def discover(
            self,
            features):


        pattern_id = self.generate_pattern_id()


        pattern = {


            "pattern_id":

            pattern_id,


            "created":

            str(datetime.utcnow()),


            "direction":

            self.classify_direction(

                features

            ),


            "volatility_state":

            self.classify_volatility(

                features

            ),


            "close":

            features.get(

                "close",

                0

            ),


            "return_pct":

            features.get(

                "return_pct",

                0

            )

        }



        return pattern
