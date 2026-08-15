"""
=========================================================
GSIS INSTITUTIONAL

EXECUTION GOVERNOR ENGINE (EGE)

Version: 1.0

Final authorization layer before execution.

=========================================================
"""


from datetime import datetime
import uuid



class ExecutionGovernor:


    def __init__(self):

        self.name = "Execution Governor Engine"

        self.status = "CREATED"

        self.history = []



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("EXECUTION GOVERNOR ONLINE")
        print("==============================")



    def authorize(
            self,
            decision,
            confidence,
            risk_status,
            volatility,
            exposure=0):


        permission = "BLOCK"

        mode = "NONE"



        if decision in [
            "BUY",
            "SELL"
        ]:


            if risk_status == "APPROVED":


                if confidence >= 80:


                    if volatility != "EXTREME":


                        if exposure < 5:


                            permission = "APPROVED"

                            mode = "NORMAL"



        if confidence >= 90:

            mode = "HIGH_CONFIDENCE"



        report = {


            "execution_id":

            str(uuid.uuid4()),


            "timestamp":

            str(datetime.utcnow()),


            "decision":

            decision,


            "confidence":

            confidence,


            "permission":

            permission,


            "execution_mode":

            mode,


            "risk_status":

            risk_status


        }



        self.history.append(report)


        return report



    def emergency_stop(self):

        return {

            "status":

            "EMERGENCY_STOP",

            "permission":

            "BLOCK"

        }



    def report(self):

        return self.history
