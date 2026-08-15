class OrderBlockEngine:


    def __init__(self):

        print("==============================")
        print("GSIS ORDER BLOCK ENGINE v1.0 ONLINE")
        print("==============================")
        print("INSTITUTIONAL ORDER ZONE DETECTION ACTIVE")
        print("==============================")


    def analyze(self, candle, sweep):


        order_block_found = False

        block_type = None

        zone_high = None

        zone_low = None

        strength = 0

        status = "NONE"



        if sweep["sweep_detected"]:


            if sweep["institutional_signal"] == "SELL":

                order_block_found = True

                block_type = "BEARISH"

                zone_high = candle["high"]

                zone_low = candle["open"]

                strength = sweep["strength"] + 5

                status = "UNMITIGATED"



            elif sweep["institutional_signal"] == "BUY":

                order_block_found = True

                block_type = "BULLISH"

                zone_high = candle["open"]

                zone_low = candle["low"]

                strength = sweep["strength"] + 5

                status = "UNMITIGATED"



        result = {

            "symbol": candle["symbol"],

            "timeframe": candle["timeframe"],

            "order_block_found": order_block_found,

            "type": block_type,

            "zone_high": zone_high,

            "zone_low": zone_low,

            "strength": strength,

            "status": status

        }


        print("==============================")
        print("GSIS ORDER BLOCK ANALYSIS")
        print("==============================")
        print(result)


        return result
