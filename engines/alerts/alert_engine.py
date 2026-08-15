import json
import time
import os
from datetime import datetime


BASE = "data/live"
LOG_DIR = "logs"


os.makedirs(LOG_DIR, exist_ok=True)



def load_json(filename):

    try:

        with open(
            os.path.join(BASE, filename),
            "r"
        ) as f:

            return json.load(f)

    except Exception:

        return {}



def create_alert():

    execution = load_json(
        "execution_state.json"
    )

    risk = load_json(
        "risk_state.json"
    )

    master = load_json(
        "master_signal.json"
    )


    symbol = execution.get(
        "symbol",
        "BTCUSDT"
    )


    execution_status = execution.get(
        "execution_status",
        "UNKNOWN"
    )


    order = execution.get(
        "order_instruction",
        "NO_ORDER"
    )


    direction = execution.get(
        "direction",
        "NONE"
    )


    risk_status = risk.get(
        "risk_status",
        "UNKNOWN"
    )


    regime = master.get(
        "regime",
        "UNKNOWN"
    )


    alert_type = "SYSTEM_UPDATE"


    if execution_status == "READY":

        alert_type = "TRADE_READY"


    elif execution_status == "BLOCKED":

        alert_type = "TRADE_BLOCKED"



    alert = {

        "engine":
        "GSIS_ALERT_ENGINE_v1.0",


        "symbol":
        symbol,


        "alert":
        alert_type,


        "direction":
        direction,


        "order":
        order,


        "execution_status":
        execution_status,


        "risk_status":
        risk_status,


        "regime":
        regime,


        "time":
        datetime.utcnow().isoformat(),


        "timestamp":
        time.time()

    }


    return alert



def run():

    print("==============================")
    print("GSIS ALERT ENGINE v1.0")
    print("==============================")


    while True:

        alert = create_alert()


        with open(
            f"{LOG_DIR}/gsis_alerts.json",
            "a"
        ) as f:

            f.write(
                json.dumps(alert)
                + "\n"
            )


        print("------------------------------")
        print("GSIS ALERT STATE")
        print(alert)


        time.sleep(15)



if __name__ == "__main__":

    run()
