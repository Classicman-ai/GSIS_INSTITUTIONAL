"""
=========================================================
GSIS INSTITUTIONAL

POSITION MANAGEMENT INTELLIGENCE ENGINE

Version 1.0

Institutional Trade Lifecycle Controller

=========================================================
"""


from datetime import datetime
import uuid



class PositionManagementEngine:



    def __init__(self):

        self.name = "Position Management Engine"

        self.status = "CREATED"

        self.positions = []





    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("POSITION MANAGEMENT ENGINE ONLINE")
        print("==============================")





    def open_position(self, data):


        position = {


            "id":

            str(uuid.uuid4()),


            "timestamp":

            str(datetime.utcnow()),


            "symbol":

            data.get(
                "symbol",
                "UNKNOWN"
            ),


            "direction":

            data.get(
                "direction",
                "WAIT"
            ),


            "entry":

            data.get(
                "entry",
                0
            ),


            "stop_loss":

            data.get(
                "stop_loss",
                0
            ),


            "targets":

            {


                "TP1":

                data.get(
                    "tp1",
                    0
                ),


                "TP2":

                data.get(
                    "tp2",
                    0
                ),


                "TP3":

                data.get(
                    "tp3",
                    0
                )

            },


            "status":

            "ACTIVE",


            "profit_stage":

            "INITIAL"

        }



        self.positions.append(position)


        return position






    def update_position(
            self,
            position_id,
            price):


        for position in self.positions:


            if position["id"] == position_id:


                if price >= position["targets"]["TP1"]:

                    position["profit_stage"] = "TP1 HIT"


                if price >= position["targets"]["TP2"]:

                    position["profit_stage"] = "TP2 HIT"


                if price >= position["targets"]["TP3"]:

                    position["profit_stage"] = "TP3 HIT"



                return position



        return None






    def protect_position(
            self,
            position_id):


        for position in self.positions:


            if position["id"] == position_id:


                position["stop_loss"] = position["entry"]


                position["protection"] = (
                    "BREAK EVEN ACTIVE"
                )


                return position



        return None






    def close_position(
            self,
            position_id,
            reason):


        for position in self.positions:


            if position["id"] == position_id:


                position["status"] = "CLOSED"


                position["close_reason"] = reason


                return position



        return None






    def active_positions(self):

        return [

            p for p in self.positions

            if p["status"] == "ACTIVE"

        ]
