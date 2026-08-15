import datetime


class StrategyValidationEngine:

    def __init__(self):

        print("==============================")
        print("GSIS STRATEGY VALIDATION ENGINE v1.0 ONLINE")
        print("STRATEGY INTEGRITY CONTROL ACTIVE")
        print("==============================")


    def validate(
        self,
        direction,
        pattern_score,
        confidence,
        stop_loss,
        take_profit,
        entry
    ):

        score = 100
        reasons = []


        if direction in ["BUY", "SELL"]:

            reasons.append(
                "DIRECTION VALID"
            )

        else:

            score -= 30

            reasons.append(
                "INVALID DIRECTION"
            )



        if pattern_score >= 60:

            reasons.append(
                "PATTERN CONFIRMED"
            )

        else:

            score -= 25

            reasons.append(
                "WEAK PATTERN"
            )



        if confidence >= 70:

            reasons.append(
                "CONFIDENCE ACCEPTED"
            )

        else:

            score -= 25

            reasons.append(
                "LOW CONFIDENCE"
            )



        risk_distance = abs(
            entry - stop_loss
        )

        reward_distance = abs(
            take_profit - entry
        )


        if reward_distance > risk_distance:

            reasons.append(
                "REWARD STRUCTURE VALID"
            )

        else:

            score -= 20

            reasons.append(
                "POOR REWARD STRUCTURE"
            )



        if score >= 80:

            decision = "STRATEGY VALIDATED"

        elif score >= 50:

            decision = "STRATEGY CAUTION"

        else:

            decision = "STRATEGY REJECTED"



        result = {

            "status":
                "STRATEGY VALIDATION COMPLETE",

            "decision":
                decision,

            "validation_score":
                score,

            "reasons":
                reasons,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS STRATEGY VALIDATION RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = StrategyValidationEngine()


    engine.validate(

        direction="SELL",

        pattern_score=66,

        confidence=70,

        entry=2387.5,

        stop_loss=2387.8,

        take_profit=2387.2

    )
