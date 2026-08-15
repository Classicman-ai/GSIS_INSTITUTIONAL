"""
=========================================================
GSIS INSTITUTIONAL

WEBSOCKET COMMUNICATION ENGINE

Version 1.0

Real-Time Communication Layer

=========================================================
"""


from datetime import datetime
import json



class WebSocketEngine:


    def __init__(self):

        self.name = "WebSocket Communication Engine"

        self.status = "CREATED"

        self.clients = []

        self.messages = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("WEBSOCKET ENGINE ONLINE")
        print("==============================")





    def connect_client(
            self,
            client):


        self.clients.append(client)


        return {


            "status":

            "CONNECTED",


            "clients":

            len(self.clients)

        }





    def disconnect_client(
            self,
            client):


        if client in self.clients:

            self.clients.remove(client)


        return {


            "status":

            "DISCONNECTED"

        }





    def broadcast(
            self,
            event,
            data):


        message = {


            "timestamp":

            str(datetime.utcnow()),


            "event":

            event,


            "data":

            data

        }



        self.messages.append(
            message
        )


        return message





    def send_engine_status(
            self,
            engine,
            status):


        return self.broadcast(

            "ENGINE_STATUS",

            {

                "engine":

                engine,


                "status":

                status

            }

        )





    def send_market_update(
            self,
            market_data):


        return self.broadcast(

            "MARKET_UPDATE",

            market_data

        )





    def latest_messages(
            self):


        return self.messages[-50:]
