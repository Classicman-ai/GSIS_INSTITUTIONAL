"""
=========================================================
GSIS INSTITUTIONAL

API GATEWAY ENGINE

Version 1.0

External Communication Control Layer

=========================================================
"""


from datetime import datetime
import uuid



class APIGatewayEngine:


    def __init__(self):

        self.name = "API Gateway Engine"

        self.status = "CREATED"

        self.requests = []

        self.services = {}





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("API GATEWAY ENGINE ONLINE")
        print("==============================")





    def register_service(
            self,
            name,
            service):


        self.services[name] = service


        return {


            "service":

            name,


            "status":

            "REGISTERED"

        }





    def request(
            self,
            service,
            action,
            payload=None):


        request_id = str(
            uuid.uuid4()
        )


        response = {


            "request_id":

            request_id,


            "timestamp":

            str(datetime.utcnow()),


            "service":

            service,


            "action":

            action

        }



        if service in self.services:


            module = self.services[service]


            if hasattr(
                module,
                action
            ):


                result = getattr(
                    module,
                    action
                )()


                response["result"] = result



            else:

                response["error"] = (
                    "ACTION NOT AVAILABLE"
                )


        else:

            response["error"] = (
                "SERVICE NOT FOUND"
            )



        self.requests.append(
            response
        )


        return response






    def system_status(self):


        return {


            "gateway":

            self.status,


            "services":

            list(
                self.services.keys()
            ),


            "requests":

            len(
                self.requests
            )

        }
