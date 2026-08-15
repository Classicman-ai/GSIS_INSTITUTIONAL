import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path


BASE = Path.home() / "GSIS"
DB = BASE / "data/gsis.db"


print("==============================")
print("GSIS TRADE SIGNAL BRIDGE v2.0")
print("==============================")


def create_table():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS trades(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        direction TEXT,
        entry REAL,
        stop_loss REAL,
        tp1 REAL,
        tp2 REAL,
        tp3 REAL,
        tp4 REAL,
        confidence REAL,
        status TEXT,
        created TEXT
    )
    """)

    conn.commit()
    conn.close()



def get_gsis_signal():

    return {
        "symbol":"BTCUSDT",
        "direction":"BUY",
        "entry":63990.00,
        "stop_loss":63800.00,
        "tp1":64060.00,
        "tp2":64150.00,
        "tp3":64250.00,
        "tp4":64400.00,
        "confidence":91
    }



def save_trade(signal):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()


    cur.execute("""
    SELECT COUNT(*)
    FROM trades
    WHERE status='ACTIVE'
    """)

    active = cur.fetchone()[0]


    if active > 0:

        print("ACTIVE TRADE ALREADY EXISTS")
        conn.close()
        return



    cur.execute("""
    INSERT INTO trades
    (
    symbol,
    direction,
    entry,
    stop_loss,
    tp1,
    tp2,
    tp3,
    tp4,
    confidence,
    status,
    created
    )

    VALUES(?,?,?,?,?,?,?,?,?,?,?)
    """,
    (
    signal["symbol"],
    signal["direction"],
    signal["entry"],
    signal["stop_loss"],
    signal["tp1"],
    signal["tp2"],
    signal["tp3"],
    signal["tp4"],
    signal["confidence"],
    "ACTIVE",
    datetime.now(timezone.utc).isoformat()
    ))


    conn.commit()
    conn.close()


    print("------------------------------")
    print("NEW ACTIVE GSIS TRADE")
    print(signal)



def run():

    create_table()


    while True:

        signal=get_gsis_signal()

        save_trade(signal)

        time.sleep(60)



if __name__=="__main__":
    run()
