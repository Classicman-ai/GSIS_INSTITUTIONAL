# ==========================================
# GSIS TELEGRAM ALERT ENGINE v6.0
# DUPLICATE PROTECTED DELIVERY PROTOCOL
# ==========================================

import json
import os
import requests

from datetime import datetime, timezone


BOT_TOKEN = "8715463057:AAHkVFolhP5oMIMkbcoYhHxwhNZ9J_NyVfs"
CHAT_ID = "8451554539"


SESSION_FILE = "data/session/current_session.json"
DELIVERY_FILE = "data/transparency/telegram_delivery.json"
MEMORY_FILE = "data/transparency/telegram_memory.json"


print("==============================")
print("GSIS TELEGRAM ALERT ENGINE v6.0")
print("DUPLICATE PROTECTED DELIVERY")
print("==============================")


# ------------------------------------------
# JSON HELPERS
# ------------------------------------------

def load_json(path):

    if not os.path.exists(path):
        return {}

    try:

        with open(path,"r") as f:
            return json.load(f)

    except:

        return {}



def save_json(path,data):

    with open(path,"w") as f:

        json.dump(
            data,
            f,
            indent=4
        )


# ------------------------------------------
# TELEGRAM SENDER
# ------------------------------------------

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

            "error": str(e)

        }



# ------------------------------------------
# DUPLICATE CHECK
# ------------------------------------------

def already_sent(trade_id,event):


    memory = load_json(MEMORY_FILE)


    if not isinstance(memory,list):

        memory=[]


    for item in memory:

        if (
            item.get("trade_id") == trade_id
            and item.get("event") == event
        ):

            return True


    return False



def remember(trade_id,event):


    memory = load_json(MEMORY_FILE)


    if not isinstance(memory,list):

        memory=[]


    memory.append({

        "trade_id":trade_id,

        "event":event,

        "timestamp":
        datetime.now(timezone.utc).isoformat()

    })


    save_json(
        MEMORY_FILE,
        memory
    )



# ------------------------------------------
# DELIVERY LOGGER
# ------------------------------------------

def save_delivery(record):


    data = load_json(DELIVERY_FILE)


    if not isinstance(data,list):

        data=[]


    data.append(record)


    save_json(
        DELIVERY_FILE,
        data
    )



# ------------------------------------------
# MAIN DELIVERY
# ------------------------------------------

def deliver_event(trade_id,event):


    session = load_json(
        SESSION_FILE
    )


    if session.get("status") != "ACTIVE":

        print({

            "status":"BLOCKED",

            "reason":
            "SESSION_NOT_ACTIVE"

        })

        return



    if already_sent(
        trade_id,
        event
    ):


        print({

            "trade_id":
            trade_id,

            "event":
            event,

            "status":
            "DUPLICATE_BLOCKED"

        })


        return



    session_id = session.get(
        "session_id"
    )


    message = (

        "🛡️ GSIS VERIFIED ALERT\n\n"

        f"Event: {event}\n"

        f"Trade ID: {trade_id}\n"

        f"Session: {session_id}\n"

        f"Time: "
        f"{datetime.now(timezone.utc).isoformat()}"

    )



    result = send_telegram(
        message
    )



    if result.get("ok"):


        message_id = result["result"]["message_id"]


        record = {

            "trade_id":
            trade_id,

            "event":
            event,

            "session_id":
            session_id,

            "telegram_status":
            "DELIVERED",

            "message_id":
            message_id,

            "timestamp":
            datetime.now(timezone.utc).isoformat()

        }


        save_delivery(record)


        remember(
            trade_id,
            event
        )


        print(record)



    else:


        print({

            "trade_id":
            trade_id,

            "event":
            event,

            "telegram_status":
            "FAILED",

            "telegram_response":
            result

        })



# ------------------------------------------
# TEST MODE
# ------------------------------------------

def run():


    trade_id = "GSIS-NEW-SESSION-TEST"


    events = [

        "TRADE_OPENED",

        "TP1_HIT",

        "TP2_HIT",

        "TP3_HIT",

        "TP4_HIT",

        "STOP_MOVED_BREAK_EVEN",

        "TRADE_COMPLETED"

    ]


    for event in events:

        deliver_event(
            trade_id,
            event
        )



if __name__ == "__main__":

    run()
