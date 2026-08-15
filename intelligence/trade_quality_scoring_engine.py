import datetime


class TradeQualityScoringEngine:

    def __init__(self):

        print("==============================")
        print("GSIS TRADE QUALITY SCORING ENGINE v1.0 ONLINE")
        print("FINAL TRADE QUALITY EVALUATION ACTIVE")
        print("==============================")


    def evaluate(
        self,
        pattern_score,
        confidence,
        risk_score,
        market_score,
        position_score
    ):

        reasons = []

        total = (

            pattern_score +
            confidence +
            risk_score +
            market_score +
            position_score

        ) / 5


        if pattern_score >= 60:

            reasons.append(
                "PATTERN QUALITY ACCEPTED"
            )

        else:

            reasons.append(
                "PATTERN QUALITY WEAK"
            )


        if confidence >= 70:

            reasons.append(
                "CONFIDENCE ACCEPTED"
            )

        else:

            reasons.append(
                "CONFIDENCE LOW"
            )


        if risk_score >= 80:

            reasons.append(
                "RISK ACCEPTED"
            )

        else:

            reasons.append(
                "RISK WARNING"
            )


        if market_score >= 80:

            reasons.append(
                "MARKET ACCEPTED"
            )

        else:

            reasons.append(
                "MARKET WARNING"
            )


        if position_score >= 80:

            reasons.append(
                "POSITION ACCEPTED"
            )

        else:

            reasons.append(
                "POSITION WARNING"
            )


        quality_score = round(
            total,
            2
        )


        if quality_score >= 85:

            decision = "A+ TRADE"

        elif quality_score >= 70:

            decision = "APPROVED TRADE"

        elif quality_score >= 50:

            decision = "CAUTION TRADE"

        else:

            decision = "REJECT TRADE"



        result = {

            "status":
                "QUALITY ANALYSIS COMPLETE",

            "decision":
                decision,

            "quality_score":
                quality_score,

            "inputs":
            {
                "pattern":
                    pattern_score,

                "confidence":
                    confidence,

                "risk":
                    risk_score,

                "market":
                    market_score,

                "position":
                    position_score
            },

            "reasons":
                reasons,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS QUALITY RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = TradeQualityScoringEngine()


    engine.evaluate(

        pattern_score=66,

        confidence=70,

        risk_score=100,

        market_score=100,

        position_score=100

    )
