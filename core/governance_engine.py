"""
=========================================================
GSIS INSTITUTIONAL

GOVERNANCE & CONTROL INTELLIGENCE ENGINE

Version 1.0

Institutional Authority Layer

=========================================================
"""


from datetime import datetime



class GovernanceEngine:


    def __init__(self):

        self.name = "Governance Engine"

        self.status = "CREATED"

        self.policies = {}

        self.approvals = []

        self.restrictions = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("GOVERNANCE ENGINE ONLINE")
        print("==============================")





    def create_policy(
            self,
            name,
            value):


        self.policies[name] = {


            "value":

            value,


            "created":

            str(datetime.utcnow())

        }



        return self.policies[name]






    def check_policy(
            self,
            name,
            value):


        if name not in self.policies:


            return {

                "status":

                "NO POLICY"

            }



        limit = self.policies[name]["value"]



        if value <= limit:


            return {


                "status":

                "APPROVED"

            }



        return {


            "status":

            "REJECTED"

        }






    def request_approval(
            self,
            action,
            details):


        request = {


            "action":

            action,


            "details":

            details,


            "status":

            "PENDING",


            "time":

            str(datetime.utcnow())

        }



        self.approvals.append(request)


        return request






    def approve_action(
            self,
            index):


        if index < len(self.approvals):


            self.approvals[index]["status"] = "APPROVED"


            return self.approvals[index]



        return None






    def add_restriction(
            self,
            restriction):


        self.restrictions.append(

            restriction

        )


        return restriction






    def governance_report(self):


        return {


            "status":

            self.status,


            "policies":

            len(self.policies),


            "pending_actions":

            len(self.approvals),


            "restrictions":

            len(self.restrictions)

        }
