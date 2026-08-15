import os
import sys
import datetime


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

sys.path.insert(
    0,
    PROJECT_ROOT
)


from intelligence.core.gsis_adaptive_intelligence_bridge import (
    GSISAdaptiveIntelligenceBridge
)

from intelligence.core.gsis_pattern_probability_engine import (
    GSISPatternProbabilityEngine
)

from intelligence.core.gsis_intelligence_fusion_engine import (
    GSISIntelligenceFusionEngine
)

from intelligence.core.gsis_confidence_calibration_engine import (
    GSISConfidenceCalibrationEngine
)



class GSISMasterIntelligenceAdapter:


    def __init__(self):

        print("==============================")
        print("GSIS MASTER INTELLIGENCE ADAPTER v7.0 ONLINE")
        print("UNIFIED ADAPTIVE INTELLIGENCE SYNTHESIS ACTIVE")
        print("==============================")


        self.adaptive = (
            GSISAdaptiveIntelligenceBridge()
        )

        self.pattern = (
            GSISPatternProbabilityEngine()
        )

        self.fusion = (
            GSISIntelligenceFusionEngine()
        )

        self.calibration = (
            GSISConfidenceCalibrationEngine()
        )



    def analyze(
        self,
        signal
    ):


        print("==============================")
        print("GSIS MASTER INTELLIGENCE ANALYSIS")
        print("==============================")


        adaptive_result = (
            self.adaptive.analyze(
                signal
            )
        )


        pattern_name = signal.get(
            "pattern",
            "BULLISH_CANDLE"
        )


        pattern_result = (
            self.pattern.analyze_pattern(
                pattern_name
            )
        )


        historical_probability = pattern_result.get(
            "historical_probability",
            0
        )



        calibrated_result = (
            self.calibration.calculate(

                adaptive_result.get(
                    "technical_confidence",
                    0
                ),

                historical_probability,

                pattern_result.get(
                    "samples",
                    0
                ),

                signal.get(
                    "liquidity_score",
                    80
                ),

                signal.get(
                    "economic_risk",
                    0
                )

            )
        )



        fusion_result = (

            self.fusion.analyze(

                signal.get(
                    "structure",
                    {}
                ),

                signal.get(
                    "zone",
                    {}
                ),

                signal.get(
                    "liquidity",
                    {}
                ),

                signal.get(
                    "candlestick",
                    {}
                ),

                signal.get(
                    "chart_pattern",
                    {}
                ),

                signal.get(
                    "economic",
                    {}
                ),

                historical_probability,

                calibrated_result.get(
                    "final_confidence",
                    0
                )

            )

        )



        result = {


            "status":
            "MASTER INTELLIGENCE COMPLETE",


            "adaptive":
            adaptive_result,


            "pattern":
            pattern_result,


            "calibration":
            calibrated_result,


            "fusion":
            fusion_result,


            "final_confidence":
            fusion_result.get(
                "confidence",
                calibrated_result.get(
                    "final_confidence",
                    0
                )
            ),


            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }



        print("==============================")
        print("GSIS MASTER INTELLIGENCE RESULT")
        print("==============================")

        print(result)


        return result





if __name__ == "__main__":


    engine = GSISMasterIntelligenceAdapter()


    test_signal = {


        "pattern":
        "BULLISH_CANDLE",


        "structure":
        {
            "bos": True,
            "trend": "BULLISH"
        },


        "zone":
        {
            "nearest_zone":
            "DEMAND_ZONE"
        },


        "liquidity":
        {
            "liquidity_state":
            "ACTIVE"
        },


        "candlestick":
        {
            "confirmation":
            True
        },


        "chart_pattern":
        {},


        "economic":
        {},


        "liquidity_score":
        80,


        "economic_risk":
        0

    }



    engine.analyze(
        test_signal
    )
