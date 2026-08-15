from datetime import datetime, timezone


class AdaptiveMarketIntelligence:


    def run(self, context):


        symbol = context.symbol


        # GSIS CONTEXT BUS INPUTS

        market = getattr(
            context,
            "market",
            {}
        )


        volume = getattr(
            context,
            "volume",
            {}
        )


        # Read synchronized flow
        # Priority: Context Mapper → Orderflow fallback

        adaptive_context = getattr(
            context,
            "adaptive",
            {}
        )


        if isinstance(adaptive_context, dict):

            flow = adaptive_context.get(
                "flow",
                {}
            )

        else:

            flow = {}



        if not flow:

            flow = getattr(
                context,
                "orderflow",
                {}
            )



        confidence = 0.50



        if market:

            confidence += 0.10



        if volume:

            confidence += 0.10



        if flow:

            confidence += 0.12



        confidence = min(
            confidence,
            1.0
        )



        result = {


            "engine":
                "GSIS ADAPTIVE MARKET INTELLIGENCE",


            "version":
                "4.1",


            "symbol":
                symbol,


            "timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat(),


            "market_condition":
                "BULLISH_TREND",


            "strategy_mode":
                "LONG_SWING",


            "risk_state":
                "NORMAL",


            "original_confidence":
                round(
                    confidence,
                    3
                ),


            "adjusted_confidence":
                round(
                    confidence,
                    3
                ),



            "inputs":

            {

                "market":
                    "VALID"
                    if market
                    else "MISSING",


                "volume":
                    "VALID"
                    if volume
                    else "MISSING",


                "flow":
                    "VALID"
                    if flow
                    else "MISSING"

            },


            "status":
                "ADAPTIVE_COMPLETE"

        }



        # Save result back into context

        context.adaptive = result


        return result




if __name__ == "__main__":


    print(
        "GSIS ADAPTIVE MARKET INTELLIGENCE v4.1 READY"
    )
