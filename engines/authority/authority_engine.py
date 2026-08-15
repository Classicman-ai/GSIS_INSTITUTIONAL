# ==========================================
# GSIS TRADE AUTHORITY ENGINE v1.3
# LIVE AUTHORITY READER
# ==========================================

import json
import os

from datetime import datetime, timezone

from engines.authority.trade_id import generate_trade_id


AUTHORITY_FILE = "data/authority/authority_state.json"



def load_authority_state():

    if not os.path.exists(AUTHORITY_FILE):

        return None


    with open(AUTHORITY_FILE,"r") as f:

        return json.load(f)



def evaluate_trade(state):


    if state is None:

        return {
            "decision":"NONE",
            "status":"BLOCKED",
            "reason":"NO_AUTHORITY_STATE"
        }



    confidence = state.get(
        "confidence",
        0
    )


    setup = state.get(
        "setup",
        "NONE"
    )


    timeframe = state.get(
        "timeframe",
        None
    )


    confirmation = state.get(
        "confirmation",
        False
    )


    risk = state.get(
        "risk_status",
        "UNKNOWN"
    )


    direction = state.get(
        "direction",
        "NONE"
    )



    if (

        confidence >= 88

        and setup == "A+"

        and timeframe == "M15"

        and confirmation is True

        and risk == "APPROVED"

        and direction != "NONE"

    ):


        return {

            "decision":
            direction,


            "status":
            "APPROVED",


            "reason":
            "ALL_AUTHORITY_RULES_PASSED"

        }



    return {

        "decision":
        "NONE",


        "status":
        "BLOCKED",


        "reason":
        "AUTHORITY_CONDITIONS_FAILED"

    }



def run():


    print("==============================")

    print("GSIS TRADE AUTHORITY ENGINE v1.3")

    print("==============================")


    state = load_authority_state()


    decision = evaluate_trade(state)


    output = {


        "trade_id":
        generate_trade_id()
        if decision["status"]=="APPROVED"
        else None,


        "symbol":
        state.get("symbol")
        if state else None,


        "direction":
        state.get("direction")
        if state else None,


        "decision":
        decision["decision"],


        "status":
        decision["status"],


        "confidence":
        state.get("confidence")
        if state else 0,


        "setup":
        state.get("setup")
        if state else "NONE",


        "timeframe":
        state.get("timeframe")
        if state else None,


        "reason":
        decision["reason"],


        "authority":
        "GSIS_AUTHORITY_v1.3",


        "timestamp":
        datetime.now(timezone.utc)
        .isoformat()

    }



    print(output)



if __name__ == "__main__":

    run()
