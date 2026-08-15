import sqlite3
import time


DATABASE = "database/qmos.db"


print("===================================")
print("QMOS ENGINE 8.1 - LIQUIDITY MAP CORE")
print("VERSION 1.1")
print("INSTITUTIONAL LIQUIDITY DETECTION")
print("===================================")


def create_table():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS liquidity_map (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        symbol TEXT,
        timeframe TEXT,

        timestamp INTEGER,

        previous_high REAL,
        previous_low REAL,

        equal_high REAL,
        equal_low REAL,

        buy_side_liquidity REAL,
        sell_side_liquidity REAL,

        liquidity_bias TEXT,

        liquidity_score REAL,

        UNIQUE(symbol,timeframe,timestamp)

    )
    """)

    conn.commit()
    conn.close()



def get_candles(symbol, timeframe):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT high, low, close
    FROM candles
    WHERE symbol=?
    AND timeframe=?
    ORDER BY open_time DESC
    LIMIT 50
    """,
    (symbol,timeframe))

    data = cursor.fetchall()

    conn.close()

    return data



def save_liquidity(data):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    cursor.execute("""

    INSERT OR REPLACE INTO liquidity_map
    (
        symbol,
        timeframe,
        timestamp,

        previous_high,
        previous_low,

        equal_high,
        equal_low,

        buy_side_liquidity,
        sell_side_liquidity,

        liquidity_bias,

        liquidity_score
    )

    VALUES
    (
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?
    )

    """, data)


    conn.commit()
    conn.close()



def analyze(symbol,timeframe):

    candles=get_candles(symbol,timeframe)


    if len(candles)<5:

        print(
            symbol,
            timeframe,
            "INSUFFICIENT DATA"
        )

        return



    highs=[c[0] for c in candles]
    lows=[c[1] for c in candles]


    previous_high=max(highs)
    previous_low=min(lows)


    equal_high=sum(
        1 for h in highs
        if abs(h-previous_high) <= previous_high*0.001
    )


    equal_low=sum(
        1 for l in lows
        if abs(l-previous_low) <= previous_low*0.001
    )


    buy_liquidity=round(
        equal_high/len(highs),
        3
    )


    sell_liquidity=round(
        equal_low/len(highs),
        3
    )


    if buy_liquidity > sell_liquidity:

        bias="BUY_SIDE"

    elif sell_liquidity > buy_liquidity:

        bias="SELL_SIDE"

    else:

        bias="BALANCED"



    score=round(
        abs(
            buy_liquidity-sell_liquidity
        ),
        3
    )


    save_liquidity(
        (
        symbol,
        timeframe,
        int(time.time()),

        previous_high,
        previous_low,

        equal_high,
        equal_low,

        buy_liquidity,
        sell_liquidity,

        bias,

        score
        )
    )


    print(
        symbol,
        timeframe,
        "→",
        bias,
        "Score:",
        score
    )



def run_engine():

    assets=[
        "XAUTUSDT",
        "BTCUSDT",
        "ETHUSDT"
    ]


    timeframes=[
        "M1",
        "M5",
        "M15",
        "H1",
        "H4",
        "D1",
        "W1",
        "MN1"
    ]


    for asset in assets:

        for tf in timeframes:

            analyze(asset,tf)



create_table()

run_engine()


print("-----------------------------------")
print("QMOS ENGINE 8.1 COMPLETE")
print("LIQUIDITY MAP UPDATED")
print("-----------------------------------")
