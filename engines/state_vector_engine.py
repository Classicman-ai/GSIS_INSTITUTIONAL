"""
GSIS STATE VECTOR ENGINE v3.0

Institutional Intelligence Fusion Core

Inputs:
- Regime Engine
- Structure Intelligence
- Volume Profile
- Order Flow

Output:
Unified Market State Vector
"""


from core.logger import Logger

from engines.structure_intelligence_engine import (
    StructureIntelligenceEngine
)

from engines.volume_profile_engine import (
    VolumeProfileEngine
)

from engines.order_flow_engine import (
    OrderFlowEngine
)

import regime_engine



class StateVectorEngine:


    def __init__(self):

        self.logger = Logger(
            "STATE_VECTOR_ENGINE"
        )


        self.structure = (
            StructureIntelligenceEngine()
        )


        self.volume = (
            VolumeProfileEngine()
        )


        self.order_flow = (
            OrderFlowEngine()
        )


        self.regime = (
            self.load_regime()
        )



    def load_regime(self):

        possible = [

            "RegimeEngine",
            "MarketRegimeEngine",
            "QMOSRegimeEngine"

        ]


        for name in possible:

            if hasattr(regime_engine,name):

                return getattr(
                    regime_engine,
                    name
                )()


        return None



    def get_regime(self,symbol):


        if self.regime is None:

            return None


        if hasattr(
            self.regime,
            "get_latest"
        ):

            return self.regime.get_latest(
                symbol
            )


        if hasattr(
            self.regime,
            "analyze"
        ):

            return self.regime.analyze(
                symbol
            )


        return None




    def calculate_score(
        self,
        structure,
        volume,
        flow
    ):


        score = 0



        if structure:


            bias = structure.get(
                "execution_bias"
            )


            if bias == "BULLISH":

                score += 1


            elif bias == "BEARISH":

                score -= 1





        if volume:


            if volume.get(
                "volume_bias"
            ) == "BUY_ACCEPTANCE":

                score += 1


            elif volume.get(
                "volume_bias"
            ) == "SELL_ACCEPTANCE":

                score -= 1





        if flow:


            if flow.get(
                "flow_bias"
            ) == "BUY_PRESSURE":

                score += 1


            elif flow.get(
                "flow_bias"
            ) == "SELL_PRESSURE":

                score -= 1



        return score





    def build(self,symbol):


        structure = (
            self.structure.analyze(
                symbol
            )
        )


        volume = (
            self.volume.calculate(
                symbol,
                "M15"
            )
        )


        flow = (
            self.order_flow.calculate(
                symbol,
                "M15"
            )
        )


        regime = (
            self.get_regime(
                symbol
            )
        )



        score = self.calculate_score(
            structure,
            volume,
            flow
        )



        if score >= 2:

            bias = "BULLISH"


        elif score <= -2:

            bias = "BEARISH"


        else:

            bias = "NEUTRAL"




        if abs(score) >= 2:

            quality = "HIGH"


        elif abs(score) == 1:

            quality = "MEDIUM"


        else:

            quality = "LOW"




        return {


            "symbol":symbol,


            "regime":regime,


            "structure_intelligence":structure,


            "volume_profile":volume,


            "order_flow":flow,


            "fusion_score":score,


            "market_bias":bias,


            "quality":quality

        }





    def start(self):


        print("===============================")

        print("GSIS STATE VECTOR ENGINE v3.0")

        print("INSTITUTIONAL FUSION CORE")

        print("===============================")



        symbols = [

            "BTCUSDT",
            "ETHUSDT",
            "XAUTUSDT"

        ]



        results=[]



        for symbol in symbols:


            state = self.build(
                symbol
            )


            results.append(
                state
            )


            print()

            print(symbol)

            print("-------------------------------")

            print(
                "BIAS:",
                state["market_bias"]
            )

            print(
                "QUALITY:",
                state["quality"]
            )

            print(
                "FUSION SCORE:",
                state["fusion_score"]
            )



        print()

        print("===============================")

        print("STATE VECTOR COMPLETE")

        print("===============================")



        return results




if __name__=="__main__":


    engine = StateVectorEngine()

    engine.start()
