import datetime


class AdaptiveStrategyEngine:

    def __init__(self):
        print("==============================")
        print("GSIS ADAPTIVE STRATEGY ENGINE v1.0 ONLINE")
        print("AUTONOMOUS STRATEGY ADJUSTMENT ACTIVE")
        print("==============================")


    def optimize(self, optimization_result):

        win_rate = optimization_result.get("win_rate", 0)
        strategy_status = optimization_result.get(
            "strategy_status",
            "UNKNOWN"
        )

        confidence_modifier = 0

        if win_rate >= 70:
            confidence_modifier = 10
            action = "INCREASE CONFIDENCE"

        elif win_rate >= 50:
            confidence_modifier = 0
            action = "MAINTAIN CONFIDENCE"

        else:
            confidence_modifier = -10
            action = "REDUCE CONFIDENCE"


        result = {

            "status": "ADAPTATION COMPLETE",

            "strategy_status": strategy_status,

            "win_rate": win_rate,

            "confidence_modifier":
                confidence_modifier,

            "recommended_action":
                action,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS ADAPTIVE RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":

    engine = AdaptiveStrategyEngine()

    test = {

        "win_rate": 0,

        "strategy_status":
            "STRATEGY WEAK"

    }


    engine.optimize(test)
