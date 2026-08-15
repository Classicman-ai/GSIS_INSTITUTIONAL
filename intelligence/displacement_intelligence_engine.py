"""
=========================================================
GSIS INSTITUTIONAL

DISPLACEMENT INTELLIGENCE ENGINE

Version 2.0

Institutional Momentum Measurement System

=========================================================
"""


from datetime import datetime



class DisplacementIntelligenceEngine:



    def __init__(self):

        self.name = "Displacement Intelligence Engine"

        self.status = "CREATED"

        self.history = []





    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("DISPLACEMENT INTELLIGENCE ENGINE ONLINE")
        print("==============================")





    def analyze(self, candles):


        if len(candles) < 2:

            return None



        previous = candles[-2]

        current = candles[-1]



        body = abs(
            current["close"]
            -
            current["open"]
        )


        candle_range = abs(
            current["high"]
            -
            current["low"]
        )


        wick_ratio = self.calculate_body_ratio(
            body,
            candle_range
        )


        expansion = self.calculate_expansion(
            current,
            previous
        )


        velocity = self.calculate_velocity(
            current,
            previous
        )


        score = (
            wick_ratio +
            expansion +
            velocity
        )


        score = min(
            score,
            100
        )



        result = {


            "timestamp":
            str(datetime.utcnow()),


            "score":
            round(score,2),


            "classification":
            self.classify(score),


            "body_ratio":
            round(wick_ratio,2),


            "expansion":
            round(expansion,2),


            "velocity":
            round(velocity,2)

        }



        self.history.append(result)


        return result






    def calculate_body_ratio(
            self,
            body,
            candle_range):


        if candle_range == 0:

            return 0


        return (
            body /
            candle_range
        ) * 40






    def calculate_expansion(
            self,
            current,
            previous):


        current_range = (
            current["high"]
            -
            current["low"]
        )


        previous_range = (
            previous["high"]
            -
            previous["low"]
        )


        if previous_range == 0:

            return 0


        ratio = (
            current_range /
            previous_range
        )


        return min(
            ratio * 30,
            30
        )






    def calculate_velocity(
            self,
            current,
            previous):


        movement = abs(
            current["close"]
            -
            previous["close"]
        )


        return min(
            movement * 30,
            30
        )






    def classify(self, score):


        if score >= 90:

            return "INSTITUTIONAL DISPLACEMENT"


        elif score >= 75:

            return "STRONG DISPLACEMENT"


        elif score >= 50:

            return "MODERATE DISPLACEMENT"


        elif score >= 25:

            return "WEAK DISPLACEMENT"


        return "NO DISPLACEMENT"






    def latest(self):

        if self.history:

            return self.history[-1]


        return None
