from intelligence.liquidity_engine import LiquidityEngine

engine = LiquidityEngine()

candle = {

    "symbol": "XAUUSD",

    "timeframe": "M1",

    "open": 2386.50,

    "high": 2387.20,

    "low": 2385.80,

    "close": 2386.90

}

structure = {

    "structure": "BULLISH"

}

result = engine.analyze(
    candle,
    structure
)

print("==============================")
print("LIQUIDITY RESULT")
print("==============================")
print(result)
