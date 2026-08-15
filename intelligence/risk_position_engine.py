from datetime import datetime, timezone


class RiskPositionEngine:

    def __init__(self):

        self.default_risk = 1.0

        print("==============================")
        print("GSIS RISK POSITION ENGINE v2.0 ONLINE")
        print("DYNAMIC RISK + POSITION CONTROL ACTIVE")
        print("==============================")


    def calculate_position(
        self,
        signal,
        balance=10000,
        risk_percent=1
    ):

        entry = signal.get("entry")
        stop_loss = signal.get("stop_loss")
        take_profit = signal.get("tp1")

        risk_amount = balance * (risk_percent / 100)

        distance = abs(entry - stop_loss)

        if distance == 0:
            lot_size = 0
        else:
            lot_size = round(
                risk_amount / (distance * 100),
                2
            )


        result = {

            "symbol": signal.get("symbol"),

            "direction": signal.get("direction"),

            "entry": entry,

            "stop_loss": stop_loss,

            "take_profit": take_profit,

            "tp_targets": {

                "TP1": take_profit,

                "TP2": round(
                    entry - (distance * 2), 2
                ) if signal.get("direction") == "SELL"
                else round(
                    entry + (distance * 2), 2
                ),

                "TP3": round(
                    entry - (distance * 3), 2
                ) if signal.get("direction") == "SELL"
                else round(
                    entry + (distance * 3), 2
                )

            },

            "risk_percent": risk_percent,

            "risk_amount": risk_amount,

            "lot_size": lot_size,

            "break_even_trigger":
                round(distance * 1.5,2),

            "trailing_distance":
                round(distance,2),

            "timestamp":
                datetime.now(timezone.utc).isoformat()

        }


        print("==============================")
        print("GSIS POSITION CALCULATION")
        print("==============================")
        print(result)


        return result



    def manage_risk(self, trade, current_price):

        entry = trade.get("entry")
        stop = trade.get("stop_loss")
        direction = trade.get("direction")


        if direction == "SELL":

            profit = entry - current_price

        else:

            profit = current_price - entry



        action = "HOLD"


        if profit > abs(entry-stop):

            action = "MOVE STOP TO BREAK EVEN"


        result = {

            "trade_id":trade.get("trade_id"),

            "current_price":current_price,

            "profit":round(profit,2),

            "action":action,

            "timestamp":
            datetime.now(timezone.utc).isoformat()

        }


        print("==============================")
        print("GSIS RISK MANAGEMENT RESULT")
        print("==============================")
        print(result)


        return result


    calculate = calculate_position
    update = manage_risk
