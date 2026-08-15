import sqlite3
import time


DATABASE = "database/qmos.db"


print("===================================")
print("QMOS ENGINE 7.9.1 - PIPELINE HISTORY LOGGER")
print("VERSION 1.0")
print("AUDIT AND EXECUTION MEMORY LAYER")
print("===================================")



def create_history_table():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipeline_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        engine_name TEXT,

        engine_version TEXT,

        status TEXT,

        execution_time REAL,

        timestamp INTEGER,

        message TEXT

    )
    """)


    conn.commit()
    conn.close()



def read_pipeline():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    cursor.execute("""
    SELECT
    engine_name,
    engine_version,
    status,
    message
    FROM pipeline_status
    """)


    rows = cursor.fetchall()

    conn.close()

    return rows



def save_history(
    engine,
    version,
    status,
    execution,
    message
):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    cursor.execute("""

    INSERT INTO pipeline_history

    (

    engine_name,

    engine_version,

    status,

    execution_time,

    timestamp,

    message

    )

    VALUES (?,?,?,?,?,?)

    """,

    (

    engine,

    version,

    status,

    execution,

    int(time.time()),

    message

    ))


    conn.commit()
    conn.close()



def run_history():

    start=time.time()


    engines = read_pipeline()


    for engine,version,status,message in engines:


        execution = round(time.time()-start,4)


        save_history(

            engine,

            version,

            status,

            execution,

            message

        )


        print("-----------------------------------")
        print(engine)
        print("VERSION:",version)
        print("STATUS:",status)
        print("LOGGED")



    print("-----------------------------------")
    print("PIPELINE HISTORY UPDATED")



create_history_table()

run_history()


print("-----------------------------------")
print("QMOS ENGINE 7.9.1 COMPLETE")
print("AUDIT MEMORY ACTIVE")
print("-----------------------------------")
