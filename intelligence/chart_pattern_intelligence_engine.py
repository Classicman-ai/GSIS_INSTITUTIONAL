import datetime


class ChartPatternIntelligenceEngine:

    def __init__(self):

        print("==============================")
        print("GSIS CHART PATTERN INTELLIGENCE ENGINE v2.0 ONLINE")
        print("ADVANCED MARKET STRUCTURE PATTERN ANALYSIS ACTIVE")
        print("==============================")


    def get_swings(self, candles):

        highs = []
        lows = []

        for i in range(1, len(candles)-1):

            if (
                candles[i]["high"] >
                candles[i-1]["high"]
                and
                candles[i]["high"] >
                candles[i+1]["high"]
            ):

                highs.append(
                    candles[i]["high"]
                )


            if (
                candles[i]["low"] <
                candles[i-1]["low"]
                and
                candles[i]["low"] <
                candles[i+1]["low"]
            ):

                lows.append(
                    candles[i]["low"]
                )


        return highs, lows



    def detect_head_shoulders(self, highs):

        patterns=[]


        if len(highs) >= 3:

            left = highs[-3]
            head = highs[-2]
            right = highs[-1]


            if (
                head > left
                and
                head > right
                and
                abs(left-right) <= head*0.01
            ):

                patterns.append({

                    "pattern":
                    "HEAD_AND_SHOULDERS",

                    "type":
                    "REVERSAL",

                    "direction":
                    "BEARISH",

                    "confidence":
                    85

                })


        return patterns



    def detect_inverse_head_shoulders(self, lows):

        patterns=[]


        if len(lows)>=3:

            left=lows[-3]
            head=lows[-2]
            right=lows[-1]


            if (
                head < left
                and
                head < right
                and
                abs(left-right) <= left*0.01
            ):

                patterns.append({

                    "pattern":
                    "INVERSE_HEAD_AND_SHOULDERS",

                    "type":
                    "REVERSAL",

                    "direction":
                    "BULLISH",

                    "confidence":
                    85

                })


        return patterns



    def detect_triple_top(self, highs):

        patterns=[]


        if len(highs)>=3:

            a,b,c=highs[-3:]

            if (
                abs(a-b)<1
                and
                abs(b-c)<1
            ):

                patterns.append({

                    "pattern":
                    "TRIPLE_TOP",

                    "type":
                    "REVERSAL",

                    "direction":
                    "BEARISH",

                    "confidence":
                    80

                })


        return patterns



    def detect_triple_bottom(self,lows):

        patterns=[]


        if len(lows)>=3:

            a,b,c=lows[-3:]


            if (
                abs(a-b)<1
                and
                abs(b-c)<1
            ):

                patterns.append({

                    "pattern":
                    "TRIPLE_BOTTOM",

                    "type":
                    "REVERSAL",

                    "direction":
                    "BULLISH",

                    "confidence":
                    80

                })


        return patterns



    def detect_wedges(self, highs, lows):

        patterns=[]


        if len(highs)>=3 and len(lows)>=3:

            high_direction = (
                highs[-1]-highs[0]
            )

            low_direction = (
                lows[-1]-lows[0]
            )


            if (
                high_direction < 0
                and
                low_direction < 0
            ):

                patterns.append({

                    "pattern":
                    "FALLING_WEDGE",

                    "type":
                    "REVERSAL",

                    "direction":
                    "BULLISH",

                    "confidence":
                    75

                })


            elif (
                high_direction > 0
                and
                low_direction > 0
            ):

                patterns.append({

                    "pattern":
                    "RISING_WEDGE",

                    "type":
                    "REVERSAL",

                    "direction":
                    "BEARISH",

                    "confidence":
                    75

                })


        return patterns



    def analyze(self,candles):

        if len(candles)<10:

            return {
                "status":
                "INSUFFICIENT DATA"
            }


        highs,lows=self.get_swings(
            candles
        )


        patterns=[]


        patterns.extend(
            self.detect_head_shoulders(
                highs
            )
        )


        patterns.extend(
            self.detect_inverse_head_shoulders(
                lows
            )
        )


        patterns.extend(
            self.detect_triple_top(
                highs
            )
        )


        patterns.extend(
            self.detect_triple_bottom(
                lows
            )
        )


        patterns.extend(
            self.detect_wedges(
                highs,
                lows
            )
        )


        result={

            "status":
            "CHART PATTERN ANALYSIS COMPLETE",

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
        print("GSIS CHART PATTERN RESULT")
        print("==============================")
        print(result)


        return result



if __name__=="__main__":

    candles=[]

    price=2385

    for i in range(30):

        candles.append({

            "open":price,

            "high":price+1,

            "low":price-1,

            "close":price+0.3

        })

        price+=0.2


    engine=ChartPatternIntelligenceEngine()

    engine.analyze(candles)
