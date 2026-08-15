import datetime


class AdaptiveCapitalEngine:

    def __init__(self):
        print("==============================")
        print("GSIS ADAPTIVE CAPITAL ENGINE v1.0 ONLINE")
        print("DYNAMIC CAPITAL ALLOCATION CONTROL ACTIVE")
        print("==============================")


    def evaluate_capital(self, performance):

        win_rate = performance.get("win_rate", 0)
        total = performance.get("total_trades", 0)

        if total < 5:
            risk_multiplier = 0.5
            status = "INITIAL LEARNING MODE"

        elif win_rate >= 70:
            risk_multiplier = 1.5
            status = "CAPITAL INCREASE APPROVED"

        elif win_rate >= 50:
            risk_multiplier = 1
            status = "NORMAL CAPITAL MODE"

        else:
            risk_multiplier = 0.5
            status = "CAPITAL REDUCTION ACTIVE"


        result = {

            "status": "CAPITAL ANALYSIS COMPLETE",
            "trade_history": total,
            "win_rate": win_rate,
            "risk_multiplier": risk_multiplier,
            "capital_status": status,
            "timestamp": datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }

        print("==============================")
        print("GSIS CAPITAL RESULT")
        print("==============================")
        print(result)

        return result



if __name__ == "__main__":

    engine = AdaptiveCapitalEngine()

    test = {
        "total_trades": 10,
        "win_rate": 60
    }

    engine.evaluate_capital(test)
