import os
import sys
from datetime import datetime, timezone


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from intelligence.trade_orchestrator import TradeOrchestrator


class LiveTradingCore:

    def __init__(self):

        print("==============================")
        print("GSIS LIVE TRADING CORE v1.2 ONLINE")
        print("==============================")
        print("ORCHESTRATOR BRIDGE ACTIVE")
        print("==============================")


        self.orchestrator = TradeOrchestrator()



    def analyze_market(
        self,
        symbol,
        direction,
        confidence,
        reasons,
        balance=100000,
        risk_percent=0.5
    ):


        print("==============================")
        print("GSIS LIVE MARKET ANALYSIS")
        print("==============================")


        validation_result = {

            "symbol": symbol,

            "setup": "VALID",

            "direction": direction,

            "confidence": confidence,

            "reasons": reasons,

            "status": "APPROVED",

            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()

        }


        print("==============================")
        print("VALIDATION BRIDGE")
        print("==============================")

        print(validation_result)



        result = self.orchestrator.process(

            validation_result,

            balance,

            risk_percent

        )


        print("==============================")
        print("GSIS LIVE TRADING RESULT")
        print("==============================")

        print(result)


        return result



if __name__ == "__main__":


    core = LiveTradingCore()


    result = core.analyze_market(

        symbol="XAUUSD",

        direction="SELL",

        confidence=100,

        reasons=[

            "LIQUIDITY SWEEP CONFIRMED",

            "BEARISH ORDER BLOCK",

            "BEARISH FAIR VALUE GAP",

            "BEARISH_CHoCH",

            "FAVORABLE MARKET REGIME"

        ]

    )


    print("==============================")
    print("FINAL LIVE CORE RESULT")
    print("==============================")

    print(result)
