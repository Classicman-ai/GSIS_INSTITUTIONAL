# ==========================================
# GSIS TELEGRAM TRADE ALERT ENGINE v1.0
# ==========================================

import json
import os
import urllib.request
import urllib.parse


EVENT_FILE = "data/history/trade_events.json"
SENT_FILE = "data/history/sent_alerts.json"


# Add your Telegram values here
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"



def load_json(file):

    if not os.path.exists(file):
        return []

    with open(file,"r") as f:
        return json.load(f)



def save_json(file,data):

    with open(file,"w") as f:
        json.dump(
            data,
            f,
            indent=4
        )



def send_message(text):

    if BOT_TOKEN == "YOUR_BOT_TOKEN":

        print("TELEGRAM NOT CONFIGURED")
        print(text)
        return


    url = (
        "https://api.telegram.org/bot"
        + BOT_TOKEN
        + "/sendMessage"
    )


    data = urllib.parse.urlencode({

        "chat_id": CHAT_ID,

        "text": text

    }).encode()


    urllib.request.urlopen(
        url,
        data=data
    )



def format_message(event):


    if event["event"] == "TP1_HIT":

        return f"""
🎯 TP1 HIT

Trade ID:
{event['trade_id']}

{event['symbol']}

Status:
PROFIT SECURED

SL:
MOVED TO BREAK EVEN
"""


    if event["event"] == "TP2_HIT":

        return f"""
🎯 TP2 HIT

Trade ID:
{event['trade_id']}

{event['symbol']}

Status:
PROFIT SECURED
"""


    if event["event"] == "TP3_HIT":

        return f"""
🎯 TP3 HIT

Trade ID:
{event['trade_id']}

{event['symbol']}

Status:
PROFIT SECURED
"""


    return None



def run():

    print("==============================")
    print("GSIS TELEGRAM ALERT ENGINE v1.0")
    print("==============================")


    events = load_json(EVENT_FILE)

    sent = load_json(SENT_FILE)


    sent_ids = [
        x["timestamp"]
        for x in sent
    ]


    for event in events:


        if event["timestamp"] not in sent_ids:


            message = format_message(event)


            if message:

                send_message(message)


                sent.append(event)

                print("ALERT SENT")
                print(message)



    save_json(
        SENT_FILE,
        sent
    )



if __name__ == "__main__":

    run()
