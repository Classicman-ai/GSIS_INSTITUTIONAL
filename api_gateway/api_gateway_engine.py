"""
=========================================================
GSIS INSTITUTIONAL

API GATEWAY &
EXTERNAL INTEGRATION ENGINE

Version 1.0

Connectivity Layer

=========================================================
"""


from datetime import datetime
import uuid



class APIGatewayEngine:


    def __init__(self):

        self.name = "API Gateway Engine"

        self.status = "CREATED"

        self.connections = []

        self.requests = []

        self.responses = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("API GATEWAY ENGINE ONLINE")
        print("==============================")





    def register_connection(
            self,
            name,
            connection_type):


        connection = {


            "id":

            str(uuid.uuid4()),


            "name":

            name,


            "type":

            connection_type,


            "status":

            "CONNECTED",


            "time":

            str(datetime.utcnow())

        }



        self.connections.append(connection)


        return connection






    def receive_request(
            self,
            source,
            request):


        data = {


            "source":

            source,


            "request":

            request,


            "time":

            str(datetime.utcnow())

        }



        self.requests.append(data)


        return data






    def send_response(
            self,
            destination,
            response):


        data = {


            "destination":

            destination,


            "response":

            response,


            "time":

            str(datetime.utcnow())

        }



        self.responses.append(data)


        return data






    def gateway_report(self):


        return {


            "status":

            self.status,


            "connections":

            len(self.connections),


            "requests":

            len(self.requests),


            "responses":

            len(self.responses)

        }
