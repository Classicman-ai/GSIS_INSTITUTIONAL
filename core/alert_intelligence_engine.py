"""
=========================================================
GSIS INSTITUTIONAL

ALERT INTELLIGENCE ENGINE

Version 1.0

Institutional Notification Intelligence Layer

=========================================================
"""


from datetime import datetime



class AlertIntelligenceEngine:


    def __init__(self):

        self.name = "Alert Intelligence Engine"

        self.status = "CREATED"

        self.alerts = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("ALERT INTELLIGENCE ENGINE ONLINE")
        print("==============================")





    def create_alert(
            self,
            alert_type,
            data):


        priority = self.calculate_priority(
            alert_type,
            data
        )


        alert = {


            "timestamp":

            str(datetime.utcnow()),


            "type":

            alert_type,


            "priority":

            priority,


            "data":

            data,


            "status":

            "NEW"

        }



        self.alerts.append(alert)


        return alert






    def calculate_priority(
            self,
            alert_type,
            data):


        if alert_type == "SYSTEM_FAILURE":

            return "CRITICAL"



        if alert_type == "TRADE_SIGNAL":


            confidence = data.get(
                "confidence",
                0
            )


            if confidence >= 85:

                return "HIGH"


            return "MEDIUM"




        if alert_type == "RISK_WARNING":

            return "HIGH"



        return "LOW"






    def acknowledge(
            self,
            alert_id):


        if alert_id < len(self.alerts):

            self.alerts[alert_id]["status"] = "ACKNOWLEDGED"


            return self.alerts[alert_id]



        return None






    def latest(self):


        if self.alerts:

            return self.alerts[-1]


        return None
