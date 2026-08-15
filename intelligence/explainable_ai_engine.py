"""
=========================================================
GSIS INSTITUTIONAL

EXPLAINABLE AI DECISION ENGINE

Version 1.0

Decision Transparency Layer

=========================================================
"""


from datetime import datetime



class ExplainableAIEngine:


    def __init__(self):

        self.name = "Explainable AI Decision Engine"

        self.status = "CREATED"

        self.explanations = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("EXPLAINABLE AI ENGINE ONLINE")
        print("==============================")





    def create_explanation(
            self,
            decision,
            evidence,
            risks):


        score = 0


        contributions = []



        for item in evidence:


            weight = item.get(
                "weight",
                0
            )


            score += weight


            contributions.append({

                "source":

                item.get(
                    "source"
                ),


                "impact":

                weight

            })





        confidence = max(
            0,
            min(
                score,
                100
            )
        )





        report = {


            "timestamp":

            str(datetime.utcnow()),


            "decision":

            decision,


            "confidence":

            confidence,


            "evidence":

            contributions,


            "risks":

            risks,


            "explanation":

            self.generate_text(

                decision,

                contributions,

                risks

            )

        }



        self.explanations.append(
            report
        )


        return report






    def generate_text(
            self,
            decision,
            evidence,
            risks):


        return {


            "decision_reason":

            "Decision generated from combined intelligence evidence",


            "evidence_count":

            len(evidence),


            "risk_count":

            len(risks)

        }






    def latest(self):


        if self.explanations:

            return self.explanations[-1]


        return None
