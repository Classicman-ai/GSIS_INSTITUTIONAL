from intelligence.realtime_data_engine import RealtimeDataEngine
from intelligence.candle_stream_engine import CandleStreamEngine
from intelligence.market_feed_manager import MarketFeedManager

from intelligence.statistical_engine import StatisticalEngine
from intelligence.feature_memory_engine import FeatureMemoryEngine
from intelligence.market_regime_engine import MarketRegimeEngine
from intelligence.smc_structure_engine import SMCStructureEngine
from intelligence.decision_engine import DecisionEngine


print("==============================")
print("GSIS LIVE GOLD PIPELINE v14.1")
print("==============================")
print("REALTIME XAUUSD INTELLIGENCE ACTIVE")
print("==============================")


# ==========================================================
# REALTIME DATA LAYER
# ==========================================================

realtime_engine = RealtimeDataEngine()

candle_engine = CandleStreamEngine()

feed_manager = MarketFeedManager(
    realtime_engine,
    candle_engine
)


# ==========================================================
# GSIS INTELLIGENCE ENGINES
# ==========================================================

stat_engine = StatisticalEngine()

feature_memory_engine = FeatureMemoryEngine()

regime_engine = MarketRegimeEngine()

smc_engine = SMCStructureEngine()

decision_engine = DecisionEngine()



# ==========================================================
# LIVE MARKET INPUT
# ==========================================================

candle = feed_manager.update(
    "XAUUSD",
    2386.50
)


print("==============================")
print("LIVE CANDLE")
print("==============================")

print(candle)



# ==========================================================
# STATISTICAL ANALYSIS
# ==========================================================

features = stat_engine.calculate(
    candle
)


print("==============================")
print("LIVE FEATURES")
print("==============================")

print(features)



# ==========================================================
# FEATURE MEMORY
# ==========================================================

feature_memory_engine.process(
    features
)



# ==========================================================
# MARKET REGIME
# ==========================================================

regime = regime_engine.analyze(
    features
)


print("==============================")
print("LIVE REGIME")
print("==============================")

print(regime)



# ==========================================================
# SMART MONEY STRUCTURE
# ==========================================================

smc_structure = smc_engine.analyze(
    features,
    regime
)


print("==============================")
print("LIVE SMC STRUCTURE")
print("==============================")

print(smc_structure)



# ==========================================================
# DECISION ENGINE
# ==========================================================

decision = decision_engine.analyze(
    regime
)


print("==============================")
print("LIVE DECISION")
print("==============================")

print(decision)



print("==============================")
print("GSIS LIVE PIPELINE v14.1 COMPLETE")
print("==============================")
