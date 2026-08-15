import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
import requests


BASE = Path.home() / "GSIS"
DB = BASE / "data/gsis.db"


print("==============================")
print("GSIS TRADE MANAGER ENGINE v2.1")
print("==============================")


def get_price():

    try:
        url="https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

        data=requests.get(url,timeout=10).json()

        return float(data["price"])

    except:

        return None



def get_active_trade():

    conn=sqlite3.connect(DB)

    cur=conn.cursor()

    cur.execute("""
    SELECT
    symbol,
    direction,
    entry,
    stop_loss,
    tp1,
    tp2,
    tp3,
    tp4,
    confidence,
    status
    FROM trades
    WHERE status='ACTIVE'
    ORDER BY id DESC
    LIMIT 1
    """)

    trade=cur.fetchone()

    conn.close()

    return trade



def monitor(price):

    trade=get_active_trade()


    if not trade:

        print("WAITING FOR GSIS SIGNAL")
        return



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
    status
    )=trade



    print("------------------------------")
    print("ACTIVE TRADE")
    print(symbol,direction)

    print("ENTRY:",entry)
    print("SL:",stop_loss)

    print("TP1:",tp1)
    print("TP2:",tp2)
    print("TP3:",tp3)
    print("TP4:",tp4)

    print("CONFIDENCE:",confidence)


    if direction=="BUY":

        if price >= tp1:
            print("✅ TP1 HIT")

        if price >= tp2:
            print("✅ TP2 HIT")

        if price >= tp3:
            print("✅ TP3 HIT")

        if price >= tp4:
            print("🏆 TP4 HIT")


        if price <= stop_loss:
            print("❌ STOP LOSS HIT")



    if direction=="SELL":

        if price <= tp1:
            print("✅ TP1 HIT")

        if price <= tp2:
            print("✅ TP2 HIT")

        if price <= tp3:
            print("✅ TP3 HIT")

        if price <= tp4:
            print("🏆 TP4 HIT")


        if price >= stop_loss:
            print("❌ STOP LOSS HIT")




def run():

    while True:

        price=get_price()

        if price:

            print("PRICE:",price)

            monitor(price)


        time.sleep(30)



if __name__=="__main__":
    run()
