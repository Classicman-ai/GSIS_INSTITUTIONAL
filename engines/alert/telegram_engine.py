# ==========================================
# GSIS TELEGRAM ALERT ENGINE v7.0
# LIVE EVENT LISTENER PROTOCOL
# DUPLICATE LOCK ENABLED
# ==========================================

import json
import os
import time
import requests

from datetime import datetime, timezone


BOT_TOKEN = "8715463057:AAHkVFolhP5oMIMkbcoYhHxwhNZ9J_NyVfs"
CHAT_ID = "8451554539"


EVENT_FILE = "data/history/trade_events.json"
DELIVERY_FILE = "data/transparency/telegram_delivery.json"
MEMORY_FILE = "data/transparency/telegram_memory.json"


print("==============================")
print("GSIS TELEGRAM ALERT ENGINE v7.0")
print("LIVE EVENT LISTENER MODE")
print("==============================")


def load_json(path):

    if not os.path.exists(path):
        return []

    try:

        with open(path,"r") as f:
            return json.load(f)

    except:

        return []



def save_json(path,data):

    with open(path,"w") as f:
        json.dump(data,f,indent=4)



def send_telegram(message):

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )


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

        return response.json()


    except Exception as e:

        return {
            "error":str(e)
        }



def event_key(trade_id,event):

    return f"{trade_id}_{event}"



def already_sent(trade_id,event):

    memory = load_json(MEMORY_FILE)


    key = event_key(
        trade_id,
        event
    )


    return key in memory



def save_memory(trade_id,event):

    memory = load_json(MEMORY_FILE)


    key = event_key(
        trade_id,
        event
    )


    if key not in memory:

        memory.append(key)


    save_json(
        MEMORY_FILE,
        memory
    )



def save_delivery(record):

    data = load_json(
        DELIVERY_FILE
    )


    if not isinstance(data,list):

        data=[]


    data.append(record)


    save_json(
        DELIVERY_FILE,
        data
    )



def process_event(event):


    trade_id = event.get(
        "trade_id"
    )


    name = event.get(
        "event"
    )


    symbol = event.get(
        "symbol"
    )


    if not trade_id or not name:

        return



    if already_sent(
        trade_id,
        name
    ):

        return



    message = (

        "🛡️ GSIS TRADE UPDATE\n\n"

        f"Symbol: {symbol}\n"

        f"Trade ID: {trade_id}\n"

        f"Event: {name}\n\n"

        f"Time: "
        f"{datetime.now(timezone.utc).isoformat()}"

    )


    result = send_telegram(
        message
    )


    if result.get("ok"):


        record = {

            "trade_id":trade_id,

            "event":name,

            "telegram_status":
            "DELIVERED",

            "message_id":
            result["result"]["message_id"],

            "timestamp":
            datetime.now(timezone.utc).isoformat()

        }


        save_delivery(
            record
        )


        save_memory(
            trade_id,
            name
        )


        print(record)


    else:

        print({

            "event":name,

            "status":"FAILED",

            "response":result

        })



def run():


    events = load_json(
        EVENT_FILE
    )


    if not events:

        print("NO NEW EVENTS")

        return



    for event in events:

        process_event(
            event
        )



if __name__ == "__main__":

    run()
