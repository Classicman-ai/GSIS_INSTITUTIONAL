from datetime import datetime, timezone


class AdaptiveMarketEngine:

    def __init__(self):
        self.name = "GSIS ADAPTIVE MARKET INTELLIGENCE"
        self.version = "4.1"


    def run(self, context):

        symbol = getattr(context, "symbol", "BTCUSDT")


        market = getattr(
            context,
            "market",
            None
        )

        volume = getattr(
            context,
            "volume",
            None
        )

        orderflow = getattr(
            context,
            "orderflow",
            None
        )

        regime = getattr(
            context,
            "regime",
            None
        )


        inputs = {

            "market":
                "VALID" if market else "MISSING",

            "volume":
                "VALID" if volume else "MISSING",

            "flow":
                "VALID" if orderflow else "MISSING",

            "regime":
                "VALID" if regime else "MISSING"
        }


        market_condition = "NEUTRAL"
        strategy_mode = "NO_TRADE"
        risk_state = "NORMAL"


        confidence = 0.5


        if regime:

            regime_name = regime.get(
                "market_regime",
                "UNKNOWN"
            )

            if regime_name == "TRENDING_UP":

                market_condition = "BULLISH_TREND"
                strategy_mode = "LONG_SWING"
                confidence = 0.7


            elif regime_name == "TRENDING_DOWN":

                market_condition = "BEARISH_TREND"
                strategy_mode = "SHORT_SWING"
                confidence = 0.7



        if orderflow:

            if orderflow.get("flow_bias") == "BUY_PRESSURE":

                confidence += 0.05


            elif orderflow.get("flow_bias") == "SELL_PRESSURE":

                confidence -= 0.05



        if confidence > 1:
            confidence = 1


        return {

            "engine":
                self.name,

            "version":
                self.version,

            "symbol":
                symbol,

            "timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat(),


            "market_condition":
                market_condition,


            "strategy_mode":
                strategy_mode,


            "risk_state":
                risk_state,


            "original_confidence":
                0.7,


            "adjusted_confidence":
                round(
                    confidence,
                    2
                ),


            "inputs":
                inputs,


            "status":
                "ADAPTIVE_COMPLETE"
        }



if __name__ == "__main__":

    engine = AdaptiveMarketEngine()

    print(
        engine.run(
            type(
                "Context",
                (),
                {
                    "symbol":"BTCUSDT"
                }
            )()
        )
    )
