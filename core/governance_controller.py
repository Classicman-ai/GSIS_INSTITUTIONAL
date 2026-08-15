"""
=========================================================
GSIS INSTITUTIONAL

INSTITUTIONAL GOVERNANCE CONTROLLER (IGC)

Version: 1.0

Functions:
- Combine system intelligence
- Authorize operation
- Control system mode

=========================================================
"""


from datetime import datetime



class GovernanceController:


    def __init__(self):


        self.name = "Institutional Governance Controller"

        self.status = "CREATED"

        self.mode = "UNKNOWN"



    def initialize(self):


        self.status = "ONLINE"


        print("==============================")

        print(
            "GOVERNANCE CONTROLLER ONLINE"
        )

        print("==============================")



    def evaluate(
            self,
            health_grade,
            reliability_grade,
            audit_status="PASS"):



        decision = "AUTHORIZED"

        mode = "NORMAL"



        if audit_status != "PASS":


            decision = "HALTED"

            mode = "SAFE_MODE"



        elif health_grade == "F" or reliability_grade == "F":


            decision = "HALTED"

            mode = "SAFE_MODE"



        elif health_grade == "C":


            decision = "RESTRICTED"

            mode = "LIMITED"



        elif health_grade == "B":


            decision = "MONITORED"

            mode = "REDUCED"



        elif health_grade == "B+":


            decision = "AUTHORIZED"

            mode = "MONITOR"



        else:


            decision = "AUTHORIZED"

            mode = "NORMAL"



        self.mode = mode



        return {


            "timestamp":
            str(datetime.utcnow()),


            "governance":
            decision,


            "system_mode":
            mode,


            "health":
            health_grade,


            "reliability":
            reliability_grade,


            "audit":
            audit_status

        }



    def status_report(self):


        return {


            "controller":
            self.name,


            "status":
            self.status,


            "mode":
            self.mode

        }
