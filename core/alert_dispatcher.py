"""
=========================================================
GSIS INSTITUTIONAL

ALERT DISPATCHER ENGINE (ADE)

Version: 1.0

Functions:
- Process classified events
- Generate alerts
- Manage alert priority
- Store alert history

=========================================================
"""


from datetime import datetime
import uuid



class AlertDispatcher:


    def __init__(self):


        self.name = "Alert Dispatcher Engine"

        self.status = "CREATED"

        self.alerts = []



    def initialize(self):


        self.status = "ONLINE"


        print("==============================")

        print(
            "ALERT DISPATCHER ONLINE"
        )

        print("==============================")



    def process_event(
            self,
            event):


        severity = event.get(
            "severity",
            "INFO"
        )


        if severity == "INFO":

            return None



        alert = {


            "alert_id":
            str(uuid.uuid4()),


            "level":
            severity,


            "event":
            event.get(
                "type"
            ),


            "time":
            str(datetime.utcnow()),


            "data":
            event.get(
                "data"
            )

        }



        self.alerts.append(
            alert
        )


        self.display_alert(
            alert
        )


        return alert



    def display_alert(
            self,
            alert):


        print("==============================")

        print(
            "GSIS ALERT"
        )

        print(
            "LEVEL:",
            alert["level"]
        )

        print(
            "EVENT:",
            alert["event"]
        )

        print(
            "TIME:",
            alert["time"]
        )

        print("==============================")



    def history(self):


        return self.alerts
