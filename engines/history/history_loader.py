import sqlite3
import requests
from datetime import datetime, timezone
from pathlib import Path
import time


BASE = Path.home() / "GSIS"

DB = BASE / "data/candles.db"


print("==============================")
print("GSIS HISTORICAL LOADER ENGINE v2.0")
print("==============================")


def create_table():

    conn = sqlite3.connect(DB)
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



def download_history():

    url = (
        "https://api.binance.com/api/v3/klines"
        "?symbol=BTCUSDT"
        "&interval=1m"
        "&limit=1000"
    )

    try:

        response = requests.get(url, timeout=20)

        data = response.json()

        return data

    except Exception as e:

        print("DOWNLOAD ERROR:", e)

        return []



def save_candles(data):

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    count = 0


    for candle in data:

        timestamp = datetime.fromtimestamp(
            candle[0] / 1000,
            timezone.utc
        ).isoformat()


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
            float(candle[1]),
            float(candle[2]),
            float(candle[3]),
            float(candle[4]),
            float(candle[5]),
            timestamp
        ))

        count += 1


    conn.commit()
    conn.close()

    return count



def run():

    create_table()

    print("------------------------------")
    print("DOWNLOADING BTCUSDT M1 HISTORY")
    print("------------------------------")


    data = download_history()


    if data:

        count = save_candles(data)

        print("------------------------------")
        print("HISTORICAL CANDLES LOADED")
        print("DATA POINTS:", count)
        print("------------------------------")

    else:

        print("NO DATA RECEIVED")



if __name__ == "__main__":
    run()
