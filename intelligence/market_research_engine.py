"""
=========================================================
GSIS INSTITUTIONAL

MARKET INTELLIGENCE RESEARCH & DISCOVERY ENGINE

Version 1.0

Institutional Research Layer

=========================================================
"""


from datetime import datetime
import uuid



class MarketResearchEngine:


    def __init__(self):

        self.name = "Market Research Engine"

        self.status = "CREATED"

        self.research_projects = []

        self.discoveries = []

        self.observations = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("MARKET RESEARCH ENGINE ONLINE")
        print("==============================")





    def create_research(
            self,
            title,
            hypothesis):


        project = {


            "id":

            str(uuid.uuid4()),


            "title":

            title,


            "hypothesis":

            hypothesis,


            "status":

            "ACTIVE",


            "time":

            str(datetime.utcnow())

        }



        self.research_projects.append(project)


        return project






    def record_discovery(
            self,
            pattern,
            confidence):


        discovery = {


            "pattern":

            pattern,


            "confidence":

            confidence,


            "time":

            str(datetime.utcnow())

        }



        self.discoveries.append(discovery)


        return discovery






    def record_observation(
            self,
            market_condition,
            finding):


        observation = {


            "condition":

            market_condition,


            "finding":

            finding,


            "time":

            str(datetime.utcnow())

        }



        self.observations.append(observation)


        return observation






    def research_report(self):


        return {


            "status":

            self.status,


            "projects":

            len(self.research_projects),


            "discoveries":

            len(self.discoveries),


            "observations":

            len(self.observations)

        }
