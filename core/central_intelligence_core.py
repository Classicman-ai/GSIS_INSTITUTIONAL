"""
=========================================================
GSIS INSTITUTIONAL

CENTRAL INTELLIGENCE
ORCHESTRATION CORE

Version 1.0

System Integration Layer

=========================================================
"""


from datetime import datetime
import uuid



class CentralIntelligenceCore:


    def __init__(self):

        self.name = "Central Intelligence Core"

        self.status = "CREATED"

        self.engines = []

        self.events = []

        self.decisions = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("CENTRAL INTELLIGENCE CORE ONLINE")
        print("==============================")





    def register_engine(
            self,
            name,
            category):


        engine = {


            "id":

            str(uuid.uuid4()),


            "name":

            name,


            "category":

            category,


            "status":

            "ONLINE",


            "time":

            str(datetime.utcnow())

        }



        self.engines.append(engine)


        return engine






    def process_event(
            self,
            event):


        data = {


            "event":

            event,


            "time":

            str(datetime.utcnow())

        }



        self.events.append(data)


        return data






    def create_decision(
            self,
            action,
            confidence):


        decision = {


            "action":

            action,


            "confidence":

            confidence,


            "time":

            str(datetime.utcnow())

        }



        self.decisions.append(decision)


        return decision






    def system_report(self):


        return {


            "status":

            self.status,


            "engines":

            len(self.engines),


            "events":

            len(self.events),


            "decisions":

            len(self.decisions)

        }
