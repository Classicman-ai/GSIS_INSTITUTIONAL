import datetime


class AdaptiveConfidenceEngine:


    def __init__(self):

        print("==============================")
        print("GSIS ADAPTIVE CONFIDENCE ENGINE v2.0 ONLINE")
        print("DYNAMIC CONFIDENCE INTELLIGENCE ACTIVE")
        print("==============================")


    def evaluate(
        self,
        pattern_score,
        historical_win_rate,
        risk_score,
        regime_score
    ):


        score = 0


        # Pattern intelligence
        if pattern_score >= 70:
            score += 30
        elif pattern_score >= 50:
            score += 20
        else:
            score += 10



        # Historical performance
        if historical_win_rate >= 70:
            score += 30
        elif historical_win_rate >= 50:
            score += 20
        else:
            score += 10



        # Risk validation
        if risk_score >= 80:
            score += 20
        else:
            score += 10



        # Market regime
        if regime_score >= 80:
            score += 20
        else:
            score += 10



        if score >= 80:

            decision="HIGH CONFIDENCE"

        elif score >= 60:

            decision="ACCEPTABLE"

        else:

            decision="CAUTION"



        result={

            "adaptive_confidence":
            score,

            "decision":
            decision,

            "inputs":{

                "pattern_score":pattern_score,
                "historical_win_rate":historical_win_rate,
                "risk_score":risk_score,
                "regime_score":regime_score

            },

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



if __name__=="__main__":

    engine=AdaptiveConfidenceEngine()

    engine.evaluate(
        66,
        0,
        80,
        80
    )
