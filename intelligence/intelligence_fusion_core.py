"""
=========================================================
GSIS INSTITUTIONAL

INTELLIGENCE FUSION CORE

Version 1.0

Unified Institutional Market Intelligence Layer

=========================================================
"""


from datetime import datetime



class IntelligenceFusionCore:



    def __init__(self):

        self.name = "Intelligence Fusion Core"

        self.status = "CREATED"

        self.history = []





    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("INTELLIGENCE FUSION CORE ONLINE")
        print("==============================")





    def analyze(self, intelligence):


        score = 0

        factors = []



        # Market Structure

        structure = intelligence.get(
            "market_structure"
        )


        if structure == "BULLISH_STRUCTURE":

            score += 20

            factors.append(
                "Bullish Structure"
            )


        elif structure == "BEARISH_STRUCTURE":

            score -= 20

            factors.append(
                "Bearish Structure"
            )





        # Liquidity

        liquidity = intelligence.get(
            "liquidity_score",
            0
        )


        if liquidity >= 70:

            score += 20

            factors.append(
                "Liquidity Confirmed"
            )





        # Order Block

        order_block = intelligence.get(
            "order_block_quality"
        )


        if order_block == "STRONG OB":

            score += 25

            factors.append(
                "Strong Order Block"
            )


        elif order_block == "IDEAL OB":

            score += 20

            factors.append(
                "Ideal Order Block"
            )





        # Displacement

        displacement = intelligence.get(
            "displacement_score",
            0
        )


        if displacement >= 75:

            score += 20

            factors.append(
                "Strong Displacement"
            )





        # MTF

        mtf = intelligence.get(
            "mtf_alignment"
        )


        if mtf == "ALIGNED":

            score += 15

            factors.append(
                "MTF Alignment"
            )




        result = {


            "timestamp":

            str(datetime.utcnow()),


            "institutional_score":

            score,


            "bias":

            self.bias(score),


            "factors":

            factors,


            "classification":

            self.classify(score)

        }



        self.history.append(result)


        return result






    def bias(self, score):


        if score >= 50:

            return "BUY BIAS"



        elif score <= -50:

            return "SELL BIAS"



        return "NEUTRAL"






    def classify(self, score):


        if score >= 80:

            return "INSTITUTIONAL SETUP"



        elif score >= 50:

            return "VALID SETUP"



        elif score >= 25:

            return "WATCHLIST"



        return "NO SETUP"






    def latest(self):


        if self.history:

            return self.history[-1]


        return None
