import os
import sys

# -------------------------------------------------
# GSIS PACKAGE PATH INITIALIZATION
# -------------------------------------------------
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from intelligence.realtime_data_engine import RealtimeDataEngine
from intelligence.candle_stream_engine import CandleStreamEngine
from intelligence.statistical_engine import StatisticalEngine
from intelligence.feature_memory_engine import FeatureMemoryEngine
from intelligence.market_regime_engine import MarketRegimeEngine
from intelligence.smc_structure_engine import SMCStructureEngine
from intelligence.decision_engine import DecisionEngine


class LiveIntelligencePipeline:

    def __init__(self):

        print("==============================")
        print("GSIS LIVE INTELLIGENCE PIPELINE v15.4 ONLINE")
        print("==============================")

        self.data_engine = RealtimeDataEngine()
        self.candle_engine = CandleStreamEngine()
        self.stat_engine = StatisticalEngine()
        self.feature_memory = FeatureMemoryEngine()
        self.regime_engine = MarketRegimeEngine()
        self.smc_engine = SMCStructureEngine()
        self.decision_engine = DecisionEngine()

    def process(self, symbol, price):

        # LIVE TICK
        tick = self.data_engine.receive_tick(
            symbol,
            price
        )

        print("==============================")
        print("LIVE TICK")
        print("==============================")
        print(tick)

        # BUILD CANDLE
        candle = self.candle_engine.build_candle(
            tick
        )

        print("==============================")
        print("LIVE CANDLE")
        print("==============================")
        print(candle)

        # STATISTICS
        features = self.stat_engine.calculate(
            candle
        )

        print("==============================")
        print("LIVE FEATURES")
        print("==============================")
        print(features)

        # FEATURE MEMORY
        self.feature_memory.process(
            features
        )

        # MARKET REGIME
        regime = self.regime_engine.analyze(
            features
        )

        print("==============================")
        print("LIVE REGIME")
        print("==============================")
        print(regime)

        # SMART MONEY STRUCTURE
        smc = self.smc_engine.analyze(
            features,
            regime
        )

        print("==============================")
        print("LIVE SMC")
        print("==============================")
        print(smc)

        # DECISION
        decision = self.decision_engine.analyze(
            regime
        )

        print("==============================")
        print("LIVE DECISION")
        print("==============================")
        print(decision)

        return {
            "tick": tick,
            "candle": candle,
            "features": features,
            "regime": regime,
            "smc": smc,
            "decision": decision
        }


if __name__ == "__main__":

    pipeline = LiveIntelligencePipeline()

    result = pipeline.process(
        "XAUUSD",
        2386.5
    )

    print("==============================")
    print("GSIS LIVE PIPELINE COMPLETE")
    print("==============================")
    print(result)
