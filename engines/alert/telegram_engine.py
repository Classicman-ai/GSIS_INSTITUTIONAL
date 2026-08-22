"""GSIS Telegram event delivery.

Credentials and paths are runtime configuration; no market data or secrets are
stored in source code.
"""

import json
import os
from datetime import datetime, timezone

import requests


def required(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing Telegram runtime configuration: {name}")
    return value


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
    token = required("GSIS_TELEGRAM_BOT_TOKEN")
    chat_id = required("GSIS_TELEGRAM_CHAT_ID")
    timeout = float(required("GSIS_TELEGRAM_TIMEOUT_SECONDS"))
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(url, data={"chat_id": chat_id, "text": message}, timeout=timeout)
    return response.json()


def event_key(trade_id, event):
    return f"{trade_id}_{event}"


def already_sent(trade_id, event, memory_file):
    return event_key(trade_id, event) in load_json(memory_file)


def save_memory(trade_id, event, memory_file):
    memory = load_json(memory_file)
    key = event_key(trade_id, event)
    if key not in memory:
        memory.append(key)
    save_json(memory_file, memory)


def save_delivery(record, delivery_file):
    data = load_json(delivery_file)
    if not isinstance(data, list):
        data = []
    data.append(record)
    save_json(delivery_file, data)


def process_event(event):
    event_file = required("GSIS_TELEGRAM_EVENT_FILE")
    delivery_file = required("GSIS_TELEGRAM_DELIVERY_FILE")
    memory_file = required("GSIS_TELEGRAM_MEMORY_FILE")
    trade_id = event.get("trade_id")
    name = event.get("event")
    symbol = event.get("symbol")
    if not trade_id or not name or already_sent(trade_id, name, memory_file):
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
        save_delivery(
            {
                "trade_id": trade_id,
                "event": name,
                "telegram_status": "DELIVERED",
                "message_id": result["result"]["message_id"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            delivery_file,
        )
        save_memory(trade_id, name, memory_file)


def run():
    event_file = required("GSIS_TELEGRAM_EVENT_FILE")
    for event in load_json(event_file):
        process_event(event)


if __name__ == "__main__":
    run()
