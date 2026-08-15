# ==========================================
# GSIS TRADE ID ENGINE v1.1
# Persistent Database Counter
# ==========================================

import sqlite3
from datetime import datetime


DB_PATH = "data/gsis.db"



def create_counter_table():

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS trade_counter (

        id INTEGER PRIMARY KEY,

        counter INTEGER

    )
    """)


    cur.execute("""
    INSERT OR IGNORE INTO trade_counter
    (id,counter)

    VALUES
    (1,0)

    """)


    conn.commit()
    conn.close()



def generate_trade_id():

    create_counter_table()


    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()


    cur.execute("""
    UPDATE trade_counter

    SET counter = counter + 1

    WHERE id = 1

    """)


    cur.execute("""
    SELECT counter
    FROM trade_counter
    WHERE id = 1

    """)


    number = cur.fetchone()[0]


    conn.commit()

    conn.close()



    date = datetime.utcnow().strftime("%Y%m%d")


    return f"GSIS-{date}-{number:05d}"
