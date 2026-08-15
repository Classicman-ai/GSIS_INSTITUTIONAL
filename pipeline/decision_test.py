from engines.decision_fusion_engine import DecisionFusionEngine


print("===================================")
print("GSIS DECISION FUSION TEST")
print("===================================")


engine = DecisionFusionEngine()

engine.start()


result = engine.analyze(
    "BTCUSDT"
)


print(result)


print("-----------------------------------")
print("DECISION FUSION COMPLETE")
