import datetime


class FinalApprovalGateEngine:

    def __init__(self):

        print("==============================")
        print("GSIS FINAL APPROVAL GATE ENGINE v1.0 ONLINE")
        print("INSTITUTIONAL EXECUTION AUTHORITY ACTIVE")
        print("==============================")


    def approve(
        self,
        confidence_result,
        decision_result,
        portfolio_result,
        capital_result,
        market_result,
        event_result
    ):

        score = 100
        reasons = []


        if confidence_result >= 70:

            reasons.append(
                "CONFIDENCE ACCEPTED"
            )

        else:

            score -= 25

            reasons.append(
                "LOW CONFIDENCE"
            )



        if decision_result == "APPROVED":

            reasons.append(
                "DECISION GOVERNOR APPROVED"
            )

        else:

            score -= 30

            reasons.append(
                "DECISION GOVERNOR REJECTED"
            )



        if portfolio_result == "PORTFOLIO APPROVED":

            reasons.append(
                "PORTFOLIO RISK ACCEPTED"
            )

        else:

            score -= 25

            reasons.append(
                "PORTFOLIO RISK FAILED"
            )



        if capital_result == "CAPITAL APPROVED":

            reasons.append(
                "CAPITAL PROTECTION ACCEPTED"
            )

        else:

            score -= 25

            reasons.append(
                "CAPITAL PROTECTION FAILED"
            )



        if market_result == "MARKET APPROVED":

            reasons.append(
                "MARKET CONDITION ACCEPTED"
            )

        else:

            score -= 20

            reasons.append(
                "MARKET CONDITION FAILED"
            )



        if event_result == "EVENT RISK APPROVED":

            reasons.append(
                "EVENT RISK ACCEPTED"
            )

        else:

            score -= 20

            reasons.append(
                "EVENT RISK FAILED"
            )



        if score >= 80:

            decision = "FINAL APPROVAL"

        else:

            decision = "FINAL REJECTION"



        result = {

            "status":
                "FINAL GATE COMPLETE",

            "decision":
                decision,

            "approval_score":
                score,

            "reasons":
                reasons,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS FINAL GATE RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = FinalApprovalGateEngine()


    engine.approve(

        confidence_result=70,

        decision_result="APPROVED",

        portfolio_result="PORTFOLIO APPROVED",

        capital_result="CAPITAL APPROVED",

        market_result="MARKET APPROVED",

        event_result="EVENT RISK APPROVED"

    )
