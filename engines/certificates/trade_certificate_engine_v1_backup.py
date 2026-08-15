# ==========================================
# GSIS TRADE CERTIFICATE ENGINE v1.0
# ==========================================

import json
import os

from datetime import datetime, timezone


TRADE_FILE = "data/execution/trade_state.json"
DELIVERY_FILE = "data/transparency/telegram_delivery.json"
CERTIFICATE_DIR = "data/certificates"


def load_json(path, default):

    if not os.path.exists(path):
        return default

    try:
        with open(path, "r") as f:
            return json.load(f)

    except Exception:
        return default



def save_json(path, data):

    with open(path, "w") as f:
        json.dump(
            data,
            f,
            indent=4
        )



def generate_certificate():

    trade = load_json(
        TRADE_FILE,
        {}
    )

    delivery = load_json(
        DELIVERY_FILE,
        []
    )


    if not trade:

        print("NO TRADE DATA FOUND")
        return



    trade_id = trade.get(
        "trade_id",
        "UNKNOWN"
    )


    confirmed_messages = []

    for item in delivery:

        if item.get("trade_id") == trade_id:

            confirmed_messages.append(item)



    certificate = {

        "certificate_engine":
        "GSIS_TRADE_CERTIFICATE_ENGINE_v1.0",


        "trade_id":
        trade_id,


        "symbol":
        trade.get("symbol"),


        "direction":
        trade.get("direction"),


        "trade_status":
        trade.get("status"),


        "targets":

        {
            "TP1":
            trade.get("tp1"),

            "TP2":
            trade.get("tp2"),

            "TP3":
            trade.get("tp3"),

            "TP4":
            trade.get("tp4")
        },


        "risk_control":

        {
            "stop_loss":
            trade.get("stop_loss"),

            "break_even":
            trade.get("break_even")
        },


        "telegram_delivery":

        {
            "messages_confirmed":
            len(confirmed_messages),

            "status":
            "VERIFIED"
            if len(confirmed_messages) > 0
            else "NOT_VERIFIED"
        },


        "final_verdict":

        "SUCCESSFUL"
        if trade.get("status") == "COMPLETED"
        else "IN_PROGRESS",


        "generated":

        datetime.now(timezone.utc)
        .isoformat()

    }


    os.makedirs(
        CERTIFICATE_DIR,
        exist_ok=True
    )


    file_path = (
        CERTIFICATE_DIR
        + "/"
        + trade_id
        + ".json"
    )


    save_json(
        file_path,
        certificate
    )


    print("==============================")
    print("GSIS TRADE CERTIFICATE ENGINE v1.0")
    print("==============================")

    print(certificate)



if __name__ == "__main__":

    generate_certificate()
