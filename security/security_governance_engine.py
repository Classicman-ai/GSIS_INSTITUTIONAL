"""
=========================================================

GSIS INSTITUTIONAL

SECURITY, GOVERNANCE &
AUDIT COMPLIANCE ENGINE

Version 1.0

Control Layer

=========================================================
"""


from datetime import datetime
import uuid



class SecurityGovernanceEngine:


    def __init__(self):

        self.name = "Security Governance Engine"

        self.status = "CREATED"

        self.users = []

        self.rules = []

        self.audit_logs = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("SECURITY GOVERNANCE ENGINE ONLINE")
        print("==============================")





    def register_user(
            self,
            username,
            role):


        user = {

            "id":
            str(uuid.uuid4()),

            "username":
            username,

            "role":
            role,

            "time":
            str(datetime.utcnow())

        }


        self.users.append(user)


        return user






    def add_rule(
            self,
            rule):


        self.rules.append(rule)


        return rule






    def create_audit(
            self,
            action,
            source,
            result):


        log = {


            "action":
            action,


            "source":
            source,


            "result":
            result,


            "time":
            str(datetime.utcnow())

        }


        self.audit_logs.append(log)


        return log






    def security_report(self):


        return {


            "status":
            self.status,


            "users":
            len(self.users),


            "rules":
            len(self.rules),


            "audit_events":
            len(self.audit_logs)

        }
