from intelligence.position_sizing_engine import PositionSizingEngine


engine = PositionSizingEngine()


result = engine.calculate(

    symbol="XAUUSD",

    balance=100000,

    risk_percent=0.5,

    entry=2387.50,

    stop_loss=2387.60

)


print("==============================")
print("FINAL POSITION SIZE RESULT")
print("==============================")
print(result)
