"""
=========================================================
GSIS INSTITUTIONAL

ORDER BLOCK QUALITY INTELLIGENCE ENGINE

Version 1.0

Institutional Order Block Classification

=========================================================
"""


from datetime import datetime




class OrderBlockQualityEngine:



    def __init__(self):


        self.name = "Order Block Quality Engine"

        self.status = "CREATED"

        self.order_blocks = []





    def initialize(self):


        self.status = "ONLINE"


        print("==============================")
        print("ORDER BLOCK QUALITY ENGINE ONLINE")
        print("==============================")





    def analyze(self, data):


        ob = {


            "timestamp":
            str(datetime.utcnow()),


            "symbol":
            data.get("symbol"),


            "type":
            self.detect_type(data),


            "score":
            self.calculate_score(data),


            "classification":
            None,


            "status":
            "ACTIVE"

        }



        ob["classification"] = self.classify(
            ob["score"]
        )



        self.order_blocks.append(ob)


        return ob






    def detect_type(self, data):


        direction = data.get(
            "direction",
            "UNKNOWN"
        )


        if direction == "BUY":

            return "BULLISH_ORDER_BLOCK"


        elif direction == "SELL":

            return "BEARISH_ORDER_BLOCK"


        return "UNDEFINED"






    def calculate_score(self, data):


        score = 0



        # Liquidity sweep confirmation

        if data.get(
            "liquidity_sweep",
            False
        ):

            score += 25



        # Structure break

        if data.get(
            "bos",
            False
        ):

            score += 25



        # Displacement

        displacement = data.get(
            "displacement",
            0
        )


        score += min(
            displacement,
            25
        )



        # Freshness

        if data.get(
            "fresh",
            False
        ):

            score += 25



        return score






    def classify(self, score):


        if score >= 90:

            return "STRONG OB"



        elif score >= 70:

            return "IDEAL OB"



        elif score >= 50:

            return "CLASSIC OB"



        elif score >= 30:

            return "WEAK OB"



        else:

            return "INVALID OB"






    def latest(self):


        if self.order_blocks:

            return self.order_blocks[-1]


        return None
