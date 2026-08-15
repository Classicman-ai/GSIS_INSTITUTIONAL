class LiquidityEngine:

    def __init__(self):

        print("==============================")
        print("GSIS LIQUIDITY ENGINE v1.0 ONLINE")
        print("==============================")
        print("INSTITUTIONAL LIQUIDITY ANALYSIS ACTIVE")
        print("==============================")

    def analyze(self, candle, structure):

        high = candle["high"]
        low = candle["low"]
        close = candle["close"]

        buy_side = high
        sell_side = low

        equal_highs = False
        equal_lows = False

        liquidity_sweep = False

        if structure["structure"] == "BULLISH":
            institutional_bias = "BUY"

        elif structure["structure"] == "BEARISH":
            institutional_bias = "SELL"

        else:
            institutional_bias = "WAIT"

        if close > high:
            liquidity_sweep = True

        if close < low:
            liquidity_sweep = True

        result = {

            "symbol": candle["symbol"],

            "timeframe": candle["timeframe"],

            "buy_side_liquidity": buy_side,

            "sell_side_liquidity": sell_side,

            "equal_highs": equal_highs,

            "equal_lows": equal_lows,

            "liquidity_sweep": liquidity_sweep,

            "institutional_bias": institutional_bias,

            "market_structure": structure["structure"]

        }

        print("==============================")
        print("GSIS LIQUIDITY ANALYSIS")
        print("==============================")
        print(result)

        return result
