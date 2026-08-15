from intelligence.trade_planner_engine import TradePlannerEngine

planner = TradePlannerEngine()

validator = {
    "symbol": "XAUUSD",
    "setup": "VALID",
    "direction": "SELL",
    "confidence": 100,
    "status": "APPROVED"
}

order_block = {
    "symbol": "XAUUSD",
    "type": "BEARISH",
    "high": 2387.40,
    "low": 2386.90
}

fvg = {
    "symbol": "XAUUSD",
    "fvg_found": True,
    "type": "BEARISH",
    "gap_high": 2387.50,
    "gap_low": 2386.70,
    "gap_size": 0.80,
    "status": "ACTIVE"
}

result = planner.plan(
    validator,
    order_block,
    fvg
)

print("==============================")
print("FINAL TRADE PLAN")
print("==============================")
print(result)
