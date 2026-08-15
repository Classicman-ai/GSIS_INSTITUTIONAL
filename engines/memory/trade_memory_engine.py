import os
import json
from datetime import datetime, timezone


MEMORY_FILE = os.path.expanduser(
    "~/GSIS/data/system/trade_memory.json"
)


def load_memory():

    os.makedirs(
        os.path.dirname(MEMORY_FILE),
        exist_ok=True
    )

    if not os.path.exists(MEMORY_FILE):

        return {
            "processed_trades": []
        }

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)



def save_memory(memory):

    with open(MEMORY_FILE, "w") as f:
        json.dump(
            memory,
            f,
            indent=4
        )



def check_trade(trade_id):

    memory = load_memory()

    if trade_id in memory["processed_trades"]:

        return {
            "status": "IGNORED",
            "reason": "TRADE_ALREADY_PROCESSED",
            "trade_id": trade_id,
            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()
        }


    memory["processed_trades"].append(
        trade_id
    )

    save_memory(memory)

    return {
        "status": "NEW",
        "reason": "TRADE_ACCEPTED",
        "trade_id": trade_id,
        "timestamp":
        datetime.now(
            timezone.utc
        ).isoformat()
    }



if __name__ == "__main__":

    print("==============================")
    print("GSIS TRADE MEMORY ENGINE v1.0")
    print("==============================")

    test_trade = "GSIS-20260719-130130"

    result = check_trade(test_trade)

    print(result)
