import datetime


class CapitalProtectionEngine:

    def __init__(self):

        print("==============================")
        print("GSIS CAPITAL PROTECTION ENGINE v2.0 ONLINE")
        print("ACCOUNT SAFETY CONTROL ACTIVE")
        print("==============================")


    def evaluate(
        self,
        account_balance,
        risk_amount,
        daily_loss,
        max_daily_loss
    ):

        score = 100
        reasons = []


        if account_balance > 0:

            reasons.append(
                "ACCOUNT BALANCE VALID"
            )

        else:

            score -= 50

            reasons.append(
                "INVALID ACCOUNT BALANCE"
            )



        risk_percent = (
            risk_amount /
            account_balance
        ) * 100



        if risk_percent <= 2:

            reasons.append(
                "RISK LEVEL SAFE"
            )

        else:

            score -= 30

            reasons.append(
                "RISK LEVEL TOO HIGH"
            )



        if daily_loss < max_daily_loss:

            reasons.append(
                "DAILY LOSS LIMIT SAFE"
            )

        else:

            score -= 40

            reasons.append(
                "DAILY LOSS LIMIT BREACHED"
            )



        if score >= 80:

            decision = "CAPITAL APPROVED"

        elif score >= 50:

            decision = "CAPITAL CAUTION"

        else:

            decision = "CAPITAL BLOCKED"



        result = {

            "status":
                "CAPITAL ANALYSIS COMPLETE",

            "decision":
                decision,

            "capital_score":
                score,

            "risk_percent":
                round(
                    risk_percent,
                    2
                ),

            "account_balance":
                account_balance,

            "risk_amount":
                risk_amount,

            "reasons":
                reasons,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS CAPITAL RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = CapitalProtectionEngine()


    engine.evaluate(

        account_balance=10000,

        risk_amount=100,

        daily_loss=0,

        max_daily_loss=500

    )
