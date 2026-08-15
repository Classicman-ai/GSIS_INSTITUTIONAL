import os
import json
import socket
from datetime import datetime, timezone


print("==============================")
print("GSIS WATCHDOG ENGINE v1.0")
print("==============================")


BASE = os.path.expanduser("~/GSIS")

HEARTBEAT_FILE = os.path.join(
    BASE,
    "data/system/heartbeat.json"
)


def internet_check():
    try:
        socket.create_connection(
            ("8.8.8.8", 53),
            timeout=3
        )
        return "CONNECTED"

    except:
        return "DISCONNECTED"


def check_engine(path):
    if os.path.exists(path):
        return "ACTIVE"
    else:
        return "MISSING"


engines = {

    "master_daemon":
    "engines/core/gsis_daemon.py",

    "market_engine":
    "engines/market/live_price_connector.py",

    "bayesian_engine":
    "engines/adapters/bayesian_adapter.py",

    "risk_engine":
    "engines/risk/risk_guard_engine.py",

    "execution_engine":
    "engines/execution/execution_gate.py",

    "position_engine":
    "engines/management/position_manager.py"

}


engine_status = {}


for name, file in engines.items():

    engine_status[name] = check_engine(
        os.path.join(BASE,file)
    )


online_status = {

    "system":
    "ONLINE",

    "daemon":
    "ACTIVE",

    "internet":
    internet_check(),

    "engines":
    engine_status,

    "last_heartbeat":
    datetime.now(timezone.utc).isoformat()

}


os.makedirs(
    os.path.dirname(HEARTBEAT_FILE),
    exist_ok=True
)


with open(
    HEARTBEAT_FILE,
    "w"
) as f:

    json.dump(
        online_status,
        f,
        indent=4
    )


print("------------------------------")
print("GSIS SYSTEM HEARTBEAT")
print(online_status)
print("------------------------------")
print("WATCHDOG STATUS: ACTIVE 🛡️")
