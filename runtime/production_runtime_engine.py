"""
=========================================================

GSIS INSTITUTIONAL

PRODUCTION RUNTIME ENGINE

Version 1.0

Continuous Operation Layer

=========================================================
"""


from datetime import datetime
import uuid
import time



class ProductionRuntimeEngine:


    def __init__(self):

        self.name = "Production Runtime Engine"

        self.status = "CREATED"

        self.services = []

        self.logs = []

        self.running = False





    def initialize(self):

        self.status = "ONLINE"

        self.log_event(
            "Runtime initialized"
        )


        print("==============================")
        print("PRODUCTION RUNTIME ENGINE ONLINE")
        print("==============================")





    def register_service(
            self,
            service):


        data = {

            "id":
            str(uuid.uuid4()),

            "service":
            service,

            "status":
            "REGISTERED",

            "time":
            str(datetime.utcnow())

        }


        self.services.append(data)


        return data






    def start_service(
            self,
            service):


        event = {


            "service":
            service,


            "action":
            "STARTED",


            "time":
            str(datetime.utcnow())

        }


        self.logs.append(event)


        return event






    def stop_service(
            self,
            service):


        event = {


            "service":
            service,


            "action":
            "STOPPED",


            "time":
            str(datetime.utcnow())

        }


        self.logs.append(event)


        return event






    def log_event(
            self,
            message):


        self.logs.append({

            "message":
            message,

            "time":
            str(datetime.utcnow())

        })






    def run(self):

        self.running = True

        self.status = "RUNNING"


        while self.running:

            time.sleep(1)





    def runtime_report(self):


        return {


            "status":
            self.status,


            "services":
            len(self.services),


            "logs":
            len(self.logs)

        }
