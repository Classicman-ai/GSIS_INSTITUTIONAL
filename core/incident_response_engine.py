"""
=========================================================
GSIS INSTITUTIONAL

AUTOMATED INCIDENT RESPONSE ENGINE (AIRE)

Version: 1.0

Functions:
- Detect system incidents
- Select response mode
- Protect trading operations

=========================================================
"""


from datetime import datetime



class IncidentResponseEngine:


    def __init__(self):


        self.name = "Automated Incident Response Engine"

        self.status = "CREATED"

        self.mode = "NORMAL"

        self.incidents = []



    def initialize(self):


        self.status = "ONLINE"


        print("==============================")

        print(
            "INCIDENT RESPONSE ENGINE ONLINE"
        )

        print("==============================")



    def evaluate(
            self,
            health_grade,
            event=None):


        response = "NORMAL"



        if health_grade in ["A+", "A", "B+"]:


            self.mode = "NORMAL"



        elif health_grade in ["B", "C"]:


            self.mode = "DEGRADED"

            response = "REDUCE_RISK"



        else:


            self.mode = "PROTECTION"

            response = "PAUSE_EXECUTION"



        incident = {


            "time":
            str(datetime.utcnow()),


            "health_grade":
            health_grade,


            "event":
            event,


            "response":
            response,


            "mode":
            self.mode

        }


        self.incidents.append(
            incident
        )


        return incident



    def get_status(self):


        return {


            "engine":
            self.name,


            "status":
            self.status,


            "mode":
            self.mode

        }
