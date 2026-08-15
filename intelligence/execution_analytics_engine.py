"""
=========================================================
GSIS INSTITUTIONAL

EXECUTION ANALYTICS & STATISTICS ENGINE (EASE)

Version: 1.0

Functions:
- Analyze execution history
- Calculate execution quality
- Generate statistics

=========================================================
"""


from datetime import datetime



class ExecutionAnalyticsEngine:


    def __init__(self):


        self.name = "Execution Analytics Engine"

        self.status = "CREATED"



    def initialize(self):


        self.status = "ONLINE"


        print("==============================")

        print(
            "EXECUTION ANALYTICS ENGINE ONLINE"
        )

        print("==============================")



    def analyze(
            self,
            executions):


        total = len(
            executions
        )


        if total == 0:


            return {


                "status":
                "NO DATA"

            }



        successful = 0

        slippage_values = []

        order_types = {}



        for item in executions:


            data = item.get(
                "execution_data",
                {}
            )


            if data.get(
                "status"
            ) == "FILLED":


                successful += 1



            if "slippage" in data:


                slippage_values.append(
                    data["slippage"]
                )



            order = item.get(
                "order_type"
            )


            if order:


                order_types[order] = (

                    order_types.get(
                        order,
                        0
                    )
                    + 1

                )



        success_rate = (

            successful /
            total
            *
            100

        )



        average_slippage = 0


        if slippage_values:


            average_slippage = (

                sum(slippage_values)
                /
                len(slippage_values)

            )



        score = self.calculate_score(
            success_rate,
            average_slippage
        )


        return {


            "timestamp":
            str(datetime.utcnow()),


            "total_executions":
            total,


            "success_rate":
            round(
                success_rate,
                2
            ),


            "average_slippage":
            round(
                average_slippage,
                5
            ),


            "order_distribution":
            order_types,


            "execution_score":
            score

        }



    def calculate_score(
            self,
            success_rate,
            slippage):


        score = success_rate



        if slippage > 0.05:


            score -= 20



        elif slippage > 0.02:


            score -= 10



        return round(
            max(score,0),
            2
        )
