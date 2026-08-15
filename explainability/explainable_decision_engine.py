"""
=========================================================
GSIS INSTITUTIONAL

EXPLAINABLE DECISION &
TRANSPARENCY INTELLIGENCE ENGINE

Version 1.0

Decision Reasoning Layer

=========================================================
"""


from datetime import datetime
import uuid



class ExplainableDecisionEngine:


    def __init__(self):

        self.name = "Explainable Decision Engine"

        self.status = "CREATED"

        self.decisions = []

        self.evidence = []

        self.audit_records = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("EXPLAINABLE DECISION ENGINE ONLINE")
        print("==============================")





    def record_decision(
            self,
            action,
            confidence,
            reasons):


        decision = {


            "id":

            str(uuid.uuid4()),


            "action":

            action,


            "confidence":

            confidence,


            "reasons":

            reasons,


            "time":

            str(datetime.utcnow())

        }



        self.decisions.append(decision)


        return decision






    def add_evidence(
            self,
            source,
            contribution):


        data = {


            "source":

            source,


            "contribution":

            contribution,


            "time":

            str(datetime.utcnow())

        }



        self.evidence.append(data)


        return data






    def create_audit(
            self,
            event,
            explanation):


        audit = {


            "event":

            event,


            "explanation":

            explanation,


            "time":

            str(datetime.utcnow())

        }



        self.audit_records.append(audit)


        return audit






    def explainability_report(self):


        return {


            "status":

            self.status,


            "decisions":

            len(self.decisions),


            "evidence":

            len(self.evidence),


            "audits":

            len(self.audit_records)

        }
