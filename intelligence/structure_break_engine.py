class StructureBreakEngine:


    def __init__(self):

        print("==============================")
        print("GSIS STRUCTURE BREAK ENGINE v1.0 ONLINE")
        print("==============================")
        print("BOS AND CHoCH DETECTION ACTIVE")
        print("==============================")


    def analyze(self, candle, liquidity_sweep, order_block, fvg):


        bos = False

        choch = False

        structure = "NEUTRAL"

        confirmation = "NONE"

        strength = 0



        high = candle["high"]

        low = candle["low"]

        close = candle["close"]



        # ==============================
        # BEARISH STRUCTURE SHIFT
        # ==============================

        if (
            liquidity_sweep["institutional_signal"] == "SELL"
            and order_block["type"] == "BEARISH"
            and fvg["type"] == "BEARISH"
        ):

            if close < fvg["gap_low"]:

                choch = True

                structure = "BEARISH"

                confirmation = "BEARISH_CHoCH"

                strength = 90


            elif close < order_block["zone_low"]:

                bos = True

                structure = "BEARISH"

                confirmation = "BEARISH_BOS"

                strength = 85



        # ==============================
        # BULLISH STRUCTURE SHIFT
        # ==============================

        if (
            liquidity_sweep["institutional_signal"] == "BUY"
            and order_block["type"] == "BULLISH"
            and fvg["type"] == "BULLISH"
        ):

            if close > fvg["gap_high"]:

                choch = True

                structure = "BULLISH"

                confirmation = "BULLISH_CHoCH"

                strength = 90


            elif close > order_block["zone_high"]:

                bos = True

                structure = "BULLISH"

                confirmation = "BULLISH_BOS"

                strength = 85



        result = {

            "symbol": candle["symbol"],

            "timeframe": candle["timeframe"],

            "structure": structure,

            "bos": bos,

            "choch": choch,

            "confirmation": confirmation,

            "strength": strength

        }


        print("==============================")
        print("GSIS STRUCTURE BREAK ANALYSIS")
        print("==============================")
        print(result)


        return result
