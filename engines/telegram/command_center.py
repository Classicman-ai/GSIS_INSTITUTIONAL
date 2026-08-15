import requests
import sqlite3
import time
from pathlib import Path
from datetime import datetime, timezone


BASE = Path.home() / "GSIS"
DB = BASE / "data/gsis.db"


BOT_TOKEN = "8715463057:AAHkVFolhP5oMIMkbcoYhHxwhNZ9J_NyVfs"


print("==============================")
print("GSIS TELEGRAM COMMAND CENTER v1.0")
print("==============================")


def send_message(chat_id, text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text
    }

    requests.post(url, data=data)



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



def system_status():

    return """
🟢 GSIS SYSTEM STATUS

Core:
ONLINE

Signal Engine:
ONLINE

Trade Manager:
ONLINE

Telegram:
ONLINE
"""



def trade_status():

    trade = get_trade()

    if not trade:

        return "No active trade."



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


    return f"""
📊 GSIS ACTIVE TRADE

Symbol:
{symbol}

Direction:
{direction}

Entry:
{entry}

SL:
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

Status:
{status}
"""



def process_command(message,chat_id):


    if message == "/status":

        send_message(chat_id,system_status())


    elif message == "/trade":

        send_message(chat_id,trade_status())


    elif message == "/signal":

        send_message(
        chat_id,
        "🧠 GSIS SIGNAL ENGINE\n\nMonitoring market conditions."
        )


    elif message == "/risk":

        send_message(
        chat_id,
        "🛡 GSIS RISK ENGINE\n\nRisk monitoring active."
        )


    elif message == "/help":

        send_message(
        chat_id,
"""
🤖 GSIS COMMANDS

/status
/trade
/signal
/risk
/help
"""
        )



def run():

    offset=None


    while True:


        url=f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"


        params={}


        if offset:

            params["offset"]=offset



        try:

            data=requests.get(
                url,
                params=params,
                timeout=30
            ).json()


            if data.get("ok"):


                for update in data["result"]:


                    offset=update["update_id"]+1


                    if "message" in update:


                        msg=update["message"]

                        text=msg.get("text","")

                        chat_id=msg["chat"]["id"]


                        process_command(
                            text,
                            chat_id
                        )


        except Exception as e:

            print(e)


        time.sleep(2)



if __name__=="__main__":

    run()
