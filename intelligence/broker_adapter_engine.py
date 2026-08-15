"""
=========================================================
GSIS INSTITUTIONAL

BROKER ADAPTER ENGINE (BAE)

Version: 1.0

Functions:
- Translate GSIS orders
- Validate execution requests
- Prepare broker instructions

=========================================================
"""


from datetime import datetime
import uuid



class BrokerAdapterEngine:


    def __init__(self):

        self.name = "Broker Adapter Engine"

        self.status = "CREATED"

        self.requests = []



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("BROKER ADAPTER ENGINE ONLINE")
        print("==============================")



    def prepare_order(
            self,
            order,
            permission):


        if permission != "APPROVED":

            return {

                "status":
                "BLOCKED",

                "reason":
                "Execution not authorized"

            }



        broker_request = {


            "request_id":

            str(uuid.uuid4()),


            "timestamp":

            str(datetime.utcnow()),


            "symbol":

            order.get(
                "symbol"
            ),


            "action":

            order.get(
                "direction"
            ),


            "order_type":

            order.get(
                "type"
            ),


            "entry":

            order.get(
                "entry"
            ),


            "stop_loss":

            order.get(
                "stop_loss"
            ),


            "take_profit":

            order.get(
                "take_profit"
            ),


            "status":

            "READY_FOR_BROKER"

        }


        self.requests.append(
            broker_request
        )


        return broker_request



    def send(
            self,
            request):


        # Placeholder
        # Real MT5/API connection added later


        request["status"] = "SIMULATED"


        return request



    def history(self):

        return self.requests
