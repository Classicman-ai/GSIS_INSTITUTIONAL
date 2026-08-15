class FairValueGapEngine:


    def __init__(self):

        print("==============================")
        print("GSIS FAIR VALUE GAP ENGINE v1.0 ONLINE")
        print("==============================")
        print("INSTITUTIONAL IMBALANCE DETECTION ACTIVE")
        print("==============================")


    def analyze(self, candle, order_block):


        fvg_found = False

        fvg_type = None

        gap_high = None

        gap_low = None

        gap_size = 0

        status = "NONE"



        high = candle["high"]

        low = candle["low"]

        open_price = candle["open"]

        close = candle["close"]



        # ==============================
        # BEARISH IMBALANCE
        # ==============================

        if order_block["type"] == "BEARISH":

            if close < open_price:

                fvg_found = True

                fvg_type = "BEARISH"

                gap_high = high

                gap_low = close

                gap_size = round(
                    gap_high - gap_low,
                    2
                )

                status = "ACTIVE"



        # ==============================
        # BULLISH IMBALANCE
        # ==============================

        elif order_block["type"] == "BULLISH":

            if close > open_price:

                fvg_found = True

                fvg_type = "BULLISH"

                gap_low = low

                gap_high = close

                gap_size = round(
                    gap_high - gap_low,
                    2
                )

                status = "ACTIVE"



        result = {


            "symbol": candle["symbol"],

            "timeframe": candle["timeframe"],

            "fvg_found": fvg_found,

            "type": fvg_type,

            "gap_high": gap_high,

            "gap_low": gap_low,

            "gap_size": gap_size,

            "status": status


        }


        print("==============================")
        print("GSIS FAIR VALUE GAP ANALYSIS")
        print("==============================")
        print(result)


        return result
