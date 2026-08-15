"""
=========================================================
GSIS INSTITUTIONAL

GOVERNANCE INTEGRATION LAYER (GIL)

Version: 1.0

Purpose:
Connect governance decisions
with execution authorization

=========================================================
"""


from datetime import datetime



class GovernanceIntegration:


    def __init__(self):


        self.name = "Governance Integration Layer"

        self.status = "CREATED"



    def initialize(self):


        self.status = "ONLINE"


        print("==============================")

        print(
            "GOVERNANCE INTEGRATION ONLINE"
        )

        print("==============================")



    def authorize_execution(
            self,
            governance_result):


        mode = governance_result.get(
            "system_mode"
        )


        decision = governance_result.get(
            "governance"
        )



        if decision == "HALTED":


            return {


                "execution":
                "BLOCKED",


                "reason":
                "GOVERNANCE HALT",


                "time":
                str(datetime.utcnow())

            }



        elif mode == "LIMITED":


            return {


                "execution":
                "REDUCED",


                "reason":
                "RESTRICTED MODE",


                "time":
                str(datetime.utcnow())

            }



        elif mode == "REDUCED":


            return {


                "execution":
                "CAUTIOUS",


                "reason":
                "REDUCED OPERATION",


                "time":
                str(datetime.utcnow())

            }



        else:


            return {


                "execution":
                "AUTHORIZED",


                "reason":
                "GOVERNANCE APPROVED",


                "time":
                str(datetime.utcnow())

            }
