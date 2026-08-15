import sqlite3
import time


DATABASE = "database/qmos.db"


print("===================================")
print("QMOS ENGINE 8.1.8 - LIQUIDITY INTELLIGENCE FUSION")
print("VERSION 1.1")
print("MULTI-LAYER LIQUIDITY DECISION MODEL")
print("===================================")



def create_table():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS liquidity_intelligence (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        symbol TEXT,
        timeframe TEXT,

        timestamp INTEGER,

        liquidity_type TEXT,

        liquidity_quality REAL,

        regime TEXT,

        structure TEXT,

        confidence REAL,

        intelligence_state TEXT,

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
    liquidity_bias,
    liquidity_score

    FROM liquidity_map
    """)

    data = cursor.fetchall()

    conn.close()

    return data



def get_quality(symbol,timeframe):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT institutional_score

    FROM liquidity_quality

    WHERE symbol=?
    AND timeframe=?

    ORDER BY timestamp DESC

    LIMIT 1

    """,(symbol,timeframe))

    result = cursor.fetchone()

    conn.close()

    return result[0] if result else 0



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



def get_confidence(symbol):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT final_confidence

    FROM confidence_model

    WHERE symbol=?

    ORDER BY timestamp DESC

    LIMIT 1

    """,(symbol,))

    result = cursor.fetchone()

    conn.close()

    return result[0] if result else 0



def decision_engine(liquidity,quality,regime,structure,confidence):


    if quality >= 0.7 and confidence >= 0.5:


        if liquidity == "BUY_SIDE" and structure == "BULLISH":

            return "POTENTIAL_LONG_AFTER_SWEEP"


        if liquidity == "SELL_SIDE" and structure == "BEARISH":

            return "POTENTIAL_SHORT_AFTER_SWEEP"



    if quality >= 0.5:

        return "WAIT_FOR_CONFIRMATION"


    return "LOW_PRIORITY"



def save(data):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    cursor.execute("""
    INSERT OR REPLACE INTO liquidity_intelligence

    (
    symbol,
    timeframe,
    timestamp,

    liquidity_type,

    liquidity_quality,

    regime,

    structure,

    confidence,

    intelligence_state,

    decision

    )

    VALUES (?,?,?,?,?,?,?,?,?,?)

    """,data)


    conn.commit()
    conn.close()



def run():

    liquidity_data = get_liquidity()


    for item in liquidity_data:


        symbol = item[0]
        timeframe = item[1]
        liquidity = item[2]


        quality = get_quality(
            symbol,
            timeframe
        )


        regime = get_regime(
            symbol,
            timeframe
        )


        structure = get_structure(
            symbol,
            timeframe
        )


        confidence = get_confidence(symbol)



        decision = decision_engine(

            liquidity,
            quality,
            regime,
            structure,
            confidence

        )


        state = "ACTIVE" if quality >= 0.5 else "WEAK"



        save(

        (
        symbol,
        timeframe,
        int(time.time()),

        liquidity,

        quality,

        regime,

        structure,

        confidence,

        state,

        decision

        )

        )


        print(
        symbol,
        timeframe,
        "| Liquidity:",
        liquidity,
        "| Quality:",
        quality,
        "| Confidence:",
        confidence,
        "| Decision:",
        decision
        )



create_table()

run()


print("-----------------------------------")
print("QMOS ENGINE 8.1.8 COMPLETE")
print("LIQUIDITY INTELLIGENCE CONNECTED")
print("-----------------------------------")
