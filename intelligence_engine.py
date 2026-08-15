import sqlite3


DATABASE = "database/qmos.db"


print("===================================")
print("QMOS ENGINE 7.6 - INTELLIGENCE ENGINE")
print("WEIGHTED MULTI-TIMEFRAME MODEL")
print("===================================")



def create_table():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qmos_state (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        symbol TEXT,
        timestamp INTEGER,

        macro_bias TEXT,
        trend_bias TEXT,
        execution_bias TEXT,

        total_score REAL,

        confidence REAL,

        risk_state TEXT,

        UNIQUE(symbol,timestamp)

    )
    """)

    conn.commit()
    conn.close()



def state_score(regime, structure):

    score = 0


    # Regime weight 40%

    if regime == "TRENDING_UP":
        score += 0.4

    elif regime == "TRENDING_DOWN":
        score -= 0.4


    # Structure weight 40%

    if structure == "BULLISH":
        score += 0.4

    elif structure == "BEARISH":
        score -= 0.4


    return score



def classify(score):

    if score >= 0.6:
        return "STRONG_BULLISH"

    elif score >= 0.2:
        return "BULLISH"

    elif score <= -0.6:
        return "STRONG_BEARISH"

    elif score <= -0.2:
        return "BEARISH"

    else:
        return "NEUTRAL"



def timeframe_group(tf):

    if tf in ["MN1","W1","D1"]:
        return "macro"

    elif tf in ["H4","H1"]:
        return "trend"

    else:
        return "execution"



def run_engine():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    cursor.execute("""
    SELECT

    symbol,
    timeframe,
    timestamp,

    regime,
    structure_state


    FROM market_intelligence

    """)


    rows = cursor.fetchall()


    data={}



    for r in rows:

        symbol,tf,time,regime,structure=r


        score=state_score(
            regime,
            structure
        )


        if symbol not in data:

            data[symbol]={
                "macro":[],
                "trend":[],
                "execution":[]
            }


        data[symbol][
            timeframe_group(tf)
        ].append(score)



    for symbol,groups in data.items():


        macro=sum(groups["macro"])/max(len(groups["macro"]),1)

        trend=sum(groups["trend"])/max(len(groups["trend"]),1)

        execution=sum(groups["execution"])/max(len(groups["execution"]),1)



        total=(

            macro*0.5
            +
            trend*0.3
            +
            execution*0.2

        )


        bias=classify(total)


        confidence=abs(total)



        risk="NORMAL"


        if confidence <0.3:
            risk="LOW_CONFIDENCE"



        cursor.execute("""

        INSERT OR REPLACE INTO qmos_state

        (

        symbol,
        timestamp,

        macro_bias,
        trend_bias,
        execution_bias,

        total_score,

        confidence,

        risk_state

        )

        VALUES (?,?,?,?,?,?,?,?)

        """,

        (

        symbol,

        int(time),

        classify(macro),
        classify(trend),
        classify(execution),

        total,

        confidence,

        risk

        ))



        print("-----------------------------------")
        print(symbol)
        print("MACRO:",classify(macro))
        print("TREND:",classify(trend))
        print("EXECUTION:",classify(execution))
        print("FINAL:",bias)
        print("CONFIDENCE:",round(confidence,2))



    conn.commit()
    conn.close()



create_table()
run_engine()


print("-----------------------------------")
print("QMOS ENGINE 7.6 COMPLETE")
print("INTELLIGENCE MODEL UPGRADED")
print("-----------------------------------")
