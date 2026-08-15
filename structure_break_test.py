from intelligence.trade_validator_engine import TradeValidatorEngine


validator = TradeValidatorEngine()


liquidity = {
    "symbol": "XAUUSD",
    "timeframe": "M1",
    "buy_side_liquidity": 2387.20,
    "sell_side_liquidity": 2385.80,
    "institutional_bias": "BUY",
    "market_structure": "BULLISH"
}


sweep = {
    "symbol": "XAUUSD",
    "timeframe": "M1",
    "sweep_detected": True,
    "sweep_type": "BUY_SIDE",
    "grabbed_price": 2387.20,
    "current_price": 2386.70,
    "strength": 80,
    "institutional_signal": "SELL"
}


order_block = {
    "symbol": "XAUUSD",
    "timeframe": "M1",
    "found": True,
    "type": "BEARISH",
    "high": 2387.40,
    "low": 2386.90
}


fvg = {
    "symbol": "XAUUSD",
    "timeframe": "M1",
    "fvg_found": True,
    "type": "BEARISH",
    "gap_high": 2387.50,
    "gap_low": 2386.70,
    "gap_size": 0.80,
    "status": "ACTIVE"
}


structure = {
    "symbol": "XAUUSD",
    "timeframe": "M1",
    "structure": "BEARISH",
    "bos": False,
    "choch": True,
    "confirmation": "BEARISH_CHoCH",
    "strength": 90
}


regime = {
    "symbol": "XAUUSD",
    "timeframe": "M1",
    "regime": "RANGING",
    "trend": "BEARISH",
    "momentum": "STRONG",
    "price": 2386.70,
    "confidence": 85
}


result = validator.validate(
    liquidity,
    sweep,
    order_block,
    fvg,
    structure,
    regime
)


print("==============================")
print("FINAL VALIDATION RESULT")
print("==============================")
print(result)
