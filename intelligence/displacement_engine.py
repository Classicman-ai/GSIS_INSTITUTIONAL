"""
=========================================================
GSIS INSTITUTIONAL

DISPLACEMENT INTELLIGENCE MEASUREMENT ENGINE (DIME)

Version: 1.0

Functions:
- Measure price displacement
- Classify impulse strength
- Detect institutional movement quality

=========================================================
"""


from datetime import datetime
import uuid



class DisplacementEngine:


    def __init__(self):

        self.name = "Displacement Intelligence Measurement Engine"

        self.status = "CREATED"

        self.history = []



    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("DISPLACEMENT ENGINE ONLINE")
        print("==============================")



    def analyze(
            self,
            candle,
            previous_candle=None):


        high = candle["high"]

        low = candle["low"]

        open_price = candle["open"]

        close = candle["close"]



        total_range = high - low


        body = abs(
            close - open_price
        )


        if total_range == 0:

            body_ratio = 0

        else:

            body_ratio = (
                body / total_range
            ) * 100



        expansion = self.measure_expansion(
            candle,
            previous_candle
        )



        score = (

            body_ratio * 0.5

            +

            expansion * 0.5

        )


        score = round(
            min(score,100),
            2
        )



        classification = self.classify(
            score
        )



        direction = "BULLISH"


        if close < open_price:

            direction = "BEARISH"



        result = {


            "displacement_id":

            str(uuid.uuid4()),


            "timestamp":

            str(datetime.utcnow()),


            "direction":

            direction,


            "body_ratio":

            round(
                body_ratio,
                2
            ),


            "expansion":

            round(
                expansion,
                2
            ),


            "score":

            score,


            "classification":

            classification


        }



        self.history.append(
            result
        )


        return result



    def measure_expansion(
            self,
            candle,
            previous):


        if previous is None:

            return 0



        current_range = (

            candle["high"]

            -

            candle["low"]

        )


        previous_range = (

            previous["high"]

            -

            previous["low"]

        )


        if previous_range == 0:

            return 0



        expansion = (

            current_range /

            previous_range

        ) * 100



        return min(
            expansion,
            100
        )



    def classify(
            self,
            score):


        if score >= 90:

            return "EXPLOSIVE DISPLACEMENT"


        elif score >= 75:

            return "INSTITUTIONAL DISPLACEMENT"


        elif score >= 60:

            return "STRONG DISPLACEMENT"


        elif score >= 40:

            return "NORMAL MOVEMENT"


        else:

            return "WEAK MOVEMENT"



    def report(self):

        return self.history
