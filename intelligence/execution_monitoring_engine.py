"""
=========================================================
GSIS INSTITUTIONAL

EXECUTION MONITORING ENGINE (EME)

Version: 1.0

Functions:
- Monitor active trades
- Track trade lifecycle
- Store execution history

=========================================================
"""


from datetime import datetime
import uuid



class ExecutionMonitoringEngine:


    def __init__(self):

        self.name = "Execution Monitoring Engine"

        self.status = "CREATED"

        self.positions = []

        self.history = []



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("EXECUTION MONITORING ENGINE ONLINE")
        print("==============================")



    def register_trade(
            self,
            order):


        position = {


            "position_id":

            str(uuid.uuid4()),


            "created":

            str(datetime.utcnow()),


            "symbol":

            order.get(
                "symbol"
            ),


            "direction":

            order.get(
                "direction"
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

            "ACTIVE"


        }


        self.positions.append(
            position
        )


        return position



    def update_price(
            self,
            position_id,
            price):


        for position in self.positions:


            if position["position_id"] == position_id:


                position["current_price"] = price


                return position



        return None




    def close_trade(
            self,
            position_id,
            result):


        for position in self.positions:


            if position["position_id"] == position_id:


                position["status"] = "CLOSED"

                position["result"] = result


                self.history.append(
                    position
                )


                return position



        return None




    def active_positions(self):

        return [

            p for p in self.positions

            if p["status"] == "ACTIVE"

        ]



    def history_report(self):

        return self.history
