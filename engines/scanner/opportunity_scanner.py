"""
GSIS OPPORTUNITY SCANNER ENGINE v1.0

Purpose:
- Scan multiple assets
- Rank opportunities
- Filter weak markets
- Create trading watchlist

Ranking:
Fusion Score
Confidence
Market Regime
Risk Condition
"""


from datetime import datetime, timezone



class OpportunityScanner:


    def __init__(self):

        self.version = "1.0"



    def scan(
        self,
        markets
    ):


        results = []



        for market in markets:


            score = 0
            reasons = []



            symbol = market["symbol"]

            confidence = market["confidence"]

            fusion = market["fusion_score"]

            regime = market["regime"]



            # Confidence scoring

            if confidence >= 0.80:

                score += 3

                reasons.append(
                    "HIGH CONFIDENCE"
                )


            elif confidence >= 0.70:

                score += 2

            else:

                reasons.append(
                    "LOW CONFIDENCE"
                )



            # Fusion scoring

            if fusion >= 8:

                score += 4

                reasons.append(
                    "STRONG FUSION"
                )


            elif fusion >= 5:

                score += 2


            else:

                reasons.append(
                    "WEAK FUSION"
                )



            # Regime

            if regime in [
                "TRENDING_UP",
                "TRENDING_DOWN"
            ]:

                score += 2

                reasons.append(
                    "TREND REGIME"
                )


            else:

                reasons.append(
                    "NON TREND"
                )



            # Classification


            if score >= 8:

                status = "PRIME_SETUP"

                grade = "A"



            elif score >= 5:

                status = "WATCHLIST"

                grade = "B"



            else:

                status = "IGNORE"

                grade = "C"



            results.append({

                "symbol":
                symbol,


                "opportunity_score":
                score,


                "grade":
                grade,


                "status":
                status,


                "reasons":
                reasons

            })



        # Highest score first

        results.sort(
            key=lambda x:x["opportunity_score"],
            reverse=True
        )



        return {

            "engine":
            "GSIS OPPORTUNITY SCANNER",


            "version":
            self.version,


            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),


            "market_count":
            len(markets),


            "ranking":
            results

        }



if __name__ == "__main__":


    scanner = OpportunityScanner()


    markets = [

        {
            "symbol":"BTCUSDT",
            "confidence":0.84,
            "fusion_score":8,
            "regime":"TRENDING_UP"
        },

        {
            "symbol":"ETHUSDT",
            "confidence":0.52,
            "fusion_score":4,
            "regime":"RANGE"
        },

        {
            "symbol":"XAUTUSDT",
            "confidence":0.78,
            "fusion_score":7,
            "regime":"TRENDING_DOWN"
        }

    ]


    print(
        scanner.scan(markets)
    )
