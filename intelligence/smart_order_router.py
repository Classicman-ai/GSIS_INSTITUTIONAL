"""
=========================================================
GSIS INSTITUTIONAL

SMART ORDER ROUTER ENGINE (SORE)

Version: 1.0

Functions:
- Prepare execution orders
- Calculate targets
- Generate broker-ready instructions

=========================================================
"""


from datetime import datetime
import uuid



class SmartOrderRouter:


    def __init__(self):

        self.name = "Smart Order Router Engine"

        self.status = "CREATED"

        self.orders = []



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("SMART ORDER ROUTER ONLINE")
        print("==============================")



    def create_order(
            self,
            symbol,
            direction,
            entry,
            stop_distance,
            reward_ratio=3):


        if direction == "BUY":

            stop_loss = (

                entry

                -

                stop_distance

            )


            take_profit = (

                entry

                +

                (
                    stop_distance
                    *
                    reward_ratio
                )

            )



        elif direction == "SELL":

            stop_loss = (

                entry

                +

                stop_distance

            )


            take_profit = (

                entry

                -

                (
                    stop_distance
                    *
                    reward_ratio
                )

            )



        else:

            return None



        order = {


            "order_id":

            str(uuid.uuid4()),


            "timestamp":

            str(datetime.utcnow()),


            "symbol":

            symbol,


            "direction":

            direction,


            "type":

            "LIMIT",


            "entry":

            entry,


            "stop_loss":

            round(
                stop_loss,
                5
            ),


            "take_profit":

            round(
                take_profit,
                5
            ),


            "reward_ratio":

            reward_ratio,


            "status":

            "READY"

        }



        self.orders.append(order)


        return order




    def cancel_order(
            self,
            order_id):


        for order in self.orders:


            if order["order_id"] == order_id:


                order["status"] = "CANCELLED"


                return order



        return None



    def history(self):

        return self.orders
