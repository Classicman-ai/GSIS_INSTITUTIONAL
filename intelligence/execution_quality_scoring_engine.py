import datetime


class ExecutionQualityScoringEngine:

    def __init__(self):

        print("==============================")
        print("GSIS EXECUTION QUALITY SCORING ENGINE v1.0 ONLINE")
        print("TRADE QUALITY INTELLIGENCE ACTIVE")
        print("==============================")


    def evaluate(
        self,
        pattern_score,
        confidence,
        risk_reward,
        market_score
    ):

        quality_score = 0
        reasons = []


        if pattern_score >= 60:

            quality_score += 25

            reasons.append(
                "PATTERN QUALITY ACCEPTED"
            )

        else:

            reasons.append(
                "WEAK PATTERN"
            )



        if confidence >= 70:

            quality_score += 25

            reasons.append(
                "CONFIDENCE ACCEPTED"
            )

        else:

            reasons.append(
                "LOW CONFIDENCE"
            )



        if risk_reward >= 1.5:

            quality_score += 25

            reasons.append(
                "RISK REWARD ACCEPTED"
            )

        else:

            reasons.append(
                "POOR RISK REWARD"
            )



        if market_score >= 80:

            quality_score += 25

            reasons.append(
                "MARKET CONDITIONS ACCEPTED"
            )

        else:

            reasons.append(
                "MARKET CONDITIONS WEAK"
            )



        if quality_score >= 80:

            decision = "HIGH QUALITY TRADE"

        elif quality_score >= 50:

            decision = "MEDIUM QUALITY TRADE"

        else:

            decision = "LOW QUALITY TRADE"



        result = {

            "status":
                "QUALITY ANALYSIS COMPLETE",

            "quality_score":
                quality_score,

            "decision":
                decision,

            "reasons":
                reasons,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS QUALITY RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = ExecutionQualityScoringEngine()


    engine.evaluate(

        pattern_score=66,

        confidence=70,

        risk_reward=1.5,

        market_score=100

    )
