from datetime import datetime, timezone


class ConfidenceEngine:

    def __init__(self):
        print("==============================")
        print("GSIS CONFIDENCE INTELLIGENCE ENGINE v1.2 ONLINE")
        print("==============================")
        print("INSTITUTIONAL DECISION SCORING ACTIVE")
        print("==============================")


    def evaluate(self, base_confidence=0, pattern_score=0, **kwargs):

        print("==============================")
        print("GSIS CONFIDENCE EVALUATION")
        print("==============================")


        confidence_points = 0
        pattern_points = 0


        # Market confidence scoring
        if base_confidence >= 90:
            confidence_points = 50

        elif base_confidence >= 70:
            confidence_points = 35

        else:
            confidence_points = 20



        # Pattern recognition scoring
        if pattern_score >= 90:
            pattern_points = 50

        elif pattern_score >= 70:
            pattern_points = 35

        else:
            pattern_points = 20



        final_confidence = min(
            confidence_points + pattern_points,
            100
        )


        if final_confidence >= 85:
            decision = "APPROVED"

        elif final_confidence >= 70:
            decision = "CAUTION"

        else:
            decision = "REJECTED"



        result = {

            "final_confidence": final_confidence,
            "decision": decision,
            "status": "INTELLIGENCE COMPLETE",
            "timestamp": datetime.now(timezone.utc).isoformat()

        }


        print(result)

        return result
