"""
=========================================================
GSIS INSTITUTIONAL

BROKER & LIQUIDITY INTELLIGENCE ENGINE (BLIE)

Version: 1.0

Functions:
- Monitor execution environment
- Analyze broker quality
- Evaluate liquidity

=========================================================
"""


from datetime import datetime



class BrokerLiquidityEngine:


    def __init__(self):


        self.name = "Broker Liquidity Intelligence Engine"

        self.status = "CREATED"

        self.history = []



    def initialize(self):


        self.status = "ONLINE"


        print("==============================")

        print(
            "BROKER LIQUIDITY ENGINE ONLINE"
        )

        print("==============================")



    def analyze(
            self,
            broker,
            latency,
            total_orders,
            filled_orders,
            liquidity):


        fill_rate = 0


        if total_orders > 0:


            fill_rate = (

                filled_orders /
                total_orders

            ) * 100



        score = self.calculate_score(
            latency,
            fill_rate,
            liquidity
        )


        result = {


            "broker":
            broker,


            "latency_ms":
            latency,


            "fill_rate":
            round(
                fill_rate,
                2
            ),


            "liquidity":
            liquidity,


            "quality_score":
            score,


            "timestamp":
            str(datetime.utcnow())

        }


        self.history.append(
            result
        )


        return result



    def calculate_score(
            self,
            latency,
            fill_rate,
            liquidity):


        score = fill_rate



        if latency > 1000:


            score -= 20


        elif latency > 500:


            score -= 10



        if liquidity == "LOW":


            score -= 15



        elif liquidity == "HIGH":


            score += 5



        return round(
            max(score,0),
            2
        )



    def history_report(self):


        return self.history
