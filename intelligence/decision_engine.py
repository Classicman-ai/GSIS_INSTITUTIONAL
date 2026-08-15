# ==========================================================
# GSIS DECISION ENGINE v1.1
# XAUUSD Institutional Decision Layer
# ==========================================================


class DecisionEngine:


    def __init__(self):

        print("==============================")
        print("GSIS DECISION ENGINE v1.1 ONLINE")
        print("==============================")



    def analyze(self, regime):


        symbol = regime.get(
            "symbol",
            "XAUUSD"
        )


        trend = regime.get(
            "trend",
            "NEUTRAL"
        )


        momentum = regime.get(
            "momentum",
            "STABLE"
        )


        confidence = regime.get(
            "confidence",
            0
        )


        market_regime = regime.get(
            "regime",
            "UNKNOWN"
        )



        if (
            trend == "ACTIVE"
            and confidence >= 75
        ):

            decision = "BUY"

            reason = (
                "Institutional trend alignment detected"
            )


        else:

            decision = "WAIT"

            reason = (
                "Market structure is not favorable"
            )



        result = {

            "symbol": symbol,

            "decision": decision,

            "reason": reason,

            "regime": market_regime,

            "trend": trend,

            "momentum": momentum,

            "confidence": confidence

        }



        print("==============================")
        print("GSIS MARKET DECISION")
        print("==============================")

        print(result)



        return result




engine = DecisionEngine()
