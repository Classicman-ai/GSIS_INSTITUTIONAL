import requests
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path


BASE = Path.home() / "GSIS"
DB = BASE / "data/gsis.db"


# Replace with your real values
BOT_TOKEN = "8715463057:AAHkVFolhP5oMIMkbcoYhHxwhNZ9J_NyVfs"
CHAT_ID = "8451554539"


print("==============================")
print("GSIS TELEGRAM TRADE ALERT ENGINE v3.0")
print("==============================")


LAST_STATUS = None
LAST_TP = None



def send_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:

        response = requests.post(
            url,
            data=payload,
            timeout=10
        )

        print(response.json())

    except Exception as e:

        print("TELEGRAM ERROR:", e)



def get_trade():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()


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


    trade = cur.fetchone()


    conn.close()


    return trade



def get_price():

    try:

        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

        data = requests.get(url,timeout=10).json()

        return float(data["price"])

    except:

        return None



def monitor_trade():


    global LAST_STATUS
    global LAST_TP


    trade = get_trade()


    if not trade:
        return



    (
    symbol,
    direction,
    entry,
    sl,
    tp1,
    tp2,
    tp3,
    tp4,
    confidence,
    status
    ) = trade



    price = get_price()


    if not price:
        return



    if LAST_STATUS != "OPEN":


        message=f"""
🟢 GSIS TRADE OPENED

Symbol:
{symbol}

Direction:
{direction}

Entry:
{entry}

Stop Loss:
{sl}

TP1:
{tp1}

TP2:
{tp2}

TP3:
{tp3}

TP4:
{tp4}

Confidence:
{confidence}%
"""

        send_message(message)

        LAST_STATUS="OPEN"



    targets=[
        ("TP1",tp1),
        ("TP2",tp2),
        ("TP3",tp3),
        ("TP4",tp4)
    ]


    for name,target in targets:


        if direction=="BUY" and price >= target:

            if LAST_TP != name:

                send_message(
f"""
🎯 GSIS {name} HIT

Symbol:
{symbol}

Direction:
{direction}

Price:
{price}

Target:
{target}

Status:
PROFIT SECURED
"""
                )

                LAST_TP=name



        if direction=="SELL" and price <= target:

            if LAST_TP != name:

                send_message(
f"""
🎯 GSIS {name} HIT

Symbol:
{symbol}

Direction:
{direction}

Price:
{price}

Target:
{target}

Status:
PROFIT SECURED
"""
                )

                LAST_TP=name




def run():

    while True:

        monitor_trade()

        time.sleep(30)



if __name__=="__main__":
    run()
