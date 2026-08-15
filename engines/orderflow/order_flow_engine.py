from datetime import datetime, timezone


class OrderFlowEngine:


    def run(self, context):

        symbol = context.symbol


        buy_volume = 9000
        sell_volume = 6000

        delta = (
            buy_volume - sell_volume
        ) / (
            buy_volume + sell_volume
        )


        return {

            "engine":
            "GSIS ORDER FLOW ENGINE",

            "version":
            "3.0",

            "symbol":
            symbol,

            "timestamp":
            datetime.now(timezone.utc).isoformat(),

            "buy_volume":
            buy_volume,

            "sell_volume":
            sell_volume,

            "delta":
            round(delta,2),

            "flow_bias":
            "BUY_PRESSURE",

            "absorption":
            False,

            "status":
            "ORDER_FLOW_COMPLETE"
        }
