"""
=========================================================
GSIS INSTITUTIONAL

REAL-TIME DASHBOARD BACKEND ENGINE

Version 1.0

System Visualization Layer

=========================================================
"""


from datetime import datetime



class DashboardBackendEngine:


    def __init__(self):

        self.name = "Dashboard Backend Engine"

        self.status = "CREATED"

        self.data_stream = {}

        self.events = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("DASHBOARD BACKEND ENGINE ONLINE")
        print("==============================")





    def update_engine_status(
            self,
            engine,
            status):


        self.data_stream[engine] = {


            "status":

            status,


            "timestamp":

            str(datetime.utcnow())

        }



    def update_market_state(
            self,
            data):


        self.data_stream["market"] = data





    def publish_event(
            self,
            event):


        self.events.append({

            "event":

            event,


            "timestamp":

            str(datetime.utcnow())

        })





    def get_dashboard_data(self):


        return {


            "system":

            self.status,


            "engines":

            self.data_stream,


            "events":

            self.events[-20:]


        }





    def health_check(self):


        return {


            "dashboard":

            self.status,


            "time":

            str(datetime.utcnow())

        }
