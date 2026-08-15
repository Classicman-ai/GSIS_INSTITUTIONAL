"""
=========================================================
GSIS INSTITUTIONAL

PERFORMANCE ANALYTICS &
ATTRIBUTION INTELLIGENCE ENGINE

Version 1.0

Measurement Layer

=========================================================
"""


from datetime import datetime
import uuid



class PerformanceAnalyticsEngine:


    def __init__(self):

        self.name = "Performance Analytics Engine"

        self.status = "CREATED"

        self.results = []

        self.attribution = []

        self.reports = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("PERFORMANCE ANALYTICS ENGINE ONLINE")
        print("==============================")





    def record_result(
            self,
            strategy,
            outcome):


        result = {


            "id":

            str(uuid.uuid4()),


            "strategy":

            strategy,


            "outcome":

            outcome,


            "time":

            str(datetime.utcnow())

        }



        self.results.append(result)


        return result






    def attribute_performance(
            self,
            component,
            contribution):


        data = {


            "component":

            component,


            "contribution":

            contribution,


            "time":

            str(datetime.utcnow())

        }



        self.attribution.append(data)


        return data






    def generate_report(
            self,
            title,
            summary):


        report = {


            "title":

            title,


            "summary":

            summary,


            "time":

            str(datetime.utcnow())

        }



        self.reports.append(report)


        return report






    def analytics_report(self):


        return {


            "status":

            self.status,


            "results":

            len(self.results),


            "attribution":

            len(self.attribution),


            "reports":

            len(self.reports)

        }
