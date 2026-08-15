from engines.adapters.intelligence_adapter import IntelligenceAdapter


print("===================================")
print("GSIS INTELLIGENCE DATABASE TEST")
print("===================================")


engine = IntelligenceAdapter()


engine.start()


data = engine.get_market_state(
    "BTCUSDT"
)


print(data)


print("-----------------------------------")
print("INTELLIGENCE CONNECTION COMPLETE")
