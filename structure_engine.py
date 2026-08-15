import sqlite3


DATABASE = "database/qmos.db"


print("===================================")
print("QMOS ENGINE 7 - MARKET STRUCTURE ENGINE")
print("VERSION 1.0")
print("===================================")


def create_table():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_structure (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        symbol TEXT,
        timeframe TEXT,

        timestamp INTEGER,

        swing_high REAL,
        swing_low REAL,

        structure_state TEXT,

        last_high REAL,
        last_low REAL,

        structure_score REAL,

        UNIQUE(symbol,timeframe,timestamp)

    )
    """)

    conn.commit()
    conn.close()



def detect_structure(candles):

    if len(candles) < 5:

        return None


    highs = []
    lows = []


    for i in range(2, len(candles)-2):

        current_high = candles[i][2]
        current_low = candles[i][3]


        if (
            current_high > candles[i-1][2]
            and
            current_high > candles[i+1][2]
            and
            current_high > candles[i-2][2]
            and
            current_high > candles[i+2][2]
        ):

            highs.append(current_high)



        if (
            current_low < candles[i-1][3]
            and
            current_low < candles[i+1][3]
            and
            current_low < candles[i-2][3]
            and
            current_low < candles[i+2][3]
        ):

            lows.append(current_low)



    if len(highs) < 2 or len(lows) < 2:

        return (
            None,
            None,
            "INSUFFICIENT_STRUCTURE",
            0
        )



    last_high = highs[-1]
    previous_high = highs[-2]

    last_low = lows[-1]
    previous_low = lows[-2]



    if last_high > previous_high and last_low > previous_low:

        state = "BULLISH"
        score = 1



    elif last_high < previous_high and last_low < previous_low:

        state = "BEARISH"
        score = -1



    else:

        state = "RANGE"
        score = 0



    return (

        last_high,
        last_low,
        state,
        score

    )



def run_engine():


    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()



    cursor.execute("""
    SELECT DISTINCT

    symbol,
    timeframe

    FROM candles

    """)


    markets = cursor.fetchall()



    for symbol, timeframe in markets:


        cursor.execute("""

        SELECT

        open_time,
        open,
        high,
        low,
        close

        FROM candles

        WHERE symbol=?
        AND timeframe=?

        ORDER BY open_time ASC

        """,

        (
        symbol,
        timeframe
        ))


        candles = cursor.fetchall()



        result = detect_structure(candles)



        if result is None:

            continue



        swing_high, swing_low, state, score = result



        timestamp = candles[-1][0]



        cursor.execute("""

        INSERT OR REPLACE INTO market_structure

        (

        symbol,
        timeframe,
        timestamp,

        swing_high,
        swing_low,

        structure_state,

        last_high,
        last_low,

        structure_score

        )

        VALUES

        (?,?,?,?,?,?,?,?,?)

        """,

        (

        symbol,
        timeframe,
        timestamp,

        swing_high,
        swing_low,

        state,

        swing_high,
        swing_low,

        score

        ))



        print(

        symbol,
        timeframe,
        "→",
        state,
        "Score:",
        score

        )



    conn.commit()
    conn.close()



create_table()

run_engine()



print("-----------------------------------")
print("QMOS ENGINE 7 COMPLETE")
print("MARKET STRUCTURE UPDATED")
print("-----------------------------------")
