import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path


BASE = Path.home() / "GSIS"

MARKET_DB = BASE / "data/gsis.db"
CANDLE_DB = BASE / "data/candles.db"


print("==============================")
print("GSIS CANDLE BUILDER ENGINE v3.0")
print("==============================")


def create_table():

    conn = sqlite3.connect(CANDLE_DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS candles(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        timeframe TEXT,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()



def build_candle():

    market = sqlite3.connect(MARKET_DB)
    cur = market.cursor()

    cur.execute("""
    SELECT price 
    FROM market_data
    WHERE symbol='BTCUSDT'
    ORDER BY id DESC
    LIMIT 60
    """)

    rows = cur.fetchall()
    market.close()


    if len(rows) < 2:
        return


    prices = [r[0] for r in rows]


    candle_open = prices[-1]
    candle_close = prices[0]
    candle_high = max(prices)
    candle_low = min(prices)
    volume = len(prices)


    conn = sqlite3.connect(CANDLE_DB)
    cur = conn.cursor()


    cur.execute("""
    INSERT INTO candles
    (
    symbol,
    timeframe,
    open,
    high,
    low,
    close,
    volume,
    timestamp
    )
    VALUES(?,?,?,?,?,?,?,?)
    """,
    (
        "BTCUSDT",
        "M1",
        candle_open,
        candle_high,
        candle_low,
        candle_close,
        volume,
        datetime.now(timezone.utc).isoformat()
    ))


    conn.commit()
    conn.close()


    print("------------------------------")
    print("CANDLE CREATED")
    print("OPEN:", candle_open)
    print("HIGH:", candle_high)
    print("LOW:", candle_low)
    print("CLOSE:", candle_close)
    print("VOLUME:", volume)



def run():

    create_table()

    while True:

        build_candle()

        time.sleep(60)



if __name__ == "__main__":
    run()
