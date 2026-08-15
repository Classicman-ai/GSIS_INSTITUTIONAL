import datetime


class PortfolioRiskGovernorEngine:

    def __init__(self):

        print("==============================")
        print("GSIS PORTFOLIO RISK GOVERNOR ENGINE v1.0 ONLINE")
        print("MULTI POSITION RISK CONTROL ACTIVE")
        print("==============================")


    def evaluate(
        self,
        account_balance,
        total_exposure,
        max_exposure,
        open_positions,
        max_positions,
        symbols
    ):

        risk_score = 100
        reasons = []


        if total_exposure > max_exposure:

            risk_score -= 40
            reasons.append(
                "EXPOSURE LIMIT BREACHED"
            )

        else:

            reasons.append(
                "EXPOSURE ACCEPTABLE"
            )


        if open_positions > max_positions:

            risk_score -= 30
            reasons.append(
                "POSITION LIMIT BREACHED"
            )

        else:

            reasons.append(
                "POSITION COUNT SAFE"
            )


        if len(set(symbols)) == 1 and open_positions > 3:

            risk_score -= 20
            reasons.append(
                "SYMBOL CONCENTRATION WARNING"
            )

        else:

            reasons.append(
                "SYMBOL DISTRIBUTION SAFE"
            )


        if risk_score >= 80:

            decision = "PORTFOLIO APPROVED"

        elif risk_score >= 50:

            decision = "PORTFOLIO CAUTION"

        else:

            decision = "PORTFOLIO BLOCKED"


        result = {

            "status":
                "RISK GOVERNANCE COMPLETE",

            "decision":
                decision,

            "risk_score":
                risk_score,

            "account_balance":
                account_balance,

            "total_exposure":
                total_exposure,

            "open_positions":
                open_positions,

            "max_positions":
                max_positions,

            "symbols":
                symbols,

            "reasons":
                reasons,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS PORTFOLIO RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":

    engine = PortfolioRiskGovernorEngine()

    engine.evaluate(
        account_balance=10000,
        total_exposure=1,
        max_exposure=5,
        open_positions=1,
        max_positions=5,
        symbols=["XAUUSD"]
    )
