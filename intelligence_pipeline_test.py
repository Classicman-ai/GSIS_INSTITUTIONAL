from datetime import datetime, timezone


# ==========================================================
# ENGINE IMPORTS
# ==========================================================

from intelligence.historical_replay_engine import HistoricalReplayEngine
from intelligence.statistical_engine import StatisticalEngine
from intelligence.feature_memory_engine import FeatureMemoryEngine
from intelligence.market_regime_engine import MarketRegimeEngine
from intelligence.smc_structure_engine import SMCStructureEngine
from intelligence.decision_engine import DecisionEngine

from intelligence.pattern_memory_engine import PatternMemoryEngine
from intelligence.pattern_recognition_engine import PatternRecognitionEngine

from intelligence.outcome_memory_engine import OutcomeMemoryEngine
from intelligence.adaptive_confidence_engine import AdaptiveConfidenceEngine

from intelligence.risk_intelligence_engine import RiskIntelligenceEngine
from intelligence.trade_setup_engine import TradeSetupEngine
from intelligence.execution_queue_engine import ExecutionQueueEngine

from intelligence.capital_management_engine import CapitalManagementEngine
from intelligence.trade_journal_engine import TradeJournalEngine



print("==============================")
print("GSIS GOLD PIPELINE v13.0")
print("==============================")
print("XAUUSD INSTITUTIONAL INTELLIGENCE ACTIVE")
print("==============================")


# ==========================================================
# INITIALIZE ENGINES
# ==========================================================

replay_engine = HistoricalReplayEngine()
stat_engine = StatisticalEngine()

feature_memory_engine = FeatureMemoryEngine()

regime_engine = MarketRegimeEngine()

# NEW SMC ENGINE
smc_engine = SMCStructureEngine()

decision_engine = DecisionEngine()


pattern_memory_engine = PatternMemoryEngine()
pattern_recognition_engine = PatternRecognitionEngine()


outcome_engine = OutcomeMemoryEngine()
confidence_engine = AdaptiveConfidenceEngine()


risk_engine = RiskIntelligenceEngine()

trade_setup_engine = TradeSetupEngine()

execution_engine = ExecutionQueueEngine()

capital_engine = CapitalManagementEngine()

journal_engine = TradeJournalEngine()



# ==========================================================
# HISTORICAL REPLAY
# ==========================================================

candle = replay_engine.load(
    "XAUUSD",
    "M1"
)


print("==============================")
print("XAUUSD REPLAY CANDLE LOADED")
print("==============================")

print(candle)



# ==========================================================
# STATISTICAL FEATURES
# ==========================================================

features = stat_engine.calculate(
    candle
)


print("==============================")
print("GSIS GOLD FEATURES")
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
print("GSIS MARKET REGIME")
print("==============================")

print(regime)



# ==========================================================
# SMC STRUCTURE ANALYSIS  NEW
# ==========================================================

smc_structure = smc_engine.analyze(
    features,
    regime
)


print("==============================")
print("GSIS SMART MONEY STRUCTURE")
print("==============================")

print(smc_structure)



# ==========================================================
# DECISION ENGINE
# ==========================================================

decision = decision_engine.analyze(
    {
        **regime,
        **smc_structure
    }
)


print("==============================")
print("GSIS GOLD DECISION")
print("==============================")

print(decision)



# ==========================================================
# PATTERN MEMORY
# ==========================================================

pattern = pattern_memory_engine.store(
    decision
)


print("==============================")
print("GSIS EXPERIENCE MEMORY")
print("==============================")

print(pattern)



# ==========================================================
# PATTERN RECOGNITION
# ==========================================================

pattern_result = pattern_recognition_engine.analyze(
    pattern
)


print("==============================")
print("GSIS PATTERN RESULT")
print("==============================")

print(pattern_result)



# ==========================================================
# OUTCOME
# ==========================================================

outcome = outcome_engine.evaluate(
    decision
)


print("==============================")
print("GSIS OUTCOME")
print("==============================")

print(outcome)



# ==========================================================
# CONFIDENCE
# ==========================================================

confidence = confidence_engine.process(
    outcome
)


print("==============================")
print("GSIS CONFIDENCE")
print("==============================")

print(confidence)



# ==========================================================
# RISK
# ==========================================================

risk = risk_engine.evaluate(
    confidence
)


print("==============================")
print("GSIS RISK")
print("==============================")

print(risk)



# ==========================================================
# TRADE SETUP
# ==========================================================

setup = trade_setup_engine.generate(
    risk
)


print("==============================")
print("GSIS TRADE SETUP")
print("==============================")

print(setup)



# ==========================================================
# EXECUTION
# ==========================================================

execution = execution_engine.process(
    setup
)


print("==============================")
print("GSIS EXECUTION")
print("==============================")

print(execution)



# ==========================================================
# CAPITAL
# ==========================================================

capital = capital_engine.calculate(
    execution
)


print("==============================")
print("GSIS CAPITAL")
print("==============================")

print(capital)



# ==========================================================
# JOURNAL
# ==========================================================

journal = journal_engine.record(
    setup
)


print("==============================")
print("GSIS JOURNAL")
print("==============================")

print(journal)



print("==============================")
print("GSIS GOLD PIPELINE v13.0 COMPLETE")
print("==============================")
