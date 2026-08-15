import sys
import os
from datetime import datetime, timezone

# ==========================================
# GSIS PROJECT PATH
# ==========================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)

from intelligence.live_trading_core import LiveTradingCore
from intelligence.intelligence_bridge import IntelligenceBridge
from intelligence.auto_learning_loop import AutoLearningLoop


print("==============================")
print("GSIS AUTO MARKET LOOP v3.1 ONLINE")
print("==============================")
print("LIVE INTELLIGENCE + AUTO LEARNING ACTIVE")
print("==============================")


class AutoMarketLoop:

    def __init__(self):

        self.live_core = LiveTradingCore()
        self.intelligence = IntelligenceBridge()
        self.learning = AutoLearningLoop()

    def run_once(self):

        signal = {

            "symbol": "XAUUSD",

            "direction": "SELL",

            "entry": 2387.5,

            "stop_loss": 2387.8,

            "tp1": 2387.2,

            "confidence": 100,

            "reasons": [

                "LIQUIDITY SWEEP CONFIRMED",

                "BEARISH ORDER BLOCK",

                "BEARISH FVG",

                "BEARISH CHoCH"

            ]

        }

        print("==============================")
        print("GSIS MARKET SCAN")
        print("==============================")
        print(signal)

        print("==============================")
        print("GSIS INTELLIGENCE FILTER")
        print("==============================")

        intelligence_result = self.intelligence.evaluate(

            signal["symbol"],

            signal["direction"],

            signal["confidence"],

            signal["reasons"]

        )

        print("==============================")
        print("GSIS INTELLIGENCE RESULT")
        print("==============================")
        print(intelligence_result)

        print("==============================")
        print("GSIS AUTO LEARNING")
        print("==============================")

        learning_result = self.learning.process_signal(

            symbol=signal["symbol"],

            direction=signal["direction"],

            entry=signal["entry"],

            stop_loss=signal["stop_loss"],

            tp1=signal["tp1"],

            confidence=signal["confidence"],

            reasons=signal["reasons"]

        )

        print("==============================")
        print("GSIS LEARNING RESULT")
        print("==============================")
        print(learning_result)

        if intelligence_result.get("decision") != "APPROVED":

            print("==============================")
            print("TRADE BLOCKED")
            print("==============================")

            return {

                "status": "FILTERED",

                "reason": intelligence_result,

                "learning": learning_result

            }

        print("==============================")
        print("GSIS EXECUTION PIPELINE")
        print("==============================")

        execution = self.live_core.analyze_market(

            signal["symbol"],

            signal["direction"],

            signal["confidence"],

            signal["reasons"]

        )

        return {

            "status": "EXECUTION READY",

            "intelligence": intelligence_result,

            "learning": learning_result,

            "execution": execution,

            "timestamp": datetime.now(
                timezone.utc
            ).isoformat()

        }


if __name__ == "__main__":

    engine = AutoMarketLoop()

    result = engine.run_once()

    print("==============================")
    print("GSIS AUTO LOOP FINAL RESULT")
    print("==============================")
    print(result)
