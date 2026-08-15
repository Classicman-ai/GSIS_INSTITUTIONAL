"""
=========================================================
GSIS INSTITUTIONAL

SLIPPAGE & MARKET IMPACT CONTROL ENGINE (SMICE)

Version: 1.0

Functions:
- Estimate slippage
- Evaluate execution conditions
- Protect order quality

=========================================================
"""


from datetime import datetime



class SlippageControlEngine:


    def __init__(self):


        self.name = "Slippage Control Engine"

        self.status = "CREATED"

        self.max_slippage = 0.05

        self.history = []



    def initialize(self):


        self.status = "ONLINE"


        print("==============================")

        print(
            "SLIPPAGE CONTROL ENGINE ONLINE"
        )

        print("==============================")



    def evaluate(
            self,
            expected_price,
            current_price):


        slippage = abs(
            current_price -
            expected_price
        )



        if slippage <= self.max_slippage:


            decision = "APPROVED"

            condition = "NORMAL"



        elif slippage <= (
            self.max_slippage * 3
        ):


            decision = "DELAYED"

            condition = "HIGH_IMPACT"



        else:


            decision = "REJECTED"

            condition = "EXTREME_SLIPPAGE"



        result = {


            "expected_price":
            expected_price,


            "current_price":
            current_price,


            "slippage":
            round(slippage,5),


            "condition":
            condition,


            "execution":
            decision,


            "timestamp":
            str(datetime.utcnow())

        }


        self.history.append(
            result
        )


        return result



    def get_history(self):


        return self.history
