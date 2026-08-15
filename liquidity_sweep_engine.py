import sqlite3
import time


DATABASE = "database/qmos.db"


print("===================================")
print("QMOS ENGINE 8.2 - LIQUIDITY SWEEP DETECTOR")
print("VERSION 1.0")
print("INSTITUTIONAL LIQUIDITY EVENT ENGINE")
print("===================================")



def create_table():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS liquidity_sweeps (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        symbol TEXT,
        timeframe TEXT,

        timestamp INTEGER,

        liquidity_type TEXT,

        sweep_status TEXT,

        direction TEXT,

        structure_state TEXT,

        regime TEXT,

        sweep_strength REAL,

        decision TEXT,

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
    liquidity_type,
    decision

    FROM liquidity_intelligence
    """)

    data = cursor.fetchall()

    conn.close()

    return data



def get_candle(symbol,timeframe):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    cursor.execute("""
    SELECT
    open,
    high,
    low,
    close

    FROM candles

    WHERE symbol=?
    AND timeframe=?

    ORDER BY open_time DESC

    LIMIT 2

    """,(symbol,timeframe))


    data = cursor.fetchall()

    conn.close()

    return data



def get_structure(symbol,timeframe):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT structure_state

    FROM market_structure_v2

    WHERE symbol=?
    AND timeframe=?

    ORDER BY timestamp DESC

    LIMIT 1

    """,(symbol,timeframe))


    result = cursor.fetchone()

    conn.close()


    return result[0] if result else "UNKNOWN"



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

    """,(symbol,timeframe))


    result = cursor.fetchone()

    conn.close()


    return result[0] if result else "UNKNOWN"



def detect_sweep(liquidity,candles):


    if len(candles) < 2:

        return (
            "NO_DATA",
            "NONE",
            0
        )


    previous = candles[1]
    current = candles[0]


    high = current[1]
    low = current[2]

    previous_high = previous[1]
    previous_low = previous[2]


    if liquidity == "BUY_SIDE":


        if high > previous_high and current[3] < current[0]:

            return (
            "DETECTED",
            "BEARISH_REJECTION",
            0.8
            )



    if liquidity == "SELL_SIDE":


        if low < previous_low and current[3] > current[0]:

            return (
            "DETECTED",
            "BULLISH_REJECTION",
            0.8
            )


    return (
    "NONE",
    "NO_REACTION",
    0
    )



def save(data):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    cursor.execute("""
    INSERT OR REPLACE INTO liquidity_sweeps

    (
    symbol,
    timeframe,
    timestamp,

    liquidity_type,

    sweep_status,

    direction,

    structure_state,

    regime,

    sweep_strength,

    decision

    )

    VALUES (?,?,?,?,?,?,?,?,?,?)

    """,data)


    conn.commit()
    conn.close()



def run():

    data=get_liquidity()


    for item in data:


        symbol=item[0]
        timeframe=item[1]
        liquidity=item[2]


        candles=get_candle(
            symbol,
            timeframe
        )


        status,direction,strength = detect_sweep(
            liquidity,
            candles
        )


        structure=get_structure(
            symbol,
            timeframe
        )


        regime=get_regime(
            symbol,
            timeframe
        )


        decision="WAIT"


        if status=="DETECTED":

            if direction=="BULLISH_REJECTION":

                decision="LONG_CONFIRMATION"

            elif direction=="BEARISH_REJECTION":

                decision="SHORT_CONFIRMATION"



        save(
        (
        symbol,
        timeframe,
        int(time.time()),

        liquidity,

        status,

        direction,

        structure,

        regime,

        strength,

        decision
        )
        )


        print(
        symbol,
        timeframe,
        "|",
        liquidity,
        "|",
        status,
        "|",
        direction,
        "|",
        decision
        )



create_table()

run()


print("-----------------------------------")
print("QMOS ENGINE 8.2 COMPLETE")
print("LIQUIDITY SWEEP DETECTION ACTIVE")
print("-----------------------------------")
