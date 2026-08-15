"""
=========================================================

GSIS INSTITUTIONAL

SYSTEM MONITORING &
HEALTH INTELLIGENCE ENGINE

Version 1.0

Reliability Layer

=========================================================
"""


from datetime import datetime
import uuid



class SystemHealthEngine:


    def __init__(self):

        self.name = "System Health Intelligence Engine"

        self.status = "CREATED"

        self.components = []

        self.alerts = []

        self.reports = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("SYSTEM HEALTH ENGINE ONLINE")
        print("==============================")





    def register_component(
            self,
            component):


        data = {


            "id":

            str(uuid.uuid4()),


            "component":

            component,


            "status":

            "ONLINE",


            "time":

            str(datetime.utcnow())

        }


        self.components.append(data)


        return data






    def create_alert(
            self,
            component,
            issue):


        alert = {


            "component":

            component,


            "issue":

            issue,


            "time":

            str(datetime.utcnow())

        }



        self.alerts.append(alert)


        return alert






    def create_report(
            self,
            status):


        report = {


            "system_status":

            status,


            "time":

            str(datetime.utcnow())

        }


        self.reports.append(report)


        return report






    def health_report(self):


        return {


            "status":

            self.status,


            "components":

            len(self.components),


            "alerts":

            len(self.alerts),


            "reports":

            len(self.reports)

        }
