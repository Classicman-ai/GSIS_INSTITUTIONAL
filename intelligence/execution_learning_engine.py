"""
=========================================================
GSIS INSTITUTIONAL

ADAPTIVE EXECUTION LEARNING ENGINE (AELE)

Version: 1.0

Functions:
- Learn from execution history
- Optimize execution parameters
- Improve future decisions

=========================================================
"""


from datetime import datetime



class AdaptiveExecutionLearningEngine:


    def __init__(self):


        self.name = "Adaptive Execution Learning Engine"

        self.status = "CREATED"

        self.memory = []



    def initialize(self):


        self.status = "ONLINE"


        print("==============================")

        print(
            "ADAPTIVE EXECUTION LEARNING ENGINE ONLINE"
        )

        print("==============================")



    def learn(
            self,
            execution_history):


        if not execution_history:


            return {


                "status":
                "NO DATA"

            }



        limit_score = 0

        market_score = 0


        total = len(
            execution_history
        )


        for execution in execution_history:


            if execution.get(
                "order_type"
            ) == "LIMIT":


                limit_score += 1



            if execution.get(
                "status"
            ) == "FILLED":


                market_score += 1



        preferred_order = "LIMIT"


        if market_score > limit_score:


            preferred_order = "MARKET"



        result = {


            "timestamp":
            str(datetime.utcnow()),


            "samples":
            total,


            "preferred_order_type":
            preferred_order,


            "learning_status":
            "ACTIVE",


            "optimization":
            "UPDATED"

        }


        self.memory.append(
            result
        )


        return result



    def get_learning_history(self):


        return self.memory
