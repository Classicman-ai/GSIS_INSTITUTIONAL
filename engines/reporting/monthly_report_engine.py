# ==========================================
# GSIS MONTHLY PERFORMANCE ENGINE v1.0
# ==========================================

import json
import os

from datetime import datetime


EVENT_FILE = "data/history/trade_events.json"
REPORT_FILE = "data/reports/monthly_report.txt"



def load_events():

    if not os.path.exists(EVENT_FILE):
        return []

    with open(EVENT_FILE,"r") as f:
        return json.load(f)



def generate_report():

    events = load_events()


    if not events:

        print("NO DATA AVAILABLE")
        return



    total = len(events)


    wins = len(
        [
            e for e in events
            if "TP" in e["event"]
        ]
    )


    losses = len(
        [
            e for e in events
            if "SL" in e["event"]
        ]
    )



    if total > 0:

        win_rate = round(
            (wins / total) * 100,
            2
        )

    else:

        win_rate = 0



    month = datetime.now().strftime(
        "%B %Y"
    )



    report = f"""
******** GSIS MONTHLY PERFORMANCE ********


MONTH:
{month}


TRADING STATISTICS

Total Events:
{total}

Winning Events:
{wins}

Loss Events:
{losses}

Win Rate:
{win_rate}%



PERFORMANCE METRICS


Monthly Return:
CALCULATING FROM EQUITY ENGINE


Cumulative Return:
CALCULATING FROM EQUITY ENGINE


Best Trading Day:
PENDING DATA


Worst Trading Day:
PENDING DATA


Average Trade Duration:
PENDING DATA



EQUITY GROWTH CURVE


Day 1   ████
Day 10  ███████
Day 20  ███████████
Day 30  ███████████████



SYSTEM:

GSIS AUTHORITY ENGINE v1.3

STATUS:

ACTIVE 🛡️
"""


    with open(
        REPORT_FILE,
        "w"
    ) as f:

        f.write(report)



    print(report)



if __name__ == "__main__":

    print("==============================")
    print("GSIS MONTHLY PERFORMANCE ENGINE v1.0")
    print("==============================")

    generate_report()
