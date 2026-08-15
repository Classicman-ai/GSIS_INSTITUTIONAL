"""
=========================================================
GSIS INSTITUTIONAL

EXECUTION INTELLIGENCE ENGINE

Version: 1.1

Governance-Aware Execution Layer

Functions:
- Signal authorization
- Governance verification
- Risk protection
- Order decision

=========================================================
"""


from datetime import datetime



class ExecutionEngine:


    def __init__(self):


        self.name = "Execution Intelligence Engine"

        self.status = "CREATED"


        self.allowed_orders = [

            "MARKET",

            "LIMIT",

            "STOP"

        ]


        self.execution_history = []



    def initialize(self):


        self.status = "ONLINE"


        print("==============================")

        print(
            "EXECUTION INTELLIGENCE ENGINE ONLINE"
        )

        print("==============================")



    def authorize(
            self,
            signal,
            governance=None):


        if not signal:


            return {


                "status":
                "REJECTED",


                "reason":
                "NO SIGNAL"

            }



        if governance:


            if governance.get(
                "execution"
            ) == "BLOCKED":


                return {


                    "status":
                    "REJECTED",


                    "reason":
                    "GOVERNANCE BLOCK",


                    "time":
                    str(datetime.utcnow())

                }



        decision = {


            "status":
            "APPROVED",


            "signal":
            signal,


            "time":
            str(datetime.utcnow())

        }



        self.execution_history.append(
            decision
        )


        return decision



    def history(self):


        return self.execution_history
