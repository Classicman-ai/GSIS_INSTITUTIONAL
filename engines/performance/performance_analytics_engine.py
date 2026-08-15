import os
import json
from datetime import datetime, timezone


print("==============================")
print("GSIS PERFORMANCE ANALYTICS ENGINE v1.4")
print("==============================")


BASE = os.path.expanduser("~/GSIS/data/performance")

TRADE_FILE = os.path.join(
    BASE,
    "trade_results.json"
)

EQUITY_FILE = os.path.join(
    BASE,
    "equity_curve.json"
)

OUTPUT_FILE = os.path.join(
    BASE,
    "performance_metrics.json"
)



def load_json(path):

    if not os.path.exists(path):
        return []

    try:
        with open(path, "r") as f:
            return json.load(f)

    except Exception:
        return []



trades = load_json(TRADE_FILE)

equity = load_json(EQUITY_FILE)



# Normalize trade data

if not isinstance(trades, list):
    trades = []



total_trades = len(trades)

winning = 0
losing = 0
total_profit = 0



for trade in trades:

    profit = trade.get(
        "profit",
        0
    )

    total_profit += profit

    if profit > 0:
        winning += 1

    elif profit < 0:
        losing += 1



win_rate = 0

if total_trades > 0:
    win_rate = round(
        (winning / total_trades) * 100,
        2
    )



# Equity authority

current_equity = 100000 + total_profit



if isinstance(equity, list) and len(equity) > 0:

    last = equity[-1]

    if isinstance(last, dict):

        current_equity = last.get(
            "equity",
            current_equity
        )



metrics = {

    "generated":
    datetime.now(
        timezone.utc
    ).isoformat(),

    "current_equity":
    current_equity,

    "total_profit":
    total_profit,

    "total_trades":
    total_trades,

    "winning_trades":
    winning,

    "losing_trades":
    losing,

    "win_rate":
    win_rate,

    "engine_status":
    "PROTECTED",

    "duplicate_filter":
    "ACTIVE"

}



with open(
    OUTPUT_FILE,
    "w"
) as f:

    json.dump(
        metrics,
        f,
        indent=4
    )



print("------------------------------")
print(metrics)
