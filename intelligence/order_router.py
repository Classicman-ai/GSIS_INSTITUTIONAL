"""
=========================================================
GSIS INSTITUTIONAL

SMART ORDER ROUTER (SOR)

Version: 1.0

Functions:
- Select order type
- Evaluate market conditions
- Reduce execution impact

=========================================================
"""


from datetime import datetime



class OrderRouter:


    def __init__(self):


        self.name = "Smart Order Router"

        self.status = "CREATED"

        self.history = []



    def initialize(self):


        self.status = "ONLINE"


        print("==============================")

        print(
            "SMART ORDER ROUTER ONLINE"
        )

        print("==============================")



    def select_order_type(
            self,
            volatility,
            liquidity,
            urgency):


        order_type = "MARKET"

        reason = "FAST EXECUTION"



        if liquidity == "LOW":


            order_type = "LIMIT"

            reason = "LOW LIQUIDITY PROTECTION"



        elif volatility == "HIGH":


            order_type = "LIMIT"

            reason = "VOLATILITY CONTROL"



        elif urgency == "HIGH":


            order_type = "MARKET"

            reason = "URGENT EXECUTION"



        else:


            order_type = "LIMIT"

            reason = "PRICE OPTIMIZATION"



        result = {


            "order_type":
            order_type,


            "reason":
            reason,


            "timestamp":
            str(datetime.utcnow())

        }


        self.history.append(
            result
        )


        return result



    def get_history(self):


        return self.history
