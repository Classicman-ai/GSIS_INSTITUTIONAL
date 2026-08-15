import sqlite3


DATABASE = "database/qmos.db"


print("===================================")
print("QMOS ENGINE 7.7.1 - CONFIDENCE ENGINE")
print("CALIBRATED INTELLIGENCE MODEL")
print("VERSION 1.1")
print("===================================")



def create_table():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS confidence_model (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        symbol TEXT,

        timestamp INTEGER,

        regime_score REAL,

        structure_score REAL,

        alignment_score REAL,

        data_score REAL,

        final_confidence REAL,

        confidence_state TEXT,

        UNIQUE(symbol,timestamp)

    )
    """)

    conn.commit()
    conn.close()



def state_to_score(state):

    if state is None:
        return 0


    state = state.upper()


    if "BULLISH_BREAK" in state:
        return 1


    if "BEARISH_BREAK" in state:
        return -1


    if "TRENDING_UP" in state:
        return 0.5


    if "TRENDING_DOWN" in state:
        return -0.5


    if "STRONG_BULLISH" in state:
        return 1


    if "STRONG_BEARISH" in state:
        return -1


    if "BULLISH" in state:
        return 0.5


    if "BEARISH" in state:
        return -0.5


    return 0



def confidence_label(value):

    if value >= 0.75:
        return "HIGH_CONFIDENCE"


    elif value >= 0.45:
        return "MEDIUM_CONFIDENCE"


    else:
        return "LOW_CONFIDENCE"



def run_engine():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute("""
    SELECT

    q.symbol,
    q.timestamp,

    q.macro_bias,
    q.trend_bias,
    q.execution_bias,

    m.regime,
    m.structure_state


    FROM qmos_state q

    JOIN market_intelligence m

    ON q.symbol = m.symbol

    """)


    rows = cursor.fetchall()



    processed = set()



    for row in rows:


        (
        symbol,
        timestamp,

        macro,
        trend,
        execution,

        regime,
        structure

        ) = row



        key = (symbol, timestamp)


        if key in processed:
            continue


        processed.add(key)



        regime_score = abs(
            state_to_score(regime)
        )


        structure_score = abs(
            state_to_score(structure)
        )



        alignment_values = [

            state_to_score(macro),

            state_to_score(trend),

            state_to_score(execution)

        ]



        alignment_score = abs(
            sum(alignment_values) /
            len(alignment_values)
        )



        data_score = 1.0



        final_confidence = (

            regime_score * 0.40

            +

            structure_score * 0.30

            +

            alignment_score * 0.20

            +

            data_score * 0.10

        )



        label = confidence_label(
            final_confidence
        )



        cursor.execute("""

        INSERT OR REPLACE INTO confidence_model

        (

        symbol,
        timestamp,

        regime_score,

        structure_score,

        alignment_score,

        data_score,

        final_confidence,

        confidence_state

        )

        VALUES (?,?,?,?,?,?,?,?)

        """,

        (

        symbol,

        timestamp,

        regime_score,

        structure_score,

        alignment_score,

        data_score,

        final_confidence,

        label

        ))



        print("-----------------------------------")
        print(symbol)
        print("Regime Score:", round(regime_score,2))
        print("Structure Score:", round(structure_score,2))
        print("Alignment Score:", round(alignment_score,2))
        print("Final Confidence:", round(final_confidence,2))
        print("State:", label)



    conn.commit()
    conn.close()



create_table()

run_engine()



print("-----------------------------------")
print("QMOS ENGINE 7.7.1 COMPLETE")
print("CONFIDENCE MODEL CALIBRATED")
print("-----------------------------------")
