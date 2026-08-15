"""
=========================================================
GSIS INSTITUTIONAL

GOVERNANCE & POLICY CONTROL ENGINE

Version 1.0

Institutional Control Layer

=========================================================
"""


from datetime import datetime



class GovernanceEngine:


    def __init__(self):

        self.name = "Governance Engine"

        self.status = "CREATED"

        self.policies = {

            "max_risk_per_trade": 0.5,

            "max_daily_loss": 2.0,

            "max_positions": 5

        }

        self.emergency_mode = False





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("GOVERNANCE ENGINE ONLINE")
        print("==============================")





    def check_permission(
            self,
            request):


        if self.emergency_mode:


            return {

                "permission":

                "BLOCKED",


                "reason":

                "EMERGENCY MODE ACTIVE"

            }





        risk = request.get(
            "risk",
            0
        )


        positions = request.get(
            "positions",
            0
        )



        if risk > self.policies[
            "max_risk_per_trade"
        ]:


            return {

                "permission":

                "BLOCKED",


                "reason":

                "RISK LIMIT EXCEEDED"

            }





        if positions >= self.policies[
            "max_positions"
        ]:


            return {

                "permission":

                "BLOCKED",


                "reason":

                "POSITION LIMIT REACHED"

            }





        return {

            "permission":

            "APPROVED",

            "timestamp":

            str(datetime.utcnow())

        }






    def activate_emergency_mode(self):


        self.emergency_mode = True


        return {


            "status":

            "EMERGENCY ACTIVE"

        }






    def disable_emergency_mode(self):


        self.emergency_mode = False


        return {


            "status":

            "NORMAL"

        }






    def update_policy(
            self,
            name,
            value):


        self.policies[name] = value


        return self.policies
