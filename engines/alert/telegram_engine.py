"""GSIS Telegram event delivery.

Credentials and paths are runtime configuration; no market data or secrets are
stored in source code.
"""

import json
import os
from datetime import datetime, timezone

import requests


BOT_TOKEN = os.environ["GSIS_TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["GSIS_TELEGRAM_CHAT_ID"]
EVENT_FILE = os.environ["GSIS_TELEGRAM_EVENT_FILE"]
DELIVERY_FILE = os.environ["GSIS_TELEGRAM_DELIVERY_FILE"]
MEMORY_FILE = os.environ["GSIS_TELEGRAM_MEMORY_FILE"]


def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path, data):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.post(url, data={"chat_id": CHAT_ID, "text": message}, timeout=float(os.environ["GSIS_TELEGRAM_TIMEOUT_SECONDS"]))
    return response.json()


def event_key(trade_id, event):
    return f"{trade_id}_{event}"


def already_sent(trade_id, event):
    return event_key(trade_id, event) in load_json(MEMORY_FILE)


def save_memory(trade_id, event):
    memory = load_json(MEMORY_FILE)
    key = event_key(trade_id, event)
    if key not in memory:
        memory.append(key)
    save_json(MEMORY_FILE, memory)


def save_delivery(record):
    data = load_json(DELIVERY_FILE)
    if not isinstance(data, list):
        data = []
    data.append(record)
    save_json(DELIVERY_FILE, data)


def process_event(event):
    trade_id = event.get("trade_id")
    name = event.get("event")
    symbol = event.get("symbol")
    if not trade_id or not name or already_sent(trade_id, name):
        return

    message = (
        "GSIS TRADE UPDATE\n\n"
        f"Symbol: {symbol}\n"
        f"Trade ID: {trade_id}\n"
        f"Event: {name}\n\n"
        f"Time: {datetime.now(timezone.utc).isoformat()}"
    )
    result = send_telegram(message)
    if result.get("ok"):
        save_delivery({
            "trade_id": trade_id,
            "event": name,
            "telegram_status": "DELIVERED",
            "message_id": result["result"]["message_id"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        save_memory(trade_id, name)


def run():
    for event in load_json(EVENT_FILE):
        process_event(event)


if __name__ == "__main__":
    run()
