import sqlite3
from config import DATABASE

def get_connection():
    return sqlite3.connect(DATABASE)

def save_candle(symbol, timeframe, candle):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO candles(
        symbol,
        timeframe,
        open_time,
        open,
        high,
        low,
        close,
        volume,
        close_time
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        symbol,
        timeframe,
        candle[0],
        float(candle[1]),
        float(candle[2]),
        float(candle[3]),
        float(candle[4]),
        float(candle[5]),
        candle[6]
    ))

    conn.commit()
    conn.close()
