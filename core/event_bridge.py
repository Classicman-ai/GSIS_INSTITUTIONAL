"""
=========================================================
GSIS INSTITUTIONAL

EVENT INTELLIGENCE BRIDGE (EIB)

Version 1.0

Connects Communication Bus
with Pipeline Controller

=========================================================
"""


from datetime import datetime



class EventIntelligenceBridge:



    def __init__(
            self,
            communication_bus,
            pipeline_controller):


        self.name = "Event Intelligence Bridge"

        self.bus = communication_bus

        self.pipeline = pipeline_controller

        self.status = "CREATED"





    def initialize(self):


        self.status = "ONLINE"


        print("==============================")
        print("EVENT INTELLIGENCE BRIDGE ONLINE")
        print("==============================")





    def process_event(
            self,
            event_type,
            data):


        if event_type == "MARKET_DATA":


            result = self.pipeline.process_market_data(
                data
            )


            return result



        return {


            "status":
            "IGNORED",


            "event":
            event_type,


            "time":
            str(datetime.utcnow())

        }
