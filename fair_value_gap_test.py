from intelligence.fair_value_gap_engine import FairValueGapEngine


engine = FairValueGapEngine()


candle = {

    "symbol": "XAUUSD",

    "timeframe": "M1",

    "open": 2387.20,

    "high": 2387.50,

    "low": 2386.20,

    "close": 2386.70

}


order_block = {

    "type": "BEARISH"

}


result = engine.analyze(

    candle,

    order_block

)


print("==============================")
print("FVG RESULT")
print("==============================")

print(result)
