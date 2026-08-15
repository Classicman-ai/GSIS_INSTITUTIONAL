import sqlite3
import time


DATABASE = "database/qmos.db"


print("===================================")
print("QMOS ENGINE 8.1.5 - LIQUIDITY QUALITY FILTER")
print("VERSION 1.0")
print("INSTITUTIONAL LIQUIDITY VALIDATION")
print("===================================")



def create_table():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS liquidity_quality (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        symbol TEXT,
        timeframe TEXT,

        timestamp INTEGER,

        liquidity_type TEXT,

        distance_from_price REAL,

        structure_alignment REAL,

        regime_alignment REAL,

        freshness_score REAL,

        institutional_score REAL,

        UNIQUE(symbol,timeframe,timestamp)

    )
    """)

    conn.commit()
    conn.close()



def get_liquidity():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
    symbol,
    timeframe,
    liquidity_bias,
    liquidity_score

    FROM liquidity_map
    """)

    data = cursor.fetchall()

    conn.close()

    return data



def get_structure(symbol,timeframe):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
    structure_state

    FROM market_structure_v2

    WHERE symbol=?
    AND timeframe=?

    ORDER BY timestamp DESC

    LIMIT 1
    """,
    (symbol,timeframe))


    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return "UNKNOWN"



def get_regime(symbol,timeframe):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT regime

    FROM market_regime

    WHERE symbol=?
    AND timeframe=?

    ORDER BY timestamp DESC

    LIMIT 1
    """,
    (symbol,timeframe))


    result=cursor.fetchone()

    conn.close()


    if result:
        return result[0]

    return "UNKNOWN"



def save_quality(data):

    conn=sqlite3.connect(DATABASE)
    cursor=conn.cursor()


    cursor.execute("""

    INSERT OR REPLACE INTO liquidity_quality

    (
    symbol,
    timeframe,
    timestamp,

    liquidity_type,

    distance_from_price,

    structure_alignment,

    regime_alignment,

    freshness_score,

    institutional_score

    )

    VALUES

    (?,?,?,?,?,?,?,?,?)

    """,data)


    conn.commit()
    conn.close()



def analyze():

    liquidity=get_liquidity()


    for row in liquidity:

        symbol=row[0]
        timeframe=row[1]
        bias=row[2]
        score=row[3]


        structure=get_structure(symbol,timeframe)

        regime=get_regime(symbol,timeframe)



        # Structure alignment

        structure_score=0


        if bias=="BUY_SIDE" and structure=="BULLISH":

            structure_score=1


        elif bias=="SELL_SIDE" and structure=="BEARISH":

            structure_score=1


        elif structure=="RANGE":

            structure_score=0.5



        # Regime alignment

        regime_score=0


        if "UP" in regime and bias=="BUY_SIDE":

            regime_score=1


        elif "DOWN" in regime and bias=="SELL_SIDE":

            regime_score=1



        # Freshness based on liquidity strength

        freshness=min(score*2,1)



        institutional_score=round(

            (
            structure_score+
            regime_score+
            freshness

            )/3,

            2
        )


        save_quality(

        (
        symbol,
        timeframe,
        int(time.time()),

        bias,

        0,

        structure_score,

        regime_score,

        freshness,

        institutional_score

        )

        )


        print(
        symbol,
        timeframe,
        "|",
        bias,
        "| Structure:",
        structure_score,
        "| Regime:",
        regime_score,
        "| Quality:",
        institutional_score
        )



create_table()

analyze()


print("-----------------------------------")
print("QMOS ENGINE 8.1.5 COMPLETE")
print("LIQUIDITY QUALITY UPDATED")
print("-----------------------------------")
