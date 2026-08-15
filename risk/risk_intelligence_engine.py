"""
=========================================================
GSIS INSTITUTIONAL

RISK INTELLIGENCE &
CAPITAL PROTECTION ENGINE

Version 1.0

Risk Management Layer

=========================================================
"""


from datetime import datetime
import uuid



class RiskIntelligenceEngine:


    def __init__(self):

        self.name = "Risk Intelligence Engine"

        self.status = "CREATED"

        self.risk_checks = []

        self.exposures = []

        self.alerts = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("RISK INTELLIGENCE ENGINE ONLINE")
        print("==============================")





    def evaluate_trade(
            self,
            symbol,
            risk):


        check = {


            "id":

            str(uuid.uuid4()),


            "symbol":

            symbol,


            "risk":

            risk,


            "status":

            "REVIEWED",


            "time":

            str(datetime.utcnow())

        }



        self.risk_checks.append(check)


        return check






    def record_exposure(
            self,
            symbol,
            amount):


        exposure = {


            "symbol":

            symbol,


            "amount":

            amount,


            "time":

            str(datetime.utcnow())

        }



        self.exposures.append(exposure)


        return exposure






    def create_alert(
            self,
            message,
            severity):


        alert = {


            "message":

            message,


            "severity":

            severity,


            "time":

            str(datetime.utcnow())

        }



        self.alerts.append(alert)


        return alert






    def risk_report(self):


        return {


            "status":

            self.status,


            "risk_checks":

            len(self.risk_checks),


            "exposures":

            len(self.exposures),


            "alerts":

            len(self.alerts)

        }
