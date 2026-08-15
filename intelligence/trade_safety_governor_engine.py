import datetime


class TradeSafetyGovernorEngine:

    def __init__(self):

        print("==============================")
        print("GSIS TRADE SAFETY GOVERNOR ENGINE v1.0 ONLINE")
        print("EXECUTION SAFETY CONTROL ACTIVE")
        print("==============================")


    def validate(
        self,
        decision,
        confidence,
        risk_reward,
        volatility,
        spread
    ):

        safety_score = 0
        reasons = []


        # Decision check
        if decision in ["APPROVED", "CAUTION"]:
            safety_score += 20
            reasons.append("DECISION ACCEPTED")
        else:
            reasons.append("DECISION REJECTED")


        # Confidence check
        if confidence >= 70:
            safety_score += 20
            reasons.append("CONFIDENCE SAFE")
        else:
            reasons.append("CONFIDENCE LOW")


        # Risk reward check
        if risk_reward >= 1.5:
            safety_score += 25
            reasons.append("RISK REWARD ACCEPTABLE")
        else:
            reasons.append("RISK REWARD WEAK")


        # Volatility check
        if volatility in ["NORMAL", "LOW"]:
            safety_score += 20
            reasons.append("VOLATILITY SAFE")
        else:
            reasons.append("VOLATILITY HIGH")


        # Spread check
        if spread <= 0.50:
            safety_score += 15
            reasons.append("SPREAD ACCEPTABLE")
        else:
            reasons.append("SPREAD TOO HIGH")



        if safety_score >= 80:

            status = "TRADE SAFE"

        elif safety_score >= 50:

            status = "TRADE CAUTION"

        else:

            status = "TRADE BLOCKED"



        result = {

            "status": status,
            "safety_score": safety_score,
            "decision": decision,
            "confidence": confidence,
            "risk_reward": risk_reward,
            "volatility": volatility,
            "spread": spread,
            "reasons": reasons,
            "timestamp": datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }


        print("==============================")
        print("GSIS SAFETY RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":

    engine = TradeSafetyGovernorEngine()

    engine.validate(
        decision="APPROVED",
        confidence=70,
        risk_reward=2,
        volatility="NORMAL",
        spread=0.29
    )
