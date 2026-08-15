import datetime


class LiquidityIntelligenceEngine:

    def __init__(self):

        print("==============================")
        print("GSIS LIQUIDITY INTELLIGENCE ENGINE v1.0 ONLINE")
        print("INSTITUTIONAL LIQUIDITY DETECTION ACTIVE")
        print("==============================")


    def detect_equal_levels(self, candles):

        equal_highs = []
        equal_lows = []

        tolerance = 0.3

        for i in range(len(candles) - 1):

            current = candles[i]
            next_candle = candles[i + 1]


            if abs(
                current["high"] -
                next_candle["high"]
            ) <= tolerance:

                equal_highs.append({

                    "level": current["high"],

                    "index": i,

                    "type": "BUY_SIDE_LIQUIDITY"

                })


            if abs(
                current["low"] -
                next_candle["low"]
            ) <= tolerance:

                equal_lows.append({

                    "level": current["low"],

                    "index": i,

                    "type": "SELL_SIDE_LIQUIDITY"

                })


        return equal_highs, equal_lows


    def detect_sweeps(self, candles, equal_highs, equal_lows):

        sweeps = []


        for high in equal_highs:

            level = high["level"]

            for candle in candles[high["index"] + 1:]:

                if candle["high"] > level and candle["close"] < level:

                    sweeps.append({

                        "type": "BUY_SIDE_LIQUIDITY_SWEEP",

                        "level": level,

                        "confirmation": "BEARISH_REJECTION"

                    })


        for low in equal_lows:

            level = low["level"]

            for candle in candles[low["index"] + 1:]:

                if candle["low"] < level and candle["close"] > level:

                    sweeps.append({

                        "type": "SELL_SIDE_LIQUIDITY_SWEEP",

                        "level": level,

                        "confirmation": "BULLISH_REJECTION"

                    })


        return sweeps



    def analyze(self, candles):


        if len(candles) < 5:

            return {

                "status": "INSUFFICIENT DATA"

            }


        equal_highs, equal_lows = self.detect_equal_levels(
            candles
        )


        sweeps = self.detect_sweeps(
            candles,
            equal_highs,
            equal_lows
        )


        liquidity_state = "BALANCED"


        if len(equal_highs) > len(equal_lows):

            liquidity_state = "BUY_SIDE HEAVY"


        elif len(equal_lows) > len(equal_highs):

            liquidity_state = "SELL_SIDE HEAVY"



        result = {

            "status": "LIQUIDITY ANALYSIS COMPLETE",

            "equal_highs": equal_highs,

            "equal_lows": equal_lows,

            "liquidity_sweeps": sweeps,

            "liquidity_state": liquidity_state,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS LIQUIDITY RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    sample = [

        {"high":2385.8,"low":2384.5,"close":2385.2},

        {"high":2386.4,"low":2385.1,"close":2386.0},

        {"high":2386.5,"low":2385.7,"close":2386.1},

        {"high":2387.2,"low":2386.0,"close":2386.8},

        {"high":2387.1,"low":2386.3,"close":2386.5},

        {"high":2388.0,"low":2386.9,"close":2387.7}

    ]


    engine = LiquidityIntelligenceEngine()

    engine.analyze(sample)
