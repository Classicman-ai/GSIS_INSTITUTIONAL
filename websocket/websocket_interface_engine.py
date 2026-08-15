"""
=========================================================
GSIS INSTITUTIONAL

WEBSOCKET INTELLIGENCE INTERFACE
&
COMMAND DASHBOARD ENGINE

Version 1.0

Visualization Layer

=========================================================
"""


from datetime import datetime
import uuid



class WebSocketInterfaceEngine:


    def __init__(self):

        self.name = "WebSocket Interface Engine"

        self.status = "CREATED"

        self.connections = []

        self.messages = []

        self.dashboard_data = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("WEBSOCKET INTERFACE ENGINE ONLINE")
        print("==============================")





    def connect_client(
            self,
            client):


        connection = {


            "id":

            str(uuid.uuid4()),


            "client":

            client,


            "status":

            "CONNECTED",


            "time":

            str(datetime.utcnow())

        }



        self.connections.append(connection)


        return connection






    def broadcast(
            self,
            event,
            data):


        message = {


            "event":

            event,


            "data":

            data,


            "time":

            str(datetime.utcnow())

        }



        self.messages.append(message)


        return message






    def update_dashboard(
            self,
            component,
            status):


        update = {


            "component":

            component,


            "status":

            status,


            "time":

            str(datetime.utcnow())

        }



        self.dashboard_data.append(update)


        return update






    def websocket_report(self):


        return {


            "status":

            self.status,


            "connections":

            len(self.connections),


            "messages":

            len(self.messages),


            "dashboard_updates":

            len(self.dashboard_data)

        }
