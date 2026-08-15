from intelligence.risk_management_engine import RiskManagementEngine


print("==============================")
print("GSIS RISK MANAGEMENT TEST")
print("==============================")


engine = RiskManagementEngine()


position = {

    "symbol": "XAUUSD",

    "account_balance": 100000,

    "risk_amount": 500,

    "risk_percent": 0.5,

    "lot_size": 2.0,

    "entry": 2387.5,

    "stop_loss": 2387.6

}



result = engine.evaluate(
    position
)


print("==============================")
print("FINAL RISK RESULT")
print("==============================")

print(result)
