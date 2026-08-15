class LiquiditySweepEngine:


    def __init__(self):

        print("==============================")
        print("GSIS LIQUIDITY SWEEP ENGINE v1.0 ONLINE")
        print("==============================")
        print("STOP HUNT AND LIQUIDITY GRAB DETECTION ACTIVE")
        print("==============================")


    def analyze(self, candle, liquidity):


        high = candle["high"]
        low = candle["low"]
        close = candle["close"]


        buy_liquidity = liquidity.get(
            "buy_side_liquidity"
        )

        sell_liquidity = liquidity.get(
            "sell_side_liquidity"
        )


        sweep_detected = False
        sweep_type = None
        strength = 0
        signal = "WAIT"
        grabbed_price = None



        # ==============================
        # BUY SIDE LIQUIDITY SWEEP
        # ==============================

        if high >= buy_liquidity:

            sweep_detected = True

            sweep_type = "BUY_SIDE"

            grabbed_price = buy_liquidity

            strength = 80


            if close < buy_liquidity:

                signal = "SELL"



        # ==============================
        # SELL SIDE LIQUIDITY SWEEP
        # ==============================

        if low <= sell_liquidity:

            sweep_detected = True

            sweep_type = "SELL_SIDE"

            grabbed_price = sell_liquidity

            strength = 80


            if close > sell_liquidity:

                signal = "BUY"



        result = {

            "symbol": candle["symbol"],

            "timeframe": candle["timeframe"],

            "sweep_detected": sweep_detected,

            "sweep_type": sweep_type,

            "grabbed_price": grabbed_price,

            "current_price": close,

            "strength": strength,

            "institutional_signal": signal

        }


        print("==============================")
        print("GSIS LIQUIDITY SWEEP ANALYSIS")
        print("==============================")
        print(result)


        return result
