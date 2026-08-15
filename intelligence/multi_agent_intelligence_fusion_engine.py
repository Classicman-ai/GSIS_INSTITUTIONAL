import datetime


class MultiAgentIntelligenceFusionEngine:

    def __init__(self):

        print("==============================")
        print("GSIS MULTI-AGENT INTELLIGENCE FUSION ENGINE v1.0 ONLINE")
        print("COLLECTIVE AI DECISION LAYER ACTIVE")
        print("==============================")


    def fuse(
        self,
        market_score,
        pattern_score,
        confidence_score,
        risk_score,
        strategy_score
    ):

        total_score = 0
        reasons = []


        # Market agent

        if market_score >= 60:

            total_score += 20
            reasons.append(
                "MARKET AGENT APPROVED"
            )

        else:

            reasons.append(
                "MARKET AGENT WEAK"
            )


        # Pattern agent

        if pattern_score >= 60:

            total_score += 20
            reasons.append(
                "PATTERN AGENT APPROVED"
            )

        else:

            reasons.append(
                "PATTERN AGENT WEAK"
            )


        # Confidence agent

        if confidence_score >= 70:

            total_score += 20
            reasons.append(
                "CONFIDENCE AGENT APPROVED"
            )

        else:

            reasons.append(
                "CONFIDENCE AGENT WEAK"
            )


        # Risk agent

        if risk_score >= 70:

            total_score += 20
            reasons.append(
                "RISK AGENT APPROVED"
            )

        else:

            reasons.append(
                "RISK AGENT WEAK"
            )


        # Strategy agent

        if strategy_score >= 50:

            total_score += 20
            reasons.append(
                "STRATEGY AGENT APPROVED"
            )

        else:

            reasons.append(
                "STRATEGY AGENT WEAK"
            )



        if total_score >= 80:

            decision = "INSTITUTIONAL APPROVAL"

        elif total_score >= 50:

            decision = "CAUTION REVIEW"

        else:

            decision = "TRADE REJECT"



        result = {

            "status":
                "MULTI AGENT FUSION COMPLETE",

            "fusion_score":
                total_score,

            "decision":
                decision,

            "agents":

            {
                "market":
                    market_score,

                "pattern":
                    pattern_score,

                "confidence":
                    confidence_score,

                "risk":
                    risk_score,

                "strategy":
                    strategy_score
            },

            "reasons":
                reasons,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS MULTI AGENT RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = MultiAgentIntelligenceFusionEngine()


    engine.fuse(

        market_score=80,

        pattern_score=66,

        confidence_score=70,

        risk_score=100,

        strategy_score=50

    )
