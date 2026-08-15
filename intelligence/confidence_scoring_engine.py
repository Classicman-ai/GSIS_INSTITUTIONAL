"""
=========================================================
GSIS INSTITUTIONAL

CONFIDENCE SCORING INTELLIGENCE ENGINE

Version 1.0

Institutional Setup Quality Evaluation

=========================================================
"""


from datetime import datetime



class ConfidenceScoringEngine:



    def __init__(self):

        self.name = "Confidence Scoring Engine"

        self.status = "CREATED"

        self.history = []





    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("CONFIDENCE SCORING ENGINE ONLINE")
        print("==============================")





    def analyze(self, data):


        structure = data.get(
            "market_structure",
            0
        )


        liquidity = data.get(
            "liquidity",
            0
        )


        order_block = data.get(
            "order_block",
            0
        )


        displacement = data.get(
            "displacement",
            0
        )


        mtf = data.get(
            "mtf_alignment",
            0
        )


        risk = data.get(
            "risk",
            0
        )



        score = (

            structure * 0.20 +

            liquidity * 0.20 +

            order_block * 0.20 +

            displacement * 0.15 +

            mtf * 0.15 +

            risk * 0.10

        )



        result = {


            "timestamp":

            str(datetime.utcnow()),


            "confidence":

            round(score,2),


            "classification":

            self.classify(score),


            "execution_permission":

            self.permission(score)

        }



        self.history.append(result)


        return result






    def classify(self, score):


        if score >= 90:

            return "INSTITUTIONAL A+ SETUP"



        elif score >= 75:

            return "HIGH QUALITY SETUP"



        elif score >= 60:

            return "ACCEPTABLE SETUP"



        elif score >= 40:

            return "LOW CONFIDENCE"



        return "NO TRADE"






    def permission(self, score):


        if score >= 75:

            return "APPROVED"



        return "BLOCKED"






    def latest(self):


        if self.history:

            return self.history[-1]


        return None
