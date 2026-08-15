"""
=========================================================
GSIS INSTITUTIONAL

EXECUTION OPTIMIZATION &
TRADE MANAGEMENT INTELLIGENCE ENGINE

Version 1.0

Execution Layer

=========================================================
"""


from datetime import datetime
import uuid



class ExecutionOptimizationEngine:


    def __init__(self):

        self.name = "Execution Optimization Engine"

        self.status = "CREATED"

        self.orders = []

        self.positions = []

        self.trade_history = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("EXECUTION OPTIMIZATION ENGINE ONLINE")
        print("==============================")





    def create_order(
            self,
            symbol,
            direction,
            size):


        order = {


            "id":

            str(uuid.uuid4()),


            "symbol":

            symbol,


            "direction":

            direction,


            "size":

            size,


            "status":

            "PENDING",


            "time":

            str(datetime.utcnow())

        }



        self.orders.append(order)


        return order






    def update_position(
            self,
            symbol,
            action):


        position = {


            "symbol":

            symbol,


            "action":

            action,


            "time":

            str(datetime.utcnow())

        }



        self.positions.append(position)


        return position






    def record_trade(
            self,
            trade):


        data = {


            "trade":

            trade,


            "time":

            str(datetime.utcnow())

        }



        self.trade_history.append(data)


        return data






    def execution_report(self):


        return {


            "status":

            self.status,


            "orders":

            len(self.orders),


            "positions":

            len(self.positions),


            "trades":

            len(self.trade_history)

        }
