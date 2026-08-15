"""
=========================================================
GSIS INSTITUTIONAL

INSTITUTIONAL ORDER SLICING ENGINE (IOSE)

Version: 1.0

Functions:
- Split large orders
- Reduce market impact
- Create execution schedule

=========================================================
"""


from datetime import datetime
import uuid



class OrderSlicingEngine:


    def __init__(self):


        self.name = "Institutional Order Slicing Engine"

        self.status = "CREATED"

        self.history = []



    def initialize(self):


        self.status = "ONLINE"


        print("==============================")

        print(
            "ORDER SLICING ENGINE ONLINE"
        )

        print("==============================")



    def create_plan(
            self,
            asset,
            order_size,
            liquidity,
            impact_level):


        slices = 1

        mode = "NORMAL"



        if impact_level == "HIGH":


            slices = 10

            mode = "SLOW"



        elif impact_level == "MEDIUM":


            slices = 5

            mode = "CONTROLLED"



        elif liquidity == "LOW":


            slices = 5

            mode = "CONTROLLED"



        else:


            slices = 1

            mode = "FAST"



        slice_size = (

            order_size /
            slices

        )



        plan = {


            "plan_id":
            str(uuid.uuid4()),


            "asset":
            asset,


            "total_size":
            order_size,


            "number_of_slices":
            slices,


            "slice_size":
            round(
                slice_size,
                4
            ),


            "execution_mode":
            mode,


            "timestamp":
            str(datetime.utcnow())

        }


        self.history.append(
            plan
        )


        return plan



    def history_report(self):


        return self.history
