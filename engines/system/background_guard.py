import os
import json
import time
import subprocess
from datetime import datetime, timezone

BASE = os.path.expanduser("~/GSIS")

HEARTBEAT_FILE = os.path.join(
    BASE,
    "data/system/heartbeat.json"
)

STATUS_FILE = os.path.join(
    BASE,
    "data/system/background_guard.json"
)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def internet_check():
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "8.8.8.8"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return result.returncode == 0

    except:
        return False


def acquire_wake_lock():
    try:
        subprocess.run(
            ["termux-wake-lock"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return True

    except:
        return False


def release_wake_lock():
    try:
        subprocess.run(
            ["termux-wake-unlock"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    except:
        pass


def update_status():

    wake = acquire_wake_lock()

    status = {

        "system": "ONLINE",

        "background_guard":
            "ACTIVE",

        "wake_lock":
            "ENABLED" if wake else "UNAVAILABLE",

        "internet":
            "CONNECTED"
            if internet_check()
            else "DISCONNECTED",

        "heartbeat":
            utc_now()

    }


    os.makedirs(
        os.path.dirname(STATUS_FILE),
        exist_ok=True
    )


    with open(
        STATUS_FILE,
        "w"
    ) as f:
        json.dump(
            status,
            f,
            indent=4
        )


    print("==============================")
    print("GSIS BACKGROUND GUARD ENGINE v1.0")
    print("==============================")
    print(status)


if __name__ == "__main__":

    while True:

        update_status()

        time.sleep(60)
