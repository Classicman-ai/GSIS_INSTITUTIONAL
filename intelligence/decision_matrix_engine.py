"""
=========================================================
GSIS INSTITUTIONAL

DECISION MATRIX ENGINE

Version 1.0

Institutional Trade Decision Layer

=========================================================
"""


from datetime import datetime



class DecisionMatrixEngine:


    def __init__(self):

        self.name = "Decision Matrix Engine"

        self.status = "CREATED"

        self.history = []




    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("DECISION MATRIX ENGINE ONLINE")
        print("==============================")





    def analyze(self, intelligence):


        score = 0


        reasons = []



        # Market Structure

        structure = intelligence.get(
            "market_structure"
        )


        if structure == "BULLISH_STRUCTURE":

            score += 20

            reasons.append(
                "Bullish market structure"
            )


        elif structure == "BEARISH_STRUCTURE":

            score -= 20

            reasons.append(
                "Bearish market structure"
            )





        # Liquidity

        liquidity = intelligence.get(
            "liquidity_score",
            0
        )


        if liquidity >= 70:

            score += 15

            reasons.append(
                "Liquidity confirmation"
            )





        # Order Block

        order_block = intelligence.get(
            "order_block_quality"
        )


        if order_block == "STRONG OB":

            score += 25

            reasons.append(
                "Strong order block"
            )


        elif order_block == "IDEAL OB":

            score += 20

            reasons.append(
                "Ideal order block"
            )





        # Displacement

        displacement = intelligence.get(
            "displacement_score",
            0
        )


        if displacement >= 75:

            score += 20

            reasons.append(
                "Strong displacement"
            )





        # Risk

        risk = intelligence.get(
            "risk_score",
            100
        )


        if risk < 40:

            score -= 30

            reasons.append(
                "High risk condition"
            )




        decision = self.classify(
            score
        )



        result = {


            "timestamp":

            str(datetime.utcnow()),


            "score":

            score,


            "decision":

            decision,


            "reasons":

            reasons

        }



        self.history.append(result)


        return result






    def classify(self, score):


        if score >= 70:

            return "BUY"


        elif score <= -70:

            return "SELL"


        elif score >= 40:

            return "WATCH BUY"


        elif score <= -40:

            return "WATCH SELL"


        return "WAIT"






    def latest(self):


        if self.history:

            return self.history[-1]


        return None
