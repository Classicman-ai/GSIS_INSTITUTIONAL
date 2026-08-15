import os
import json
import time
from datetime import datetime, timezone


ENGINE = "GSIS_REPORT_BRIDGE_v2.0"

STATE_FILE = "data/live/REPORT_state.json"


ENGINES = {
    "HMM": "data/live/HMM_state.json",
    "ORDERFLOW": "data/live/ORDERFLOW_state.json",
    "STRUCTURE": "data/live/STRUCTURE_state.json",
    "FUSION": "data/live/FUSION_state.json",
    "DECISION": "data/live/DECISION_state.json",
    "CONFIRMATION": "data/live/CONFIRMATION_state.json",
    "QUALIFICATION": "data/live/QUALIFICATION_state.json",
    "RISK": "data/live/RISK_state.json",
    "EXECUTION": "data/live/EXECUTION_state.json"
}



def utc_now():

    return datetime.now(
        timezone.utc
    ).isoformat()



def load_state(path):

    try:

        with open(path, "r") as file:
            return json.load(file)

    except Exception:

        return {
            "status": "OFFLINE"
        }



def collect_states():

    report = {}

    for name, path in ENGINES.items():

        report[name] = load_state(path)


    return report



def generate_report():

    data = collect_states()


    report = {

        "symbol": "BTCUSDT",

        "market_regime":
            data.get("HMM", {})
            .get("state", {})
            .get("current_regime", "UNKNOWN"),


        "institutional_bias":
            data.get("FUSION", {})
            .get("state", {})
            .get("bias", "UNKNOWN"),


        "institutional_score":
            data.get("FUSION", {})
            .get("state", {})
            .get("institutional_score", 0),


        "decision":
            data.get("DECISION", {})
            .get("state", {})
            .get("decision", "WAIT"),


        "qualification":
            data.get("QUALIFICATION", {})
            .get("state", {})
            .get("qualification", "NO_TRADE"),


        "risk_status":
            data.get("RISK", {})
            .get("state", {})
            .get("risk_status", "BLOCKED"),


        "execution_status":
            data.get("EXECUTION", {})
            .get("state", {})
            .get("execution_status", "BLOCKED"),


        "execution_instruction":
            data.get("EXECUTION", {})
            .get("state", {})
            .get("order_instruction", "NO_ORDER"),


        "next_action": "WAIT_FOR_CONFIRMATION"

    }


    if (
        report["risk_status"] == "APPROVED"
        and report["execution_status"] == "READY"
    ):

        report["next_action"] = "EXECUTE_TRADE"


    return report



def save_state():

    os.makedirs(
        "data/live",
        exist_ok=True
    )


    payload = {

        "engine": ENGINE,

        "status": "ACTIVE",

        "heartbeat": time.time(),

        "timestamp": utc_now(),

        "state": generate_report()

    }


    with open(
        STATE_FILE,
        "w"
    ) as file:

        json.dump(
            payload,
            file,
            indent=4
        )


    return payload



def run():

    print("==============================")
    print("GSIS REPORT BRIDGE v2.0")
    print("==============================")


    while True:

        state = save_state()

        print("------------------------------")
        print("GSIS INSTITUTIONAL REPORT")

        print(state)


        time.sleep(30)



if __name__ == "__main__":

    run()
