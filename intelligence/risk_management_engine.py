class RiskManagementEngine:

    def __init__(self):

        print("==============================")
        print("GSIS RISK MANAGEMENT ENGINE v1.0 ONLINE")
        print("==============================")
        print("INSTITUTIONAL RISK CONTROL ACTIVE")
        print("==============================")


    def evaluate(
        self,
        position
    ):

        symbol = position.get(
            "symbol",
            "UNKNOWN"
        )

        lot_size = position.get(
            "lot_size",
            0
        )

        risk_amount = position.get(
            "risk_amount",
            0
        )

        balance = position.get(
            "account_balance",
            0
        )


        max_risk_percent = 1.0

        max_lot_size = 5.0


        risk_percent = 0

        if balance > 0:

            risk_percent = (
                risk_amount / balance
            ) * 100



        reasons = []


        status = "APPROVED"



        if risk_percent > max_risk_percent:

            status = "BLOCKED"

            reasons.append(
                "RISK PERCENT ABOVE LIMIT"
            )


        if lot_size > max_lot_size:

            status = "BLOCKED"

            reasons.append(
                "POSITION SIZE TOO LARGE"
            )


        if status == "APPROVED":

            reasons.append(
                "RISK PARAMETERS ACCEPTED"
            )



        result = {

            "symbol": symbol,

            "requested_lot": lot_size,

            "risk_amount": risk_amount,

            "risk_percent": round(
                risk_percent,
                2
            ),

            "max_allowed_lot": max_lot_size,

            "max_allowed_risk_percent": max_risk_percent,

            "status": status,

            "reasons": reasons

        }



        print("==============================")
        print("GSIS RISK EVALUATION")
        print("==============================")
        print(result)


        return result
