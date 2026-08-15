"""
=========================================================
GSIS INSTITUTIONAL
CONFIDENCE CLASSIFICATION ENGINE
Version: 1.0

A+ / A / B / WEAK Signal Ranking
=========================================================
"""


class ConfidenceClassifier:


    def __init__(self):

        self.name = "Confidence Classifier"

        self.status = "CREATED"



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("CONFIDENCE CLASSIFIER ONLINE")
        print("==============================")



    def calculate_score(
            self,
            evidence):


        score = 0



        # Bayesian probability

        probability = evidence.get(
            "probability",
            0
        )


        if probability >= 80:

            score += 30


        elif probability >= 65:

            score += 20


        elif probability >= 50:

            score += 10



        # Pattern similarity

        similarity = evidence.get(
            "similarity",
            0
        )


        if similarity >= 85:

            score += 25


        elif similarity >= 70:

            score += 15



        # Regime confirmation

        regime = evidence.get(
            "regime",
            "UNKNOWN"
        )


        if regime != "UNKNOWN":

            score += 15



        # Event risk

        event_risk = evidence.get(
            "event_risk",
            False
        )


        if event_risk:

            score -= 20


        else:

            score += 10



        # Risk reward

        rr = evidence.get(
            "risk_reward",
            0
        )


        if rr >= 3:

            score += 20


        elif rr >= 2:

            score += 10



        return score



    def classify(
            self,
            evidence):


        score = self.calculate_score(
            evidence
        )



        if score >= 85:

            grade = "A+"


        elif score >= 70:

            grade = "A"


        elif score >= 50:

            grade = "B"


        else:

            grade = "WEAK"



        return {

            "score":
            score,

            "grade":
            grade

        }
