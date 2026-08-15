import sqlite3


DATABASE = "database/qmos.db"


print("===================================")
print("QMOS ENGINE 7.5 - MARKET INTELLIGENCE FUSION")
print("VERSION 1.0")
print("===================================")


def create_table():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_intelligence (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        symbol TEXT,
        timeframe TEXT,

        timestamp INTEGER,

        regime TEXT,
        regime_confidence REAL,

        structure_state TEXT,
        structure_break TEXT,

        change_of_character TEXT,

        final_state TEXT,

        confidence_score REAL,

        UNIQUE(symbol,timeframe,timestamp)

    )
    """)

    conn.commit()
    conn.close()



def calculate_fusion(
        regime,
        regime_conf,
        structure,
        structure_break,
        choch
):


    score = 0


    # Regime contribution

    if regime == "TRENDING_UP":
        score += 1

    elif regime == "TRENDING_DOWN":
        score -= 1



    # Structure contribution

    if structure == "BULLISH":
        score += 1

    elif structure == "BEARISH":
        score -= 1



    # Structure break

    if structure_break == "BULLISH_BREAK":
        score += 0.5

    elif structure_break == "BEARISH_BREAK":
        score -= 0.5



    # CHoCH increases transition awareness

    if choch == "TRUE":
        score *= 0.8



    if score >= 1:

        final_state = "BULLISH"

    elif score <= -1:

        final_state = "BEARISH"

    else:

        final_state = "NEUTRAL"



    confidence = min(
        abs(score) / 2,
        1
    )


    return final_state, confidence



def run_engine():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute("""
    SELECT

    r.symbol,
    r.timeframe,
    r.timestamp,

    r.regime,
    r.confidence,

    s.structure_state,
    s.structure_break,
    s.change_of_character


    FROM market_regime r

    JOIN market_structure_v2 s

    ON r.symbol = s.symbol

    AND r.timeframe = s.timeframe

    """)


    rows = cursor.fetchall()



    for row in rows:


        (
        symbol,
        timeframe,
        timestamp,

        regime,
        regime_conf,

        structure,
        structure_break,
        choch

        ) = row



        final_state, confidence = calculate_fusion(

            regime,
            regime_conf,

            structure,
            structure_break,

            choch

        )



        cursor.execute("""

        INSERT OR REPLACE INTO market_intelligence

        (

        symbol,
        timeframe,
        timestamp,

        regime,
        regime_confidence,

        structure_state,
        structure_break,

        change_of_character,

        final_state,

        confidence_score

        )

        VALUES

        (?,?,?,?,?,?,?,?,?,?)

        """,

        (

        symbol,
        timeframe,
        timestamp,

        regime,
        regime_conf,

        structure,
        structure_break,

        choch,

        final_state,

        confidence

        ))



        print(

        symbol,
        timeframe,

        "| Regime:",
        regime,

        "| Structure:",
        structure,

        "| FINAL:",
        final_state,

        "| Confidence:",
        round(confidence,2)

        )



    conn.commit()
    conn.close()



create_table()

run_engine()


print("-----------------------------------")
print("QMOS ENGINE 7.5 COMPLETE")
print("MARKET INTELLIGENCE CONNECTED")
print("-----------------------------------")
