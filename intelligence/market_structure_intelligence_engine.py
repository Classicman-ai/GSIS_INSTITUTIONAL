import datetime


class MarketStructureIntelligenceEngine:

    def __init__(self):

        print("==============================")
        print("GSIS MARKET STRUCTURE INTELLIGENCE ENGINE v2.0 ONLINE")
        print("INSTITUTIONAL MARKET STRUCTURE INTELLIGENCE ACTIVE")
        print("==============================")

    def _find_swings(self, candles):

        swing_highs = []
        swing_lows = []

        for i in range(1, len(candles)-1):

            if (
                candles[i]["high"] > candles[i-1]["high"]
                and
                candles[i]["high"] > candles[i+1]["high"]
            ):
                swing_highs.append(
                    {
                        "index": i,
                        "price": candles[i]["high"]
                    }
                )

            if (
                candles[i]["low"] < candles[i-1]["low"]
                and
                candles[i]["low"] < candles[i+1]["low"]
            ):
                swing_lows.append(
                    {
                        "index": i,
                        "price": candles[i]["low"]
                    }
                )

        return swing_highs, swing_lows

    def analyze(self, candles):

        if len(candles) < 7:

            return {
                "status": "INSUFFICIENT DATA"
            }

        swing_highs, swing_lows = self._find_swings(candles)

        last = candles[-1]
        previous = candles[-2]

        trend = "RANGE"

        if last["close"] > previous["close"]:
            trend = "BULLISH"

        elif last["close"] < previous["close"]:
            trend = "BEARISH"

        hh = False
        hl = False
        lh = False
        ll = False

        if len(swing_highs) >= 2:

            if swing_highs[-1]["price"] > swing_highs[-2]["price"]:
                hh = True
            else:
                lh = True

        if len(swing_lows) >= 2:

            if swing_lows[-1]["price"] > swing_lows[-2]["price"]:
                hl = True
            else:
                ll = True

        bos = hh or ll

        choch = (
            (trend == "BULLISH" and ll)
            or
            (trend == "BEARISH" and hh)
        )

        mss = bos and choch

        market_phase = "RANGE"

        if hh and hl:
            market_phase = "MARKUP"

        elif lh and ll:
            market_phase = "MARKDOWN"

        elif hh and ll:
            market_phase = "DISTRIBUTION"

        elif hl and lh:
            market_phase = "ACCUMULATION"

        result = {

            "status": "MARKET STRUCTURE COMPLETE",

            "trend": trend,

            "market_phase": market_phase,

            "higher_high": hh,

            "higher_low": hl,

            "lower_high": lh,

            "lower_low": ll,

            "bos": bos,

            "choch": choch,

            "mss": mss,

            "swing_highs": swing_highs,

            "swing_lows": swing_lows,

            "structure_strength": len(swing_highs) + len(swing_lows),

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }

        print("==============================")
        print("GSIS MARKET STRUCTURE RESULT")
        print("==============================")
        print(result)

        return result


if __name__ == "__main__":

    sample = [

        {"high":2385.2,"low":2384.4,"close":2385.0},
        {"high":2386.1,"low":2384.9,"close":2385.9},
        {"high":2387.3,"low":2385.6,"close":2387.0},
        {"high":2386.8,"low":2385.9,"close":2386.2},
        {"high":2388.2,"low":2386.1,"close":2388.0},
        {"high":2387.5,"low":2386.7,"close":2387.1},
        {"high":2389.0,"low":2387.0,"close":2388.8},
        {"high":2388.4,"low":2387.5,"close":2387.8},
        {"high":2390.1,"low":2388.0,"close":2389.9}

    ]

    engine = MarketStructureIntelligenceEngine()

    engine.analyze(sample)
