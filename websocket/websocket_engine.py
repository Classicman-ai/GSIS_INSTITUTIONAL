"""
=========================================================
GSIS INSTITUTIONAL

REAL-TIME WEBSOCKET
INTELLIGENCE INTERFACE ENGINE

Version 1.0

Live Communication Layer

=========================================================
"""


from datetime import datetime
import uuid



class WebSocketEngine:


    def __init__(self):

        self.name = "WebSocket Intelligence Engine"

        self.status = "CREATED"

        self.clients = []

        self.messages = []

        self.streams = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("WEBSOCKET ENGINE ONLINE")
        print("==============================")





    def register_client(
            self,
            client_name):


        client = {


            "id":

            str(uuid.uuid4()),


            "name":

            client_name,


            "connected":

            True,


            "time":

            str(datetime.utcnow())

        }



        self.clients.append(client)


        return client






    def send_stream(
            self,
            channel,
            data):


        message = {


            "channel":

            channel,


            "data":

            data,


            "time":

            str(datetime.utcnow())

        }



        self.messages.append(message)


        return message






    def create_stream(
            self,
            name):


        stream = {


            "name":

            name,


            "status":

            "ACTIVE",


            "time":

            str(datetime.utcnow())

        }



        self.streams.append(stream)


        return stream






    def websocket_report(self):


        return {


            "status":

            self.status,


            "clients":

            len(self.clients),


            "messages":

            len(self.messages),


            "streams":

            len(self.streams)

        }
