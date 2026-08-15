import sys
import os
from datetime import datetime, timezone

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)

from intelligence.pattern_matching_engine import PatternMatchingEngine
from intelligence.confidence_engine import ConfidenceEngine


print("==============================")
print("GSIS INTELLIGENCE BRIDGE v2.2 ONLINE")
print("==============================")
print("FULL EXECUTION INTELLIGENCE ACTIVE")
print("==============================")


class IntelligenceBridge:

    def __init__(self):

        self.pattern_engine = PatternMatchingEngine()
        self.confidence_engine = ConfidenceEngine()


    def evaluate(
        self,
        symbol,
        direction,
        confidence=100,
        reasons=None
    ):

        if reasons is None:
            reasons = []

        print("==============================")
        print("GSIS INTELLIGENCE EVALUATION")
        print("==============================")

        pattern_result = self.pattern_engine.match_pattern(
            symbol=symbol,
            direction=direction,
            reasons=reasons,
            confidence=confidence
        )

        pattern_score = pattern_result.get(
            "match_score",
            0
        )

        confidence_result = self.confidence_engine.evaluate(
            base_confidence=confidence
        )

        final_confidence = confidence_result.get(
            "final_confidence",
            confidence
        )

        decision = (
            "APPROVED"
            if final_confidence >= 80
            else "CAUTION"
        )

        result = {

            "symbol": symbol,

            "direction": direction,

            "pattern_match": pattern_score,

            "confidence": final_confidence,

            "decision": decision,

            "status": "INTELLIGENCE COMPLETE",

            "timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat()

        }

        print("==============================")
        print("GSIS BRIDGE RESULT")
        print("==============================")
        print(result)

        return result
