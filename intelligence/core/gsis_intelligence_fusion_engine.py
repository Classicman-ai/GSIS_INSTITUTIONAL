import datetime


class GSISIntelligenceFusionEngine:

    def __init__(self):

        print("==============================")
        print("GSIS INTELLIGENCE FUSION ENGINE v1.0 ONLINE")
        print("MULTI ENGINE DECISION SYNTHESIS ACTIVE")
        print("==============================")


    def analyze(

        self,

        structure,

        zone,

        liquidity,

        candlestick,

        chart_pattern,

        economic,

        historical_probability,

        calibrated_confidence

    ):


        score = 0

        reasons = []


        # Market structure

        if structure.get("bos"):

            score += 15

            reasons.append(
                "BREAK OF STRUCTURE CONFIRMED"
            )


        if structure.get("trend") == "BULLISH":

            score += 10

            reasons.append(
                "BULLISH MARKET STRUCTURE"
            )


        elif structure.get("trend") == "BEARISH":

            score += 10

            reasons.append(
                "BEARISH MARKET STRUCTURE"
            )



        # Zones

        if zone.get("nearest_zone"):

            score += 15

            reasons.append(

                str(
                    zone["nearest_zone"]
                )

                +
                " ZONE ACTIVE"

            )



        # Liquidity

        if liquidity.get("liquidity_sweeps"):

            score += 15

            reasons.append(
                "LIQUIDITY EVENT DETECTED"
            )



        # Candlestick

        if candlestick.get("patterns"):

            score += 10

            reasons.append(
                "CANDLE PATTERN CONFIRMATION"
            )



        # Chart patterns

        if chart_pattern.get("patterns"):

            score += 10

            reasons.append(
                "CHART PATTERN CONFIRMATION"
            )



        # Economic filter

        if economic.get("high_impact") == 0:

            score += 5

            reasons.append(
                "NO HIGH IMPACT RISK"
            )



        # Historical intelligence

        score += (

            historical_probability * 0.1

        )


        # Final fusion

        final_score = round(

            (

                score * 0.6

            )

            +

            (

                calibrated_confidence * 0.4

            ),

            2

        )



        if final_score >= 85:

            quality = "INSTITUTIONAL"

        elif final_score >= 70:

            quality = "HIGH"

        elif final_score >= 50:

            quality = "MEDIUM"

        else:

            quality = "LOW"



        direction = "BUY"

        if structure.get("trend") == "BEARISH":

            direction = "SELL"



        return {


            "status":

            "FUSION ANALYSIS COMPLETE",


            "decision_direction":

            direction,


            "confidence":

            final_score,


            "quality":

            quality,


            "reasons":

            reasons,


            "timestamp":

            datetime.datetime.now(

                datetime.timezone.utc

            ).isoformat()


        }



if __name__ == "__main__":


    engine = GSISIntelligenceFusionEngine()


    result = engine.analyze(

        structure={

            "trend":"BULLISH",

            "bos":True

        },


        zone={

            "nearest_zone":"DEMAND"

        },


        liquidity={

            "liquidity_sweeps":

            [

                "SELL_SIDE_SWEEP"

            ]

        },


        candlestick={

            "patterns":

            [

                "BULLISH_ENGULFING"

            ]

        },


        chart_pattern={

            "patterns":

            []

        },


        economic={

            "high_impact":0

        },


        historical_probability=75,


        calibrated_confidence=84

    )


    print("==============================")
    print("GSIS FUSION RESULT")
    print("==============================")
    print(result)
