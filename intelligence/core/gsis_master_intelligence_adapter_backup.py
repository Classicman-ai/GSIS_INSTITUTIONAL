import sys
import os
import datetime


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(BASE_DIR)


from gsis_intelligence_fusion_engine import (
    GSISIntelligenceFusionEngine
)

from gsis_confidence_calibration_engine import (
    GSISConfidenceCalibrationEngine
)

from gsis_pattern_probability_engine import (
    GSISPatternProbabilityEngine
)



class GSISMasterIntelligenceAdapter:


    def __init__(self):

        print("==============================")
        print("GSIS MASTER INTELLIGENCE ADAPTER v1.1 ONLINE")
        print("INSTITUTIONAL INTELLIGENCE BRIDGE ACTIVE")
        print("==============================")


        self.fusion = GSISIntelligenceFusionEngine()

        self.calibration = GSISConfidenceCalibrationEngine()

        self.probability = GSISPatternProbabilityEngine()



    def analyze(self, context):


        pattern = context.get(
            "pattern",
            "BULLISH_ENGULFING"
        )


        probability = self.probability.analyze_pattern(
            pattern
        )


        historical_probability = probability.get(
            "win_probability",
            0
        )


        samples = probability.get(
            "samples",
            0
        )


        calibration = self.calibration.calculate(

            technical_score=90,

            historical_probability=
            historical_probability,

            sample_size=
            samples,

            liquidity_score=85,

            economic_risk=10

        )


        decision = self.fusion.analyze(

            context.get("structure", {}),

            context.get("zone", {}),

            context.get("liquidity", {}),

            context.get("candlestick", {}),

            context.get("chart_pattern", {}),

            context.get("economic", {}),

            historical_probability,

            calibration.get(
                "final_confidence",
                0
            )

        )


        return {

            "status":
            "MASTER INTELLIGENCE COMPLETE",

            "decision":
            decision,

            "historical_probability":
            historical_probability,

            "calibrated_confidence":
            calibration.get(
                "final_confidence",
                0
            ),

            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }




if __name__ == "__main__":


    engine = GSISMasterIntelligenceAdapter()


    result = engine.analyze(

        {

            "structure":
            {
                "trend":"BULLISH",
                "bos":True
            },

            "zone":
            {
                "nearest_zone":"DEMAND"
            },

            "liquidity":
            {
                "liquidity_sweeps":
                [
                    "SELL_SIDE_SWEEP"
                ]
            },

            "candlestick":
            {
                "patterns":
                [
                    "BULLISH_ENGULFING"
                ]
            },

            "chart_pattern":
            {
                "patterns":[]
            },

            "economic":
            {
                "high_impact":0
            },

            "pattern":
            "BULLISH_ENGULFING"

        }

    )


    print("==============================")
    print("GSIS MASTER INTELLIGENCE RESULT")
    print("==============================")
    print(result)
