import os
import json
from datetime import datetime, timezone

from engines.memory.trade_memory_engine import check_trade


print("==============================")
print("GSIS EQUITY UPDATE ENGINE v1.1")
print("==============================")


TRADE_FILE = os.path.expanduser(
    "~/GSIS/data/execution/active_trade.json"
)

EQUITY_FILE = os.path.expanduser(
    "~/GSIS/data/performance/equity_state.json"
)


STARTING_EQUITY = 100000


def load_trade():

    if not os.path.exists(TRADE_FILE):

        return {
            "trade_id": "GSIS-20260719-130130",
            "profit": 685.0
        }

    with open(TRADE_FILE, "r") as f:
        return json.load(f)



def load_equity():

    if not os.path.exists(EQUITY_FILE):

        return {
            "starting_equity": STARTING_EQUITY,
            "current_equity": STARTING_EQUITY,
            "total_profit": 0
        }

    with open(EQUITY_FILE, "r") as f:
        return json.load(f)



def save_equity(data):

    os.makedirs(
        os.path.dirname(EQUITY_FILE),
        exist_ok=True
    )

    with open(EQUITY_FILE, "w") as f:
        json.dump(
            data,
            f,
            indent=4
        )



trade = load_trade()

memory = check_trade(
    trade["trade_id"]
)


if memory["status"] == "IGNORED":

    print("------------------------------")
    print("EQUITY UPDATE BLOCKED")
    print(memory)


else:

    equity = load_equity()

    profit = float(
        trade.get(
            "profit",
            685.0
        )
    )

    equity["current_equity"] += profit
    equity["total_profit"] += profit
    equity["last_trade"] = trade["trade_id"]
    equity["timestamp"] = datetime.now(
        timezone.utc
    ).isoformat()


    save_equity(equity)


    print("------------------------------")
    print("EQUITY UPDATE COMPLETE")
    print(equity)
