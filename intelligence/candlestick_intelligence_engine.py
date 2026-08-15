import datetime


class CandlestickIntelligenceEngine:

    def __init__(self):

        print("==============================")
        print("GSIS CANDLESTICK INTELLIGENCE ENGINE v2.0 ONLINE")
        print("ADVANCED CANDLE PATTERN RECOGNITION ACTIVE")
        print("==============================")


    def candle_stats(self, c):

        body = abs(c["close"] - c["open"])

        total = c["high"] - c["low"]

        if total == 0:
            total = 0.0001

        upper = c["high"] - max(
            c["open"],
            c["close"]
        )

        lower = min(
            c["open"],
            c["close"]
        ) - c["low"]


        return {

            "body": body,
            "range": total,
            "upper": upper,
            "lower": lower,

            "bullish":
            c["close"] > c["open"],

            "bearish":
            c["close"] < c["open"]

        }


    def single_patterns(self, c):

        s = self.candle_stats(c)

        patterns = []


        # DOJI

        if s["body"] <= s["range"] * 0.1:

            patterns.append(
                {
                    "pattern":"DOJI",
                    "direction":"NEUTRAL",
                    "strength":60
                }
            )


        # DRAGONFLY DOJI

        if (
            s["lower"] > s["range"] * 0.6
            and
            s["upper"] < s["range"] * 0.1
        ):

            patterns.append(
                {
                    "pattern":"DRAGONFLY_DOJI",
                    "direction":"BULLISH",
                    "strength":75
                }
            )


        # GRAVESTONE DOJI

        if (
            s["upper"] > s["range"] * 0.6
            and
            s["lower"] < s["range"] * 0.1
        ):

            patterns.append(
                {
                    "pattern":"GRAVESTONE_DOJI",
                    "direction":"BEARISH",
                    "strength":75
                }
            )


        # PIN BAR BULLISH

        if (
            s["lower"] > s["body"] * 3
            and
            s["upper"] < s["body"]
        ):

            patterns.append(
                {
                    "pattern":"BULLISH_PIN_BAR",
                    "direction":"BULLISH",
                    "strength":80
                }
            )


        # PIN BAR BEARISH

        if (
            s["upper"] > s["body"] * 3
            and
            s["lower"] < s["body"]
        ):

            patterns.append(
                {
                    "pattern":"BEARISH_PIN_BAR",
                    "direction":"BEARISH",
                    "strength":80
                }
            )


        # MARUBOZU

        if (
            s["upper"] < s["body"] * 0.2
            and
            s["lower"] < s["body"] * 0.2
        ):

            patterns.append(
                {
                    "pattern":"MARUBOZU",
                    "direction":
                    "BULLISH"
                    if s["bullish"]
                    else "BEARISH",

                    "strength":85
                }
            )


        return patterns



    def two_patterns(self, previous, current):

        p = self.candle_stats(previous)
        c = self.candle_stats(current)

        patterns = []


        # ENGULFING

        if (
            p["bearish"]
            and
            c["bullish"]
            and
            current["close"] >
            previous["open"]
        ):

            patterns.append(
                {
                    "pattern":"BULLISH_ENGULFING",
                    "direction":"BULLISH",
                    "strength":90
                }
            )


        if (
            p["bullish"]
            and
            c["bearish"]
            and
            current["close"] <
            previous["open"]
        ):

            patterns.append(
                {
                    "pattern":"BEARISH_ENGULFING",
                    "direction":"BEARISH",
                    "strength":90
                }
            )


        # INSIDE BAR

        if (
            current["high"] <
            previous["high"]
            and
            current["low"] >
            previous["low"]
        ):

            patterns.append(
                {
                    "pattern":"INSIDE_BAR",
                    "direction":"NEUTRAL",
                    "strength":70
                }
            )


        # OUTSIDE BAR

        if (
            current["high"] >
            previous["high"]
            and
            current["low"] <
            previous["low"]
        ):

            patterns.append(
                {
                    "pattern":"OUTSIDE_BAR",
                    "direction":"EXPANSION",
                    "strength":75
                }
            )


        return patterns



    def three_patterns(self, candles):

        patterns=[]

        a,b,c = candles[-3], candles[-2], candles[-1]


        # MORNING STAR

        if (
            a["close"] < a["open"]
            and
            b["high"] < a["close"]
            and
            c["close"] > a["open"]
        ):

            patterns.append(
                {
                    "pattern":"MORNING_STAR",
                    "direction":"BULLISH",
                    "strength":85
                }
            )


        # EVENING STAR

        if (
            a["close"] > a["open"]
            and
            b["low"] > a["close"]
            and
            c["close"] < a["open"]
        ):

            patterns.append(
                {
                    "pattern":"EVENING_STAR",
                    "direction":"BEARISH",
                    "strength":85
                }
            )


        return patterns



    def analyze(self,candles):

        if len(candles)<3:

            return {
                "status":"INSUFFICIENT DATA"
            }


        patterns=[]


        patterns.extend(
            self.single_patterns(
                candles[-1]
            )
        )


        patterns.extend(
            self.two_patterns(
                candles[-2],
                candles[-1]
            )
        )


        patterns.extend(
            self.three_patterns(
                candles
            )
        )


        result={

            "status":
            "CANDLESTICK ANALYSIS COMPLETE",

            "patterns_detected":
            len(patterns),

            "patterns":
            patterns,

            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }


        print("==============================")
        print("GSIS CANDLESTICK RESULT")
        print("==============================")
        print(result)

        return result



if __name__=="__main__":


    sample=[

        {
        "open":2387,
        "high":2388,
        "low":2386,
        "close":2386.5
        },

        {
        "open":2386.5,
        "high":2387,
        "low":2386,
        "close":2386.8
        },

        {
        "open":2386.8,
        "high":2388.2,
        "low":2386.7,
        "close":2388
        }

    ]


    engine=CandlestickIntelligenceEngine()

    engine.analyze(sample)
