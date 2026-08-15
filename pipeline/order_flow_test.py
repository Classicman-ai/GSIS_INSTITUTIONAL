from engines.order_flow_engine import OrderFlowEngine


print("===================================")
print("GSIS ENGINE 8.3 TEST")
print("ORDER FLOW INTELLIGENCE")
print("===================================")


engine = OrderFlowEngine()

engine.start()


result = engine.calculate(
    "BTCUSDT",
    "M15"
)


print(result)


print("-----------------------------------")
print("ORDER FLOW COMPLETE")
