from intelligence.trade_orchestrator import TradeOrchestrator


engine = TradeOrchestrator()



validation_result = {

    "symbol": "XAUUSD",

    "setup": "VALID",

    "direction": "SELL",

    "confidence": 100,

    "status": "APPROVED",

    "entry": 2387.5,

    "stop_loss": 2387.6

}



result = engine.process(

    validation_result,

    balance=100000,

    risk_percent=0.5

)



print("==============================")
print("FINAL GSIS ORCHESTRATOR RESULT")
print("==============================")

print(result)
