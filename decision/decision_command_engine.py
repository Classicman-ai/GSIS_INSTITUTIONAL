"""
=========================================================
GSIS INSTITUTIONAL

DECISION COMMAND ORCHESTRATION ENGINE

Version 1.0

Final Decision Authority Layer

=========================================================
"""


from datetime import datetime
import uuid



class DecisionCommandEngine:


    def __init__(self):

        self.name = "Decision Command Engine"

        self.status = "CREATED"

        self.decisions = []

        self.rules = []

        self.audit_log = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("DECISION COMMAND ENGINE ONLINE")
        print("==============================")





    def add_rule(
            self,
            rule):


        self.rules.append(rule)


        return rule






    def evaluate_decision(
            self,
            action,
            confidence,
            reason):


        decision = {


            "id":

            str(uuid.uuid4()),


            "action":

            action,


            "confidence":

            confidence,


            "reason":

            reason,


            "time":

            str(datetime.utcnow())

        }



        self.decisions.append(decision)


        return decision






    def create_audit(
            self,
            decision):


        record = {


            "decision":

            decision,


            "verified":

            True,


            "time":

            str(datetime.utcnow())

        }



        self.audit_log.append(record)


        return record






    def command_report(self):


        return {


            "status":

            self.status,


            "decisions":

            len(self.decisions),


            "rules":

            len(self.rules),


            "audits":

            len(self.audit_log)

        }
