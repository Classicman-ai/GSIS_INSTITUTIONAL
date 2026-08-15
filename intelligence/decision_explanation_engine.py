"""
=========================================================
GSIS INSTITUTIONAL

DECISION EXPLANATION & TRANSPARENCY
INTELLIGENCE ENGINE

Version 1.0

Explainable AI Layer

=========================================================
"""


from datetime import datetime
import uuid



class DecisionExplanationEngine:


    def __init__(self):

        self.name = "Decision Explanation Engine"

        self.status = "CREATED"

        self.explanations = []

        self.factors = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("DECISION EXPLANATION ENGINE ONLINE")
        print("==============================")





    def create_explanation(
            self,
            decision,
            confidence,
            reasons):


        explanation = {


            "id":

            str(uuid.uuid4()),


            "decision":

            decision,


            "confidence":

            confidence,


            "reasons":

            reasons,


            "time":

            str(datetime.utcnow())

        }



        self.explanations.append(explanation)


        return explanation






    def add_factor(
            self,
            factor,
            contribution):


        data = {


            "factor":

            factor,


            "contribution":

            contribution,


            "time":

            str(datetime.utcnow())

        }



        self.factors.append(data)


        return data






    def generate_summary(
            self,
            explanation):


        return {


            "summary":

            f"Decision {explanation['decision']} generated with confidence {explanation['confidence']} based on analyzed market factors.",


            "timestamp":

            explanation["time"]

        }






    def explanation_report(self):


        return {


            "status":

            self.status,


            "explanations":

            len(self.explanations),


            "factors":

            len(self.factors)

        }
