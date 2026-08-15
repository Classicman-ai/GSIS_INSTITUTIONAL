import datetime


class AutonomousDecisionIntelligenceEngine:

    def __init__(self):

        print("==============================")
        print("GSIS AUTONOMOUS DECISION INTELLIGENCE ENGINE v1.0 ONLINE")
        print("FINAL TRADE INTELLIGENCE CONTROL ACTIVE")
        print("==============================")


    def evaluate(
        self,
        confidence,
        pattern_score,
        risk_score,
        memory_score
    ):

        decision_score = 0
        reasons = []


        # Confidence evaluation
        if confidence >= 70:
            decision_score += 25
            reasons.append("CONFIDENCE PASSED")
        else:
            reasons.append("CONFIDENCE FAILED")


        # Pattern evaluation
        if pattern_score >= 60:
            decision_score += 25
            reasons.append("PATTERN PASSED")
        else:
            reasons.append("PATTERN FAILED")


        # Risk evaluation
        if risk_score >= 70:
            decision_score += 25
            reasons.append("RISK PASSED")
        else:
            reasons.append("RISK WARNING")


        # Memory intelligence
        if memory_score >= 50:
            decision_score += 25
            reasons.append("MEMORY VALIDATED")
        else:
            reasons.append("MEMORY WEAK")


        if decision_score >= 80:

            decision = "APPROVED"

        elif decision_score >= 50:

            decision = "CAUTION"

        else:

            decision = "REJECT"



        result = {

            "status": "DECISION COMPLETE",
            "decision": decision,
            "decision_score": decision_score,
            "confidence": confidence,
            "pattern_score": pattern_score,
            "risk_score": risk_score,
            "memory_score": memory_score,
            "reasons": reasons,
            "timestamp": datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }


        print("==============================")
        print("GSIS DECISION RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":

    engine = AutonomousDecisionIntelligenceEngine()

    engine.evaluate(
        confidence=70,
        pattern_score=66,
        risk_score=80,
        memory_score=50
    )
