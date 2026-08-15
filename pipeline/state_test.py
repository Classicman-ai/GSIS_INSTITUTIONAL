from engines.state_vector_engine import StateVectorEngine


print("===================================")
print("GSIS STATE VECTOR TEST")
print("===================================")


engine = StateVectorEngine()

engine.start()


state = engine.build(
    "BTCUSDT"
)


print(state)


print("-----------------------------------")
print("STATE VECTOR COMPLETE")
