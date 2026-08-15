"""
=========================================================
GSIS INSTITUTIONAL

SYSTEM HEALTH MONITORING &
SELF-DIAGNOSTIC INTELLIGENCE ENGINE

Version 1.0

System Health Layer

=========================================================
"""


from datetime import datetime
import uuid



class SystemHealthEngine:


    def __init__(self):

        self.name = "System Health Engine"

        self.status = "CREATED"

        self.components = []

        self.errors = []

        self.reports = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("SYSTEM HEALTH ENGINE ONLINE")
        print("==============================")





    def register_component(
            self,
            name):


        component = {


            "id":

            str(uuid.uuid4()),


            "name":

            name,


            "status":

            "HEALTHY",


            "time":

            str(datetime.utcnow())

        }



        self.components.append(component)


        return component






    def record_error(
            self,
            component,
            issue,
            severity):


        error = {


            "component":

            component,


            "issue":

            issue,


            "severity":

            severity,


            "time":

            str(datetime.utcnow())

        }



        self.errors.append(error)


        return error






    def generate_report(
            self,
            health_score):


        report = {


            "health_score":

            health_score,


            "components":

            len(self.components),


            "errors":

            len(self.errors),


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


            "errors":

            len(self.errors),


            "reports":

            len(self.reports)

        }
