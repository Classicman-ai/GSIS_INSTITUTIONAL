from intelligence.multi_timeframe_candle_engine import MultiTimeframeCandleEngine

engine = MultiTimeframeCandleEngine()

sample = {
    "symbol": "XAUUSD",
    "timeframe": "M1",
    "open": 2386.50,
    "high": 2386.75,
    "low": 2386.45,
    "close": 2386.63,
    "timestamp": "2026-07-27T20:30:00Z"
}

engine.update(sample)

print("==============================")
print("ALL TIMEFRAMES")
print("==============================")

for tf, candle in engine.get_all().items():
    print(tf, candle)
