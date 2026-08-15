# ==========================================
# GSIS TELEGRAM ALERT ENGINE v4.0
# TRANSPARENT DELIVERY PROTOCOL
# ==========================================

import requests
import json
import os
from datetime import datetime, timezone
from pathlib import Path


BASE = Path.home() / "GSIS"

DELIVERY_FILE = BASE / "data/transparency/telegram_delivery.json"
EVENT_FILE = BASE / "data/history/trade_events.json"


BOT_TOKEN = "8715463057:AAHkVFolhP5oMIMkbcoYhHxwhNZ9J_NyVfs"
CHAT_ID = "8451554539"


print("==============================")
print("GSIS TELEGRAM ALERT ENGINE v4.0")
print("TRANSPARENT DELIVERY PROTOCOL")
print("==============================")


def load_json(path, default):

    if not path.exists():
        return default

    try:
        with open(path, "r") as f:
            return json.load(f)

    except:
        return default



def save_json(path, data):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(path, "w") as f:
        json.dump(
            data,
            f,
            indent=4
        )



def send_telegram(message, trade_id, event):

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

        result = response.json()


        if result.get("ok"):

            delivery = load_json(
                DELIVERY_FILE,
                []
            )


            record = {

                "trade_id": trade_id,

                "event": event,

                "telegram_status": "DELIVERED",

                "message_id":
                result["result"]["message_id"],

                "timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat()

            }


            delivery.append(record)

            save_json(
                DELIVERY_FILE,
                delivery
            )


            print(record)

            return True


        else:

            print(
                "TELEGRAM FAILED",
                result
            )

            return False


    except Exception as e:

        print(
            "TELEGRAM ERROR:",
            e
        )

        return False



def process_events():

    events = load_json(
        EVENT_FILE,
        []
    )


    if not events:

        print("NO EVENTS")

        return



    for event in events[-10:]:

        trade_id = event.get(
            "trade_id"
        )

        event_name = event.get(
            "event"
        )


        message = f"""
🛡️ GSIS TRANSPARENT TRADE UPDATE

Trade ID:
{trade_id}

Event:
{event_name}

Symbol:
{event.get('symbol')}

Status:
VERIFIED DELIVERY

Time:
{datetime.now(timezone.utc).isoformat()}
"""


        send_telegram(
            message,
            trade_id,
            event_name
        )



if __name__ == "__main__":

    process_events()
