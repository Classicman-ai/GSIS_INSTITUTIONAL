"""
=========================================================

GSIS INSTITUTIONAL

INTEGRATION CORE &
SYSTEM ORCHESTRATION ENGINE

Version 1.0

Central Control Layer

=========================================================
"""


from datetime import datetime
import uuid



class IntegrationCore:


    def __init__(self):

        self.name = "GSIS Integration Core"

        self.status = "CREATED"

        self.engines = []

        self.messages = []

        self.health = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("GSIS INTEGRATION CORE ONLINE")
        print("==============================")





    def register_engine(
            self,
            engine_name,
            category):


        engine = {


            "id":

            str(uuid.uuid4()),


            "engine":

            engine_name,


            "category":

            category,


            "status":

            "REGISTERED",


            "time":

            str(datetime.utcnow())

        }


        self.engines.append(engine)


        return engine






    def send_message(
            self,
            source,
            destination,
            message):


        data = {


            "source":

            source,


            "destination":

            destination,


            "message":

            message,


            "time":

            str(datetime.utcnow())

        }



        self.messages.append(data)


        return data






    def update_health(
            self,
            component,
            status):


        data = {


            "component":

            component,


            "status":

            status,


            "time":

            str(datetime.utcnow())

        }



        self.health.append(data)


        return data






    def system_report(self):


        return {


            "status":

            self.status,


            "engines":

            len(self.engines),


            "messages":

            len(self.messages),


            "health_checks":

            len(self.health)

        }
