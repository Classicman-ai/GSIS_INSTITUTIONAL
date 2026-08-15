"""
=========================================================
GSIS INSTITUTIONAL

EVENT CLASSIFICATION ENGINE (ECE)

Version: 1.0

Functions:
- Classify events
- Assign severity
- Generate structured event records

=========================================================
"""


from datetime import datetime
import uuid



class EventClassifier:


    def __init__(self):

        self.name = "Event Classification Engine"

        self.status = "CREATED"

        self.history = []



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("EVENT CLASSIFIER ONLINE")
        print("==============================")



    def classify(
            self,
            event,
            data=None):


        severity = "INFO"


        if "ERROR" in event:

            severity = "HIGH"


        elif "TRADE" in event:

            severity = "WARNING"



        classified = {


            "event_id":
            str(uuid.uuid4()),


            "type":
            event,


            "severity":
            severity,


            "timestamp":
            str(datetime.utcnow()),


            "data":
            data

        }


        self.history.append(
            classified
        )


        return classified



    def get_history(self):

        return self.history
