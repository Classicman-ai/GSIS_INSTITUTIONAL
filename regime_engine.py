import sqlite3
from config import DATABASE


print("===================================")
print("QMOS ENGINE 6 - MARKET REGIME ENGINE")
print("VERSION 1.1")
print("===================================")


def create_table():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_regime (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        symbol TEXT,
        timeframe TEXT,

        timestamp INTEGER,

        trend_state TEXT,
        trend_score REAL,

        volatility_state TEXT,
        volatility_score REAL,

        momentum_state TEXT,
        momentum_score REAL,

        regime TEXT,
        confidence REAL,

        UNIQUE(symbol,timeframe,timestamp)

    )
    """)

    conn.commit()
    conn.close()



def classify_regime(
        return_pct,
        volatility,
        ema20,
        ema50,
        ema200
):

    # Trend calculation

    if ema20 and ema50 and ema200:

        if ema20 > ema50 > ema200:

            trend_state = "UP"
            trend_score = 1

        elif ema20 < ema50 < ema200:

            trend_state = "DOWN"
            trend_score = -1

        else:

            trend_state = "MIXED"
            trend_score = 0

    else:

        trend_state = "UNKNOWN"
        trend_score = 0



    # Volatility calculation

    if volatility is None:

        volatility = 0


    if volatility > 0.5:

        volatility_state = "EXPANSION"
        volatility_score = 1

    else:

        volatility_state = "NORMAL"
        volatility_score = 0.5



    # Momentum calculation

    if return_pct > 0:

        momentum_state = "POSITIVE"
        momentum_score = 1

    else:

        momentum_state = "NEGATIVE"
        momentum_score = -1



    # Final regime

    if trend_state == "UP":

        regime = "TRENDING_UP"

    elif trend_state == "DOWN":

        regime = "TRENDING_DOWN"

    elif volatility_state == "EXPANSION":

        regime = "VOLATILITY_EXPANSION"

    else:

        regime = "RANGE"



    confidence = (
        abs(trend_score)
        +
        volatility_score
        +
        abs(momentum_score)

    ) / 3



    return (
        trend_state,
        trend_score,

        volatility_state,
        volatility_score,

        momentum_state,
        momentum_score,

        regime,
        confidence
    )



def run_engine():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute("""
    SELECT

    symbol,
    timeframe,
    timestamp,

    return_pct,
    volatility,

    ema20,
    ema50,
    ema200

    FROM features

    """)


    rows = cursor.fetchall()


    for row in rows:

        (
        symbol,
        timeframe,
        timestamp,

        return_pct,
        volatility,

        ema20,
        ema50,
        ema200

        ) = row



        result = classify_regime(

            return_pct,
            volatility,

            ema20,
            ema50,
            ema200

        )



        cursor.execute("""

        INSERT OR REPLACE INTO market_regime

        (

        symbol,
        timeframe,
        timestamp,

        trend_state,
        trend_score,

        volatility_state,
        volatility_score,

        momentum_state,
        momentum_score,

        regime,
        confidence

        )

        VALUES

        (?,?,?,?,?,?,?,?,?,?,?)

        """,

        (

        symbol,
        timeframe,
        timestamp,

        result[0],
        result[1],

        result[2],
        result[3],

        result[4],
        result[5],

        result[6],
        result[7]

        ))



        print(

        symbol,
        timeframe,
        "→",
        result[6],
        "Confidence:",
        round(result[7],2)

        )



    conn.commit()
    conn.close()



create_table()

run_engine()


print("-----------------------------------")
print("QMOS ENGINE 6 COMPLETE")
print("MARKET REGIME UPDATED")
print("-----------------------------------")
