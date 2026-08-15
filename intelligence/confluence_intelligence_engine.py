import datetime


class ConfluenceIntelligenceEngine:

    def __init__(self):

        print("==============================")
        print("GSIS CONFLUENCE INTELLIGENCE ENGINE v1.0 ONLINE")
        print("MULTI FACTOR MARKET ANALYSIS ACTIVE")
        print("==============================")


    def analyze(
        self,
        structure,
        zones,
        liquidity,
        price_action,
        candles,
        patterns
    ):


        score = 0

        reasons = []

        direction = "NEUTRAL"



        # MARKET STRUCTURE

        if structure:

            if structure.get("bos"):

                score += 20

                reasons.append(
                    "BREAK OF STRUCTURE CONFIRMED"
                )


            if structure.get("trend") == "BULLISH":

                score += 10

                direction = "BUY"

                reasons.append(
                    "BULLISH STRUCTURE"
                )


            elif structure.get("trend") == "BEARISH":

                score += 10

                direction = "SELL"

                reasons.append(
                    "BEARISH STRUCTURE"
                )



        # ZONE CONTEXT

        if zones:

            nearest = zones.get(
                "nearest_zone"
            )


            if nearest:

                score += 20

                reasons.append(

                    nearest["type"]
                    +
                    " ZONE ACTIVE"

                )


                if nearest["type"] == "DEMAND":

                    direction = "BUY"


                elif nearest["type"] == "SUPPLY":

                    direction = "SELL"




        # LIQUIDITY

        if liquidity:

            sweeps = liquidity.get(
                "liquidity_sweeps",
                []
            )


            if len(sweeps) > 0:

                score += 20

                reasons.append(
                    "LIQUIDITY SWEEP DETECTED"
                )



        # PRICE ACTION

        if price_action:

            rejection = price_action.get(
                "latest_rejection"
            )


            if rejection != "NONE":

                score += 10

                reasons.append(
                    rejection
                )



        # CANDLESTICKS

        if candles:

            detected = candles.get(
                "patterns",
                []
            )


            if len(detected) > 0:

                score += 10

                reasons.append(
                    "CANDLE PATTERN CONFIRMATION"
                )



        # CHART PATTERNS

        if patterns:

            detected = patterns.get(
                "patterns",
                []
            )


            if len(detected) > 0:

                score += 10

                reasons.append(
                    "CHART PATTERN CONFIRMATION"
                )



        if score > 100:

            score = 100



        confidence = score



        if confidence >= 80:

            quality = "HIGH"


        elif confidence >= 60:

            quality = "MEDIUM"


        else:

            quality = "LOW"



        result = {

            "status":
            "CONFLUENCE ANALYSIS COMPLETE",

            "decision_direction":
            direction,

            "confidence":
            confidence,

            "quality":
            quality,

            "reasons":
            reasons,

            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }


        print("==============================")
        print("GSIS CONFLUENCE RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = ConfluenceIntelligenceEngine()


    test_structure = {

        "trend":"BULLISH",

        "bos":True

    }


    test_zone = {

        "nearest_zone":{

            "type":"DEMAND"

        }

    }


    test_liquidity = {

        "liquidity_sweeps":[

            {

                "type":
                "SELL_SIDE_SWEEP"

            }

        ]

    }


    test_price = {

        "latest_rejection":
        "BULLISH_REJECTION"

    }


    test_candle = {

        "patterns":[

            {

                "pattern":
                "BULLISH_ENGULFING"

            }

        ]

    }


    test_pattern = {

        "patterns":[]

    }



    engine.analyze(

        test_structure,

        test_zone,

        test_liquidity,

        test_price,

        test_candle,

        test_pattern

    )
