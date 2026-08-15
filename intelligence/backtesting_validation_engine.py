"""
=========================================================
GSIS INSTITUTIONAL

MODEL VALIDATION & BACKTESTING INTELLIGENCE ENGINE

Version 1.0

Scientific Testing Laboratory Layer

=========================================================
"""


from datetime import datetime



class BacktestingValidationEngine:


    def __init__(self):

        self.name = "Backtesting Validation Engine"

        self.status = "CREATED"

        self.tests = []

        self.metrics = []

        self.optimizations = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("BACKTESTING VALIDATION ENGINE ONLINE")
        print("==============================")





    def create_test(
            self,
            model,
            period):


        test = {


            "model":

            model,


            "period":

            period,


            "status":

            "CREATED",


            "time":

            str(datetime.utcnow())

        }



        self.tests.append(test)


        return test






    def record_metric(
            self,
            metric,
            value):


        data = {


            "metric":

            metric,


            "value":

            value,


            "time":

            str(datetime.utcnow())

        }



        self.metrics.append(data)


        return data






    def optimize_parameter(
            self,
            parameter,
            value):


        result = {


            "parameter":

            parameter,


            "optimal_value":

            value,


            "time":

            str(datetime.utcnow())

        }



        self.optimizations.append(result)


        return result






    def validation_report(self):


        return {


            "status":

            self.status,


            "tests":

            len(self.tests),


            "metrics":

            len(self.metrics),


            "optimizations":

            len(self.optimizations)

        }
