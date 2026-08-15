"""
=========================================================
GSIS INSTITUTIONAL

REAL-TIME DATA FUSION &
MARKET INTELLIGENCE GATEWAY

Version 1.0

Data Integration Layer

=========================================================
"""


from datetime import datetime
import uuid



class DataFusionGateway:


    def __init__(self):

        self.name = "Data Fusion Gateway"

        self.status = "CREATED"

        self.sources = []

        self.data_streams = []

        self.snapshots = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("DATA FUSION GATEWAY ONLINE")
        print("==============================")





    def register_source(
            self,
            name,
            source_type):


        source = {


            "id":

            str(uuid.uuid4()),


            "name":

            name,


            "type":

            source_type,


            "status":

            "CONNECTED",


            "time":

            str(datetime.utcnow())

        }



        self.sources.append(source)


        return source






    def receive_data(
            self,
            source,
            data):


        stream = {


            "source":

            source,


            "data":

            data,


            "time":

            str(datetime.utcnow())

        }



        self.data_streams.append(stream)


        return stream






    def create_snapshot(
            self,
            market_state):


        snapshot = {


            "market_state":

            market_state,


            "time":

            str(datetime.utcnow())

        }



        self.snapshots.append(snapshot)


        return snapshot






    def gateway_report(self):


        return {


            "status":

            self.status,


            "sources":

            len(self.sources),


            "streams":

            len(self.data_streams),


            "snapshots":

            len(self.snapshots)

        }
