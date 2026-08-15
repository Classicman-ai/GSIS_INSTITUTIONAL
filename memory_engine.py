import sqlite3


DATABASE = "database/qmos.db"


print("===================================")
print("QMOS ENGINE 7.8 - DECISION MEMORY ENGINE")
print("VERSION 1.0")
print("===================================")



def create_table():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS decision_memory (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        symbol TEXT,

        timestamp INTEGER,

        previous_confidence REAL,

        current_confidence REAL,

        confidence_change REAL,

        previous_state TEXT,

        current_state TEXT,

        transition TEXT,

        intelligence_condition TEXT,

        UNIQUE(symbol,timestamp)

    )
    """)


    conn.commit()
    conn.close()



def classify_transition(change):

    if change > 0.20:
        return "ACCELERATION"

    elif change < -0.20:
        return "DETERIORATION"

    else:
        return "STABLE"



def condition(state, confidence):

    if state == "HIGH_CONFIDENCE":
        return "ACTIVE"

    elif state == "MEDIUM_CONFIDENCE":
        return "DEVELOPING"

    else:
        return "UNCERTAIN"



def run_engine():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute("""
    SELECT

    symbol,
    timestamp,
    final_confidence,
    confidence_state

    FROM confidence_model

    ORDER BY timestamp ASC

    """)


    rows = cursor.fetchall()


    history = {}



    for row in rows:


        symbol, timestamp, confidence, state = row


        if symbol not in history:


            previous_confidence = 0

            previous_state = "NONE"


        else:


            previous_confidence = history[symbol]["confidence"]

            previous_state = history[symbol]["state"]



        change = confidence - previous_confidence



        transition = classify_transition(change)



        current_condition = condition(
            state,
            confidence
        )



        cursor.execute("""

        INSERT OR REPLACE INTO decision_memory

        (

        symbol,
        timestamp,

        previous_confidence,

        current_confidence,

        confidence_change,

        previous_state,

        current_state,

        transition,

        intelligence_condition

        )

        VALUES (?,?,?,?,?,?,?,?,?)

        """,

        (

        symbol,

        timestamp,

        previous_confidence,

        confidence,

        change,

        previous_state,

        state,

        transition,

        current_condition

        ))



        print("-----------------------------------")
        print(symbol)
        print("Previous:", previous_state, round(previous_confidence,2))
        print("Current:", state, round(confidence,2))
        print("Change:", round(change,2))
        print("Transition:", transition)
        print("Condition:", current_condition)



        history[symbol]={

            "confidence":confidence,

            "state":state

        }



    conn.commit()
    conn.close()



create_table()

run_engine()



print("-----------------------------------")
print("QMOS ENGINE 7.8 COMPLETE")
print("DECISION MEMORY UPDATED")
print("-----------------------------------")
