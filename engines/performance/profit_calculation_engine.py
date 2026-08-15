import os
import json
from datetime import datetime, timezone


print("==============================")
print("GSIS PROFIT CALCULATION ENGINE v1.2")
print("==============================")


BASE = os.path.expanduser("~/GSIS/data")

TRADE_FILE = os.path.join(
    BASE,
    "performance",
    "trade_results.json"
)

MEMORY_FILE = os.path.join(
    BASE,
    "system",
    "trade_memory.json"
)



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



memory = load_json(
    MEMORY_FILE,
    []
)


if isinstance(memory, dict):

    processed = memory.get(
        "processed_trades",
        []
    )

else:

    processed = memory



trade = {

    "trade_id": "GSIS-20260719-130130",
    "symbol": "BTCUSDT",
    "direction": "BUY",
    "entry": 63990,
    "exit": 64250,
    "r_multiple": 1.37,
    "profit": 685.0,
    "timestamp":
    datetime.now(
        timezone.utc
    ).isoformat()

}



trade_id = trade["trade_id"]



# Duplicate protection

if trade_id in processed:

    print("------------------------------")
    print(
        {
            "status": "IGNORED",
            "reason": "TRADE_ALREADY_PROCESSED",
            "trade_id": trade_id,
            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()
        }
    )

    exit()



# Save new trade

results = load_json(
    TRADE_FILE,
    []
)


if not isinstance(results, list):

    results = []



results.append(
    trade
)


save_json(
    TRADE_FILE,
    results
)



processed.append(
    trade_id
)


save_json(
    MEMORY_FILE,
    {
        "processed_trades": processed,
        "last_update":
        datetime.now(
            timezone.utc
        ).isoformat()
    }
)



print("------------------------------")
print(
    {
        "status": "NEW",
        "reason": "PROFIT_RECORDED",
        "trade_id": trade_id,
        "profit": trade["profit"],
        "timestamp":
        datetime.now(
            timezone.utc
        ).isoformat()
    }
)
