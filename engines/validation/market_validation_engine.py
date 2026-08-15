from datetime import datetime, timezone


class MarketValidationEngine:


    def __init__(self):

        self.version = "1.1"



    def run(self, context):


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


        orderflow = getattr(
            context,
            "orderflow",
            {}
        )


        regime = getattr(
            context,
            "regime",
            {}
        )


        if regime is None:
            regime = {}



        if market is None:
            market = {}


        if volume is None:
            volume = {}


        if orderflow is None:
            orderflow = {}



        checks = {

            "market_data":
            bool(market),


            "volume_data":
            bool(volume),


            "orderflow_data":
            bool(orderflow),


            "regime_data":
            bool(regime)

        }



        valid = all(
            checks.values()
        )


        reasons = []


        if not checks["market_data"]:
            reasons.append(
                "MARKET DATA MISSING"
            )


        if not checks["volume_data"]:
            reasons.append(
                "VOLUME DATA MISSING"
            )


        if not checks["orderflow_data"]:
            reasons.append(
                "ORDERFLOW DATA MISSING"
            )


        if not checks["regime_data"]:
            reasons.append(
                "REGIME DATA MISSING"
            )



        result = {


            "engine":
            "GSIS MARKET VALIDATION ENGINE",


            "version":
            self.version,


            "symbol":
            context.symbol,


            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),


            "validation":
            "PASSED"
            if valid
            else "FAILED",


            "market_state":
            "HEALTHY"
            if valid
            else "BLOCKED",


            "checks":
            checks,


            "reasons":
            reasons,


            "status":
            "VALIDATION_COMPLETE"

        }



        context.validation = result


        return result




if __name__ == "__main__":

    print(
        "GSIS MARKET VALIDATION ENGINE v1.1 READY"
    )
