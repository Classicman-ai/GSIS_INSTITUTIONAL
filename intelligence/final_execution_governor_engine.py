import datetime


class FinalExecutionGovernorEngine:

    def __init__(self):

        print("==============================")
        print("GSIS FINAL EXECUTION GOVERNOR ENGINE v1.0 ONLINE")
        print("INSTITUTIONAL EXECUTION CONTROL ACTIVE")
        print("==============================")


    def authorize(
        self,
        intelligence_score,
        safety_score,
        capital_score,
        portfolio_score
    ):

        execution_score = 0
        reasons = []


        if intelligence_score >= 70:

            execution_score += 25
            reasons.append(
                "INTELLIGENCE APPROVED"
            )

        else:

            reasons.append(
                "INTELLIGENCE WEAK"
            )


        if safety_score >= 80:

            execution_score += 25
            reasons.append(
                "SAFETY APPROVED"
            )

        else:

            reasons.append(
                "SAFETY WARNING"
            )


        if capital_score >= 80:

            execution_score += 25
            reasons.append(
                "CAPITAL PROTECTION APPROVED"
            )

        else:

            reasons.append(
                "CAPITAL WARNING"
            )


        if portfolio_score >= 80:

            execution_score += 25
            reasons.append(
                "PORTFOLIO APPROVED"
            )

        else:

            reasons.append(
                "PORTFOLIO WARNING"
            )


        if execution_score >= 80:

            decision = "EXECUTION APPROVED"

        elif execution_score >= 50:

            decision = "EXECUTION CAUTION"

        else:

            decision = "EXECUTION BLOCKED"



        result = {

            "status":
                "EXECUTION GOVERNANCE COMPLETE",

            "decision":
                decision,

            "execution_score":
                execution_score,

            "components":
            {
                "intelligence":
                    intelligence_score,

                "safety":
                    safety_score,

                "capital":
                    capital_score,

                "portfolio":
                    portfolio_score
            },

            "reasons":
                reasons,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS FINAL EXECUTION RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":

    engine = FinalExecutionGovernorEngine()


    engine.authorize(

        intelligence_score=80,

        safety_score=100,

        capital_score=100,

        portfolio_score=100

    )
