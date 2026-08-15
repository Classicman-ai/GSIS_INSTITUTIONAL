"""
=========================================================
GSIS INSTITUTIONAL

EXECUTION INTELLIGENCE ENGINE

Version 1.0

Institutional Execution Quality Controller

=========================================================
"""


from datetime import datetime



class ExecutionIntelligenceEngine:



    def __init__(self):

        self.name = "Execution Intelligence Engine"

        self.status = "CREATED"

        self.history = []





    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("EXECUTION INTELLIGENCE ENGINE ONLINE")
        print("==============================")





    def analyze(self, data):


        confidence = data.get(
            "confidence",
            0
        )


        spread = data.get(
            "spread",
            "NORMAL"
        )


        volatility = data.get(
            "volatility",
            "NORMAL"
        )



        score = 0



        # Signal confidence

        if confidence >= 80:

            score += 40


        elif confidence >= 60:

            score += 25



        # Spread condition

        if spread == "LOW":

            score += 30


        elif spread == "NORMAL":

            score += 20



        # Volatility condition

        if volatility == "NORMAL":

            score += 30


        elif volatility == "HIGH":

            score += 10



        result = {


            "timestamp":

            str(datetime.utcnow()),


            "execution_score":

            score,


            "order_type":

            self.order_type(score),


            "status":

            self.permission(score)

        }



        self.history.append(result)


        return result






    def order_type(self, score):


        if score >= 80:

            return "LIMIT ORDER"


        elif score >= 60:

            return "STOP ORDER"


        else:

            return "WAIT"






    def permission(self, score):


        if score >= 70:

            return "APPROVED"


        elif score >= 50:

            return "CAUTION"


        return "BLOCKED"






    def latest(self):


        if self.history:

            return self.history[-1]


        return None
