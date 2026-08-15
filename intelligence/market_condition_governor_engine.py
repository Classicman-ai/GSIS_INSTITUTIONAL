import datetime


class MarketConditionGovernorEngine:

    def __init__(self):

        print("==============================")
        print("GSIS MARKET CONDITION GOVERNOR ENGINE v1.0 ONLINE")
        print("MARKET QUALITY CONTROL ACTIVE")
        print("==============================")


    def evaluate(
        self,
        volatility,
        liquidity,
        spread,
        session_quality
    ):

        score = 100
        reasons = []


        if volatility == "NORMAL":

            reasons.append(
                "VOLATILITY ACCEPTABLE"
            )

        elif volatility == "HIGH":

            score -= 20

            reasons.append(
                "HIGH VOLATILITY"
            )

        else:

            score -= 40

            reasons.append(
                "EXTREME VOLATILITY"
            )



        if liquidity == "ACTIVE":

            reasons.append(
                "LIQUIDITY AVAILABLE"
            )

        else:

            score -= 25

            reasons.append(
                "LOW LIQUIDITY"
            )



        if spread <= 0.5:

            reasons.append(
                "SPREAD ACCEPTABLE"
            )

        else:

            score -= 20

            reasons.append(
                "SPREAD TOO HIGH"
            )



        if session_quality == "GOOD":

            reasons.append(
                "SESSION QUALITY GOOD"
            )

        else:

            score -= 15

            reasons.append(
                "SESSION QUALITY WARNING"
            )



        if score >= 80:

            decision = "MARKET APPROVED"

        elif score >= 50:

            decision = "MARKET CAUTION"

        else:

            decision = "MARKET BLOCKED"



        result = {

            "status":
                "MARKET CONDITION COMPLETE",

            "decision":
                decision,

            "market_score":
                score,

            "reasons":
                reasons,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS MARKET CONDITION RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = MarketConditionGovernorEngine()


    engine.evaluate(

        volatility="NORMAL",

        liquidity="ACTIVE",

        spread=0.29,

        session_quality="GOOD"

    )
