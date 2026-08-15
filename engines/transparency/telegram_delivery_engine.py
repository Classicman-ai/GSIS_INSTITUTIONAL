# ==========================================
# GSIS TELEGRAM DELIVERY VERIFICATION ENGINE v1.0
# ==========================================

import json
import os

from datetime import datetime, timezone


DELIVERY_FILE = "data/transparency/telegram_delivery.json"



def load_delivery():

    if not os.path.exists(DELIVERY_FILE):
        return []

    with open(DELIVERY_FILE,"r") as f:
        return json.load(f)



def save_delivery(data):

    with open(DELIVERY_FILE,"w") as f:
        json.dump(
            data,
            f,
            indent=4
        )



def record_delivery(
        trade_id,
        event,
        status,
        message_id=None
):

    records = load_delivery()


    record = {

        "trade_id": trade_id,

        "event": event,

        "telegram_status": status,

        "message_id": message_id,

        "timestamp":
        datetime.now(timezone.utc)
        .isoformat()

    }


    records.append(record)

    save_delivery(records)


    return record



if __name__ == "__main__":

    print("==============================")
    print("GSIS TELEGRAM DELIVERY ENGINE")
    print("==============================")


    test = record_delivery(
        "GSIS-TEST-001",
        "TP4_HIT",
        "DELIVERED",
        999
    )


    print(test)
