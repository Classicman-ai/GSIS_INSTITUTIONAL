import datetime
import os
import sys


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

sys.path.insert(0, PROJECT_ROOT)


from intelligence.core.gsis_adaptive_intelligence_bridge import (
    GSISAdaptiveIntelligenceBridge
)

from intelligence.core.gsis_intelligence_fusion_engine import (
    GSISIntelligenceFusionEngine
)

from intelligence.core.gsis_confidence_calibration_engine import (
    GSISConfidenceCalibrationEngine
)

from intelligence.core.gsis_pattern_probability_engine import (
    GSISPatternProbabilityEngine
)



class GSISMasterIntelligenceAdapter:


    def __init__(self):

        print("==============================")
        print("GSIS MASTER INTELLIGENCE ADAPTER v6.1 ONLINE")
        print("UNIFIED INTELLIGENCE COMPATIBILITY LAYER ACTIVE")
        print("==============================")


        self.adaptive = GSISAdaptiveIntelligenceBridge()

        self.fusion = GSISIntelligenceFusionEngine()

        self.calibration = GSISConfidenceCalibrationEngine()

        self.pattern = GSISPatternProbabilityEngine()



    def analyze(self, signal):


        print("==============================")
        print("GSIS MASTER INTELLIGENCE ANALYSIS")
        print("==============================")


        adaptive_result = self.adaptive.analyze(
            signal
        )


        technical_confidence = adaptive_result.get(
            "final_confidence",
            0
        )


        historical_probability = adaptive_result.get(
            "historical_probability",
            0
        )


        memory_samples = adaptive_result.get(
            "memory_samples",
            0
        )


        pattern_result = self.pattern.analyze_pattern(
            signal.get(
                "pattern",
                "UNKNOWN"
            )
        )



        calibration_result = self.calibration.calculate(

            technical_confidence,

            historical_probability,

            memory_samples,

            signal.get(
                "liquidity_score",
                80
            ),

            signal.get(
                "economic_risk",
                0
            )

        )



        calibrated_confidence = calibration_result.get(
            "calibrated_confidence",
            technical_confidence
        )



        fusion_result = self.fusion.analyze(

            signal.get(
                "structure",
                {
                    "bos": True,
                    "trend": "BULLISH"
                }
            ),


            signal.get(
                "zone",
                {
                    "nearest_zone":
                    "DEMAND_ZONE"
                }
            ),


            signal.get(
                "liquidity",
                {
                    "liquidity_state":
                    "ACTIVE"
                }
            ),


            signal.get(
                "candlestick",
                {
                    "confirmation":
                    True
                }
            ),


            signal.get(
                "chart_pattern",
                {
                    "pattern":
                    "BREAK_OF_STRUCTURE"
                }
            ),


            signal.get(
                "economic",
                {
                    "risk":
                    "LOW"
                }
            ),


            historical_probability,


            calibrated_confidence

        )



        result = {


            "status":
            "MASTER INTELLIGENCE COMPLETE",


            "adaptive":
            adaptive_result,


            "pattern":
            pattern_result,


            "calibration":
            calibration_result,


            "fusion":
            fusion_result,


            "final_confidence":
            calibrated_confidence,


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


        "symbol":
        "XAUUSD",


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
        {
            "pattern":
            "BREAK_OF_STRUCTURE"
        },


        "economic":
        {
            "risk":
            "LOW"
        },


        "liquidity_score":
        80,


        "economic_risk":
        0

    }


    engine.analyze(
        test_signal
    )
