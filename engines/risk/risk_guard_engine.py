# ==========================================
# GSIS RISK GUARD ENGINE v1.1
# ==========================================

import json
import os
from datetime import datetime, timezone


EQUITY_FILE = "data/performance/equity_curve.json"
ACTIVE_FILE = "data/execution/active_trade.json"
RESULT_FILE = "data/performance/trade_results.json"

STATE_FILE = "data/risk/risk_guard_state.json"


MAX_RISK_PERCENT = 0.5
MAX_OPEN_TRADES = 1

MAX_DRAWDOWN_PERCENT = 5
MAX_DAILY_LOSS_PERCENT = 2

DAILY_PROFIT_LOCK_PERCENT = 5



def load_json(path):

    if not os.path.exists(path):
        return {}

    with open(path, "r") as f:
        return json.load(f)



def save_json(path, data):

    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    with open(path, "w") as f:
        json.dump(
            data,
            f,
            indent=4
        )



def main():

    print("==============================")
    print("GSIS RISK GUARD ENGINE v1.1")
    print("==============================")


    active_trade = load_json(
        ACTIVE_FILE
    )

    equity_data = load_json(
        EQUITY_FILE
    )

    trade_results = load_json(
        RESULT_FILE
    )


    current_equity = 100000

    if isinstance(equity_data, list) and len(equity_data):

        current_equity = equity_data[-1].get(
            "equity",
            100000
        )


    profit_percent = (
        (current_equity - 100000)
        /
        100000
    ) * 100


    drawdown_percent = (
        (100000 - current_equity)
        /
        100000
    ) * 100


    open_trades = 0

    if active_trade:

        open_trades = 1



    losing_trades = 0

    if isinstance(trade_results, list):

        for trade in trade_results:

            if trade.get("profit",0) < 0:

                losing_trades += 1



    risk_score = 100


    status = "APPROVED"
    permission = "TRADE_ALLOWED"
    reason = "ALL_RISK_PARAMETERS_ACCEPTED"



    if open_trades >= MAX_OPEN_TRADES:

        status = "BLOCKED"
        permission = "NO_TRADE"
        reason = "MAX_OPEN_TRADES_REACHED"

        risk_score -= 40



    elif drawdown_percent >= MAX_DRAWDOWN_PERCENT:

        status = "BLOCKED"
        permission = "NO_TRADE"
        reason = "MAX_DRAWDOWN_LIMIT"

        risk_score -= 50



    elif profit_percent >= DAILY_PROFIT_LOCK_PERCENT:

        status = "BLOCKED"
        permission = "NO_TRADE"
        reason = "DAILY_PROFIT_LOCK_ACTIVE"
