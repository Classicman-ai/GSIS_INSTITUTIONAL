import os
import json
from datetime import datetime, timezone


print("==============================")
print("GSIS REPORT INTEGRATION ENGINE v1.4")
print("==============================")


ANALYTICS_FILE = os.path.expanduser(
    "~/GSIS/data/performance/analytics_report.json"
)

PERFORMANCE_FILE = os.path.expanduser(
    "~/GSIS/data/performance/performance_metrics.json"
)


def load_json(path):

    if not os.path.exists(path):
        return {}

    try:
        with open(path, "r") as f:
            return json.load(f)

    except Exception:
        return {}



# ONLY TRUST ANALYTICS ENGINE

analytics = load_json(
    ANALYTICS_FILE
)


# fallback only if analytics file missing

if not analytics:

    analytics = load_json(
        PERFORMANCE_FILE
    )



current_equity = analytics.get(
    "current_equity",
    100000
)


total_profit = analytics.get(
    "total_profit",
    0
)


total_trades = analytics.get(
    "total_trades",
    0
)


winning = analytics.get(
    "winning_trades",
    0
)


losing = analytics.get(
    "losing_trades",
    0
)


win_rate = analytics.get(
    "win_rate",
    0
)



report = {

    "generated":
    datetime.now(
        timezone.utc
    ).isoformat(),

    "account": {

        "starting_equity": 100000,

        "current_equity":
        current_equity

    },


    "performance": {

        "total_profit":
        total_profit,

        "win_rate":
        win_rate

    },


    "statistics": {

        "total_trades":
        total_trades,

        "winning_trades":
        winning,

        "losing_trades":
        losing

    },


    "engine_status":
    "PROTECTED",

    "source":
    "GSIS_ANALYTICS_ENGINE_v1.3"

}



print("******** GSIS PERFORMANCE REPORT ********")
print()

print("ACCOUNT")
print()

print(
    "Starting Equity:",
    "$100000"
)

print()

print(
    "Current Equity:",
    current_equity
)

print()

print("PERFORMANCE")
print()

print(
    "Total Profit:",
    "+" + str(total_profit)
)

print(
    "Win Rate:",
    str(win_rate) + "%"
)

print()

print("TRADING STATISTICS")
print()

print(
    "Total Trades:",
    total_trades
)

print(
    "Winning Trades:",
    winning
)

print(
    "Losing Trades:",
    losing
)

print()

print("EQUITY STATUS")
print()

print(
    "GSIS EQUITY ENGINE ACTIVE 🛡️"
)

print()

print(
    "Generated:"
)

print(
    report["generated"]
)

print("------------------------------")

print(report)
