import datetime


class PriceActionIntelligenceEngine:

    def __init__(self):

        print("==============================")
        print("GSIS PRICE ACTION INTELLIGENCE ENGINE v1.0 ONLINE")
        print("INSTITUTIONAL PRICE ACTION ANALYSIS ACTIVE")
        print("==============================")


    def candle_analysis(self, candle):

        body = abs(
            candle["close"] - candle["open"]
        )

        upper_wick = (
            candle["high"] -
            max(candle["open"], candle["close"])
        )

        lower_wick = (
            min(candle["open"], candle["close"]) -
            candle["low"]
        )


        if body == 0:

            body = 0.0001


        return {

            "body_size": round(body, 2),

            "upper_wick": round(upper_wick, 2),

            "lower_wick": round(lower_wick, 2),

            "bullish":

                candle["close"] >
                candle["open"],

            "bearish":

                candle["close"] <
                candle["open"]

        }



    def analyze_trend(self, candles):

        closes = [
            c["close"]
            for c in candles
        ]


        rising = 0
        falling = 0


        for i in range(1, len(closes)):

            if closes[i] > closes[i-1]:

                rising += 1

            elif closes[i] < closes[i-1]:

                falling += 1


        if rising > falling:

            return "UPTREND"

        elif falling > rising:

            return "DOWNTREND"

        return "RANGE"



    def detect_market_condition(self, candles):

        ranges = []

        for candle in candles:

            ranges.append(

                candle["high"] -
                candle["low"]

            )


        average_range = sum(ranges) / len(ranges)

        latest_range = ranges[-1]


        if latest_range > average_range * 1.5:

            return "EXPANSION"


        if latest_range < average_range * 0.7:

            return "COMPRESSION"


        return "NORMAL"



    def detect_rejection(self, candle):

        analysis = self.candle_analysis(candle)


        if (
            analysis["lower_wick"] >
            analysis["body_size"] * 2
        ):

            return "BULLISH_REJECTION"


        if (
            analysis["upper_wick"] >
            analysis["body_size"] * 2
        ):

            return "BEARISH_REJECTION"


        return "NONE"



    def analyze(self, candles):

        if len(candles) < 5:

            return {

                "status":
                "INSUFFICIENT DATA"

            }


        trend = self.analyze_trend(
            candles
        )


        condition = self.detect_market_condition(
            candles
        )


        rejection = self.detect_rejection(
            candles[-1]
        )


        result = {

            "status":
            "PRICE ACTION ANALYSIS COMPLETE",

            "trend":
            trend,

            "market_condition":
            condition,

            "latest_rejection":
            rejection,

            "latest_candle":
            self.candle_analysis(
                candles[-1]
            ),

            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }


        print("==============================")
        print("GSIS PRICE ACTION RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    sample = [

        {
            "open":2385.0,
            "high":2386.0,
            "low":2384.8,
            "close":2385.7
        },

        {
            "open":2385.7,
            "high":2386.8,
            "low":2385.4,
            "close":2386.5
        },

        {
            "open":2386.5,
            "high":2387.4,
            "low":2386.1,
            "close":2387.0
        },

        {
            "open":2387.0,
            "high":2387.8,
            "low":2386.7,
            "close":2387.2
        },

        {
            "open":2387.2,
            "high":2388.1,
            "low":2386.5,
            "close":2386.8
        }

    ]


    engine = PriceActionIntelligenceEngine()

    engine.analyze(sample)
