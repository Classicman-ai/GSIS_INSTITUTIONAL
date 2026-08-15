import datetime


class MarketRegimeDecisionEngine:

    def __init__(self):

        print("==============================")
        print("GSIS MARKET REGIME DECISION ENGINE v1.0 ONLINE")
        print("MARKET ENVIRONMENT INTELLIGENCE ACTIVE")
        print("==============================")


    def analyze(
        self,
        volatility,
        trend_strength,
        liquidity
    ):

        score = 0
        conditions = []


        if volatility == "NORMAL":

            score += 30
            conditions.append(
                "VOLATILITY STABLE"
            )

        elif volatility == "HIGH":

            score -= 20
            conditions.append(
                "HIGH VOLATILITY WARNING"
            )


        if trend_strength >= 60:

            score += 30
            conditions.append(
                "TREND CONFIRMED"
            )

        else:

            conditions.append(
                "WEAK TREND"
            )


        if liquidity == "ACTIVE":

            score += 40
            conditions.append(
                "LIQUIDITY AVAILABLE"
            )

        else:

            score -= 20
            conditions.append(
                "LOW LIQUIDITY"
            )


        if score >= 70:

            regime = "FAVORABLE MARKET"

        elif score >= 40:

            regime = "CAUTION MARKET"

        else:

            regime = "UNFAVORABLE MARKET"


        result = {

            "status":
                "MARKET REGIME COMPLETE",

            "market_regime":
                regime,

            "regime_score":
                score,

            "volatility":
                volatility,

            "trend_strength":
                trend_strength,

            "liquidity":
                liquidity,

            "conditions":
                conditions,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS MARKET REGIME RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":

    engine = MarketRegimeDecisionEngine()

    engine.analyze(
        volatility="NORMAL",
        trend_strength=70,
        liquidity="ACTIVE"
    )
