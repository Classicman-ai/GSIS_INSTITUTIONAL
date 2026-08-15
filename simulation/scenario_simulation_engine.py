"""
=========================================================
GSIS INSTITUTIONAL

SCENARIO SIMULATION &
STRESS INTELLIGENCE ENGINE

Version 1.0

Future Testing Layer

=========================================================
"""


from datetime import datetime
import uuid



class ScenarioSimulationEngine:


    def __init__(self):

        self.name = "Scenario Simulation Engine"

        self.status = "CREATED"

        self.scenarios = []

        self.tests = []

        self.results = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("SCENARIO SIMULATION ENGINE ONLINE")
        print("==============================")





    def create_scenario(
            self,
            name,
            description):


        scenario = {


            "id":

            str(uuid.uuid4()),


            "name":

            name,


            "description":

            description,


            "time":

            str(datetime.utcnow())

        }



        self.scenarios.append(scenario)


        return scenario






    def run_test(
            self,
            scenario,
            strategy):


        test = {


            "scenario":

            scenario,


            "strategy":

            strategy,


            "time":

            str(datetime.utcnow())

        }



        self.tests.append(test)


        return test






    def record_result(
            self,
            scenario,
            result):


        data = {


            "scenario":

            scenario,


            "result":

            result,


            "time":

            str(datetime.utcnow())

        }



        self.results.append(data)


        return data






    def simulation_report(self):


        return {


            "status":

            self.status,


            "scenarios":

            len(self.scenarios),


            "tests":

            len(self.tests),


            "results":

            len(self.results)

        }
