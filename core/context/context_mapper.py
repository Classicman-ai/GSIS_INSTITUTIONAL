from datetime import datetime, timezone


class GSISContextMapper:

    def __init__(self):

        self.version = "1.1"



    def ensure_container(self, context, name):

        value = getattr(context, name, None)

        if not isinstance(value, dict):

            setattr(
                context,
                name,
                {}
            )



    def sync(self, context):


        containers = [

            "market",
            "volume",
            "orderflow",
            "liquidity",
            "adaptive",
            "fusion",
            "signal",
            "risk",
            "quality",
            "execution",
            "journal",
            "performance",
            "memory"

        ]


        for item in containers:

            self.ensure_container(
                context,
                item
            )



        # ORDER FLOW → ADAPTIVE

        if context.orderflow:

            context.adaptive["flow"] = {

                "flow_bias":
                    context.orderflow.get(
                        "flow_bias",
                        "UNKNOWN"
                    ),

                "delta":
                    context.orderflow.get(
                        "delta",
                        0
                    ),

                "buy_volume":
                    context.orderflow.get(
                        "buy_volume",
                        0
                    ),

                "sell_volume":
                    context.orderflow.get(
                        "sell_volume",
                        0
                    ),

                "absorption":
                    context.orderflow.get(
                        "absorption",
                        False
                    )

            }



        # MARKET → ADAPTIVE

        if context.market:

            context.adaptive["market"] = {

                "price":
                    context.market.get(
                        "price",
                        0
                    ),

                "trend":
                    context.market.get(
                        "trend",
                        "UNKNOWN"
                    )

            }



        # VOLUME → ADAPTIVE

        if context.volume:

            context.adaptive["volume"] = {

                "volume_bias":
                    context.volume.get(
                        "volume_bias",
                        "UNKNOWN"
                    ),

                "strength":
                    context.volume.get(
                        "volume_strength",
                        0
                    )

            }



        return {


            "engine":
                "GSIS CONTEXT MAPPER",


            "version":
                self.version,


            "timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat(),


            "inputs":

            {

                "market":
                    "VALID"
                    if context.market
                    else "MISSING",


                "volume":
                    "VALID"
                    if context.volume
                    else "MISSING",


                "flow":
                    "VALID"
                    if context.orderflow
                    else "MISSING"

            },


            "status":
                "CONTEXT_SYNCHRONIZED"

        }



if __name__ == "__main__":

    print(
        "GSIS CONTEXT MAPPER v1.1 READY"
    )
