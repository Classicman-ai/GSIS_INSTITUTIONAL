class TradePlannerEngine:

    def __init__(self):

        print("==============================")
        print("GSIS TRADE PLANNER ENGINE v1.0 ONLINE")
        print("==============================")
        print("INSTITUTIONAL EXECUTION PLANNING ACTIVE")
        print("==============================")


    def plan(
        self,
        validator,
        order_block,
        fvg
    ):

        if validator.get("status") != "APPROVED":

            result = {
                "symbol": validator.get("symbol"),
                "status": "REJECTED",
                "reason": "Trade not approved by validator"
            }

            print("==============================")
            print("GSIS TRADE PLAN")
            print("==============================")
            print(result)

            return result


        direction = validator["direction"]


        if direction == "BUY":

            entry = fvg["gap_low"]

            stop_loss = order_block["low"] - 0.20

            risk = entry - stop_loss

            tp1 = round(entry + risk, 2)

            tp2 = round(entry + (risk * 2), 2)

            tp3 = round(entry + (risk * 3), 2)


        else:

            entry = fvg["gap_high"]

            stop_loss = order_block["high"] + 0.20

            risk = stop_loss - entry

            tp1 = round(entry - risk, 2)

            tp2 = round(entry - (risk * 2), 2)

            tp3 = round(entry - (risk * 3), 2)


        result = {

            "symbol": validator["symbol"],

            "direction": direction,

            "entry": round(entry, 2),

            "stop_loss": round(stop_loss, 2),

            "tp1": tp1,

            "tp2": tp2,

            "tp3": tp3,

            "risk_reward": "1:3",

            "order_type": "MARKET",

            "status": "READY",

            "confidence": validator["confidence"]

        }


        print("==============================")
        print("GSIS TRADE PLAN")
        print("==============================")
        print(result)

        return result
