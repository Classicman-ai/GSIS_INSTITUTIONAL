from intelligence.execution_control_engine import ExecutionControlEngine


engine = ExecutionControlEngine()


trade_plan = {

    "symbol": "XAUUSD",

    "direction": "SELL",

    "entry": 2387.50,

    "stop_loss": 2387.60,

    "tp1": 2387.40,

    "tp2": 2387.30,

    "tp3": 2387.20,

    "order_type": "MARKET",

    "status": "READY"

}


position_result = {

    "symbol": "XAUUSD",

    "lot_size": 2.0,

    "status": "APPROVED"

}


risk_result = {

    "symbol": "XAUUSD",

    "risk_amount": 500,

    "risk_percent": 0.5,

    "status": "APPROVED"

}



result = engine.validate_execution(

    trade_plan,

    risk_result,

    position_result

)



print("==============================")
print("FINAL EXECUTION CONTROL RESULT")
print("==============================")

print(result)
