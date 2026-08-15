from intelligence.liquidity_sweep_engine import LiquiditySweepEngine


engine = LiquiditySweepEngine()



candle = {

    "symbol": "XAUUSD",

    "timeframe": "M1",

    "open": 2386.50,

    "high": 2387.50,

    "low": 2386.00,

    "close": 2386.70

}



liquidity = {

    "buy_side_liquidity": 2387.20,

    "sell_side_liquidity": 2385.80

}



result = engine.analyze(

    candle,

    liquidity

)



print("==============================")
print("SWEEP RESULT")
print("==============================")

print(result)
