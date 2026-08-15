"""
=========================================================
GSIS INSTITUTIONAL

INTELLIGENCE FUSION ENGINE (IFE)

Version 1.0

Central Intelligence Aggregator

=========================================================
"""


from datetime import datetime



class IntelligenceFusionEngine:



    def __init__(self):


        self.name = "Intelligence Fusion Engine"

        self.status = "CREATED"

        self.history = []





    def initialize(self):


        self.status = "ONLINE"


        print("==============================")
        print("INTELLIGENCE FUSION ENGINE ONLINE")
        print("==============================")






    def analyze(
            self,
            intelligence):


        score = 0


        factors = {}



        # Market Structure

        structure = intelligence.get(
            "market_structure",
            0
        )

        score += structure

        factors["market_structure"] = structure



        # Liquidity

        liquidity = intelligence.get(
            "liquidity",
            0
        )

        score += liquidity

        factors["liquidity"] = liquidity



        # Displacement

        displacement = intelligence.get(
            "displacement",
            0
        )

        score += displacement

        factors["displacement"] = displacement



        # Order Block

        order_block = intelligence.get(
            "order_block",
            0
        )

        score += order_block

        factors["order_block"] = order_block



        # Supply Demand

        supply_demand = intelligence.get(
            "supply_demand",
            0
        )

        score += supply_demand

        factors["supply_demand"] = supply_demand



        confidence = score / 5



        result = {


            "timestamp":

            str(datetime.utcnow()),


            "total_score":

            score,


            "confidence":

            round(confidence,2),


            "factors":

            factors,


            "status":

            self.classify(confidence)

        }



        self.history.append(
            result
        )


        return result






    def classify(
            self,
            confidence):


        if confidence >= 80:

            return "HIGH CONFIDENCE"


        elif confidence >= 60:

            return "MODERATE CONFIDENCE"


        elif confidence >= 40:

            return "LOW CONFIDENCE"


        else:

            return "NO TRADE CONDITION"






    def latest(self):


        if self.history:

            return self.history[-1]


        return None
