import sqlite3
import time


DATABASE = "database/qmos.db"


print("===================================")
print("QMOS ENGINE 7.9 - PIPELINE CONTROLLER")
print("VERSION 1.0")
print("SYSTEM SYNCHRONIZATION LAYER")
print("===================================")



def create_table():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipeline_status (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        engine_name TEXT,

        engine_version TEXT,

        status TEXT,

        last_update INTEGER,

        message TEXT,

        UNIQUE(engine_name)

    )
    """)


    conn.commit()
    conn.close()



def check_table(cursor, table):

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table,)
    )

    result = cursor.fetchone()

    return result is not None



def register_engine(cursor, name, version, status, message):

    cursor.execute("""

    INSERT OR REPLACE INTO pipeline_status

    (

    engine_name,

    engine_version,

    status,

    last_update,

    message

    )

    VALUES (?,?,?,?,?)

    """,

    (

    name,

    version,

    status,

    int(time.time()),

    message

    ))



def run_controller():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    dependencies = [

        ("ENGINE_01_DATA", "1.0", "candles"),

        ("ENGINE_05_STATISTICS", "1.0", "features"),

        ("ENGINE_06_REGIME", "1.1", "market_regime"),

        ("ENGINE_07_STRUCTURE", "2.0", "market_structure_v2"),

        ("ENGINE_07.5_INTELLIGENCE", "1.0", "market_intelligence"),

        ("ENGINE_07.6_MODEL", "1.0", "qmos_state"),

        ("ENGINE_07.7_CONFIDENCE", "1.1", "confidence_model"),

        ("ENGINE_07.8_MEMORY", "1.0", "decision_memory")

    ]


    system_ready = True



    for engine,version,table in dependencies:


        if check_table(cursor,table):


            status="READY"

            message="Database layer available"


        else:


            status="MISSING"

            message=f"Missing table: {table}"

            system_ready=False



        register_engine(

            cursor,

            engine,

            version,

            status,

            message

        )



        print("-----------------------------------")
        print(engine)
        print("Status:",status)
        print(message)



    print("-----------------------------------")


    if system_ready:


        print("QMOS PIPELINE STATUS: READY")

        register_engine(

            cursor,

            "SYSTEM",

            "7.9",

            "READY",

            "All intelligence layers synchronized"

        )


    else:


        print("QMOS PIPELINE STATUS: BLOCKED")


        register_engine(

            cursor,

            "SYSTEM",

            "7.9",

            "BLOCKED",

            "Missing intelligence layer"

        )



    conn.commit()

    conn.close()



create_table()

run_controller()



print("-----------------------------------")
print("QMOS ENGINE 7.9 COMPLETE")
print("PIPELINE SYNCHRONIZATION ACTIVE")
print("-----------------------------------")
