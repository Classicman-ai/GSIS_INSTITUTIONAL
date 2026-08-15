"""
=========================================================
GSIS INSTITUTIONAL

RISK MANAGEMENT & CAPITAL PROTECTION
INTELLIGENCE ENGINE

Version 1.0

Chief Risk Officer Layer

=========================================================
"""


from datetime import datetime
import uuid



class RiskManagementEngine:


    def __init__(self):

        self.name = "Risk Management Engine"

        self.status = "CREATED"

        self.risk_records = []

        self.exposure_records = []

        self.alerts = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("RISK MANAGEMENT ENGINE ONLINE")
        print("==============================")





    def calculate_risk(
            self,
            symbol,
            capital,
            risk_percent):


        record = {


            "id":

            str(uuid.uuid4()),


            "symbol":

            symbol,


            "capital":

            capital,


            "risk_percent":

            risk_percent,


            "time":

            str(datetime.utcnow())

        }



        self.risk_records.append(record)


        return record






    def record_exposure(
            self,
            asset,
            exposure):


        data = {


            "asset":

            asset,


            "exposure":

            exposure,


            "time":

            str(datetime.utcnow())

        }



        self.exposure_records.append(data)


        return data






    def create_risk_alert(
            self,
            condition,
            action):


        alert = {


            "condition":

            condition,


            "action":

            action,


            "time":

            str(datetime.utcnow())

        }



        self.alerts.append(alert)


        return alert






    def risk_report(self):


        return {


            "status":

            self.status,


            "risk_records":

            len(self.risk_records),


            "exposures":

            len(self.exposure_records),


            "alerts":

            len(self.alerts)

        }
