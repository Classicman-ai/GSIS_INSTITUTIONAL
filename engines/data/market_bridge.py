import sqlite3
import time
import requests
from datetime import datetime, timezone
from pathlib import Path


BASE = Path.home() / "GSIS"

DB = BASE / "data/gsis.db"


print("==============================")
print("GSIS MARKET DATA BRIDGE v2.0")
print("==============================")


def create_table():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS market_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        timeframe TEXT,
        price REAL,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()



def get_price():

    try:

        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

        r = requests.get(url, timeout=10)

        data = r.json()

        return float(data["price"])

    except Exception as e:

        print("PRICE ERROR:", e)

        return None



def save_price(price):

    conn = sqlite3.connect(DB)

    cur = conn.cursor()


    cur.execute("""
    INSERT INTO market_data
    (symbol,timeframe,price,timestamp)
    VALUES(?,?,?,?)
    """,
    (
        "BTCUSDT",
        "M1",
        price,
        datetime.now(timezone.utc).isoformat()
    ))


    conn.commit()
    conn.close()



def run():

    create_table()

    while True:

        price = get_price()


        if price:

            save_price(price)

            print("------------------------------")
            print("PRICE:", price)
            print(datetime.now(timezone.utc).isoformat())


        time.sleep(60)



if __name__ == "__main__":
    run()
