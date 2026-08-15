# ==========================================
# GSIS EXECUTION GATE ENGINE v1.2
# ==========================================

import json
import os
from datetime import datetime, timezone


PROTECTION_FILE = "data/protection/protection_state.json"
RISK_FILE = "data/risk/risk_guard_state.json"
AUTHORITY_FILE = "data/authority/authority_state.json"

ACTIVE_TRADE_FILE = "data/execution/active_trade.json"



def load_json(path):

    if not os.path.exists(path):
        return {}

    with open(path, "r") as f:
        return json.load(f)



def save_trade(data):

    os.makedirs(
        "data/execution",
        exist_ok=True
    )

    with open(
        ACTIVE_TRADE_FILE,
        "w"
    ) as f:
        json.dump(
            data,
            f,
            indent=4
        )



def main():

    print("==============================")
    print("GSIS EXECUTION GATE ENGINE v1.2")
    print("==============================")


    protection = load_json(
        PROTECTION_FILE
    )

    risk = load_json(
        RISK_FILE
    )

    authority = load_json(
        AUTHORITY_FILE
    )


    # Protection Lock

    if protection.get("new_entries") == "BLOCKED":

        result = {

            "status":
            "REJECTED",

            "reason":
            "TRADE_PROTECTION_ACTIVE",

            "active_trade":
            protection.get("active_trade"),

            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()
        }


        print("------------------------------")
        print("EXECUTION BLOCKED")
        print(result)

        return



    # Risk Guard Lock

    if risk.get("risk_status") == "BLOCKED":

        result = {

            "status":
            "REJECTED",

            "reason":
            risk.get(
                "reason"
            ),

            "risk_status":
            "BLOCKED",

            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()
        }


        print("------------------------------")
        print("EXECUTION BLOCKED BY RISK GUARD")
        print(result)

        return



    trade = {

        "trade_id":
        "GSIS-" +
        datetime.now(
            timezone.utc
        ).strftime(
            "%Y%m%d-%H%M%S"
        ),

        "symbol":
        authority.get(
            "symbol"
        ),

        "direction":
        authority.get(
            "direction"
        ),

        "confidence":
        authority.get(
            "confidence"
        ),

        "setup":
        authority.get(
            "setup"
        ),

        "timeframe":
        authority.get(
            "timeframe"
        ),

        "status":
        "ACTIVE",

        "opened_at":
        datetime.now(
            timezone.utc
        ).isoformat()
    }


    save_trade(
        trade
    )


    print("------------------------------")
    print("EXECUTION APPROVED")
    print(trade)



if __name__ == "__main__":

    main()
