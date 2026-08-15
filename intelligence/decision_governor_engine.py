import datetime


class DecisionGovernorEngine:

    def __init__(self):
        print("==============================")
        print("GSIS DECISION GOVERNOR ENGINE v1.1 ONLINE")
        print("SMART TRADE APPROVAL CONTROL ACTIVE")
        print("==============================")


    def evaluate(self, intelligence, risk=None, market=None):

        confidence = intelligence.get("confidence", 0)
        pattern_score = intelligence.get("pattern_match", 0)

        reasons = []

        approval_score = 0


        # Confidence validation
        if confidence >= 70:
            approval_score += 30
            reasons.append("CONFIDENCE ACCEPTED")
        else:
            reasons.append("LOW CONFIDENCE")


        # Pattern validation
        if pattern_score >= 60:
            approval_score += 30
            reasons.append("PATTERN ACCEPTED")
        else:
            reasons.append("WEAK PATTERN")


        # Risk validation
        if risk:

            if risk.get("lot_size", 0) > 0:
                approval_score += 20
                reasons.append("RISK VALIDATED")


        # Market validation
        if market:

            if market.get("liquidity_state") == "ACTIVE":
                approval_score += 10
                reasons.append("LIQUIDITY ACTIVE")


            if market.get("volatility") == "NORMAL":
                approval_score += 10
                reasons.append("VOLATILITY ACCEPTED")


        if approval_score >= 60:
            decision = "APPROVED"
        else:
            decision = "REJECT"


        result = {

            "decision": decision,

            "approval_score": approval_score,

            "confidence": confidence,

            "pattern_score": pattern_score,

            "reasons": reasons,

            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }


        print("==============================")
        print("GSIS GOVERNOR RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":

    engine = DecisionGovernorEngine()

    result = engine.evaluate(
        {
            "confidence":70,
            "pattern_match":66
        },
        {
            "lot_size":3.33
        }
    )

    print(result)
