class PositionSizingEngine:


    def __init__(self):

        print("==============================")
        print("GSIS POSITION SIZING ENGINE v2.0 ONLINE")
        print("==============================")
        print("INSTITUTIONAL CAPITAL CONTROL ACTIVE")
        print("==============================")


    def calculate(
        self,
        symbol,
        balance,
        risk_percent,
        entry,
        stop_loss
    ):


        risk_amount = balance * (
            risk_percent / 100
        )


        stop_distance = abs(
            entry - stop_loss
        )


        if stop_distance <= 0:

            return {

                "symbol": symbol,

                "status": "BLOCKED",

                "reason": "INVALID STOP DISTANCE"

            }



        # ==============================
        # GOLD CONTRACT CALCULATION
        # ==============================

        value_per_point = 100


        raw_lot = (
            risk_amount /
            (stop_distance * value_per_point)
        )



        # ==============================
        # INSTITUTIONAL LIMITS
        # ==============================

        minimum_stop = 0.10

        maximum_lot = 5.0



        if stop_distance < minimum_stop:

            adjusted_stop = minimum_stop

            raw_lot = (
                risk_amount /
                (adjusted_stop * value_per_point)
            )



        approved_lot = min(
            round(raw_lot, 2),
            maximum_lot
        )



        adjustment = False


        if approved_lot < raw_lot:

            adjustment = True



        result = {


            "symbol":

            symbol,


            "account_balance":

            balance,


            "risk_percent":

            risk_percent,


            "risk_amount":

            round(
                risk_amount,
                2
            ),


            "entry":

            entry,


            "stop_loss":

            stop_loss,


            "stop_distance":

            round(
                stop_distance,
                2
            ),


            "requested_lot":

            round(
                raw_lot,
                2
            ),


            "approved_lot":

            approved_lot,


            "maximum_allowed_lot":

            maximum_lot,


            "adjusted":

            adjustment,


            "status":

            "APPROVED"

        }


        print("==============================")
        print("GSIS POSITION SIZE RESULT")
        print("==============================")

        print(result)


        return result
