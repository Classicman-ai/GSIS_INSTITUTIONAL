import datetime


class EventRiskIntelligenceEngine:

    def __init__(self):

        print("==============================")
        print("GSIS EVENT RISK INTELLIGENCE ENGINE v2.0 ONLINE")
        print("MACRO EVENT RISK CONTROL ACTIVE")
        print("==============================")


    def evaluate(
        self,
        high_impact_event,
        volatility_state,
        market_disruption
    ):

        score = 100
        reasons = []


        if high_impact_event:

            score -= 40

            reasons.append(
                "HIGH IMPACT EVENT DETECTED"
            )

        else:

            reasons.append(
                "NO MAJOR EVENT DETECTED"
            )



        if volatility_state == "EXTREME":

            score -= 30

            reasons.append(
                "EXTREME VOLATILITY WARNING"
            )

        elif volatility_state == "HIGH":

            score -= 15

            reasons.append(
                "HIGH VOLATILITY WARNING"
            )

        else:

            reasons.append(
                "VOLATILITY ACCEPTABLE"
            )



        if market_disruption:

            score -= 30

            reasons.append(
                "MARKET DISRUPTION DETECTED"
            )

        else:

            reasons.append(
                "MARKET STRUCTURE STABLE"
            )



        if score >= 80:

            decision = "EVENT RISK APPROVED"

        elif score >= 50:

            decision = "EVENT RISK CAUTION"

        else:

            decision = "EVENT RISK BLOCKED"



        result = {

            "status":
                "EVENT RISK ANALYSIS COMPLETE",

            "decision":
                decision,

            "risk_score":
                score,

            "conditions":
            {
                "high_impact_event":
                    high_impact_event,

                "volatility":
                    volatility_state,

                "market_disruption":
                    market_disruption
            },

            "reasons":
                reasons,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS EVENT RISK RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = EventRiskIntelligenceEngine()


    engine.evaluate(

        high_impact_event=False,

        volatility_state="NORMAL",

        market_disruption=False

    )
