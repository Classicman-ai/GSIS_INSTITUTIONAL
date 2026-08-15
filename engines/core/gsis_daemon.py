import time
import datetime
import traceback
import subprocess
import os


VERSION = "GSIS ONLINE CORE DAEMON v1.0"

CYCLE_INTERVAL = 60  # seconds


def banner():
    print("=" * 30)
    print(VERSION)
    print("=" * 30)


def timestamp():
    return datetime.datetime.now(
        datetime.timezone.utc
    ).isoformat()


def run_master_cycle():

    print("\n------------------------------")
    print("STARTING GSIS MASTER CYCLE")
    print(timestamp())
    print("------------------------------")

    try:

        result = subprocess.run(
            [
                "python",
                "-m",
                "engines.master.gsis_master"
            ],
            capture_output=True,
            text=True
        )

        print(result.stdout)

        if result.stderr:
            print("WARNINGS:")
            print(result.stderr)

        print("------------------------------")
        print("MASTER CYCLE COMPLETE")
        print("------------------------------")


    except Exception:

        print("MASTER CYCLE ERROR")
        traceback.print_exc()



def main():

    banner()

    print("GSIS ONLINE STATUS: ACTIVE 🟢")
    print(
        "Cycle Interval:",
        CYCLE_INTERVAL,
        "seconds"
    )


    while True:

        run_master_cycle()

        print(
            "NEXT CYCLE:",
            CYCLE_INTERVAL,
            "seconds"
        )

        time.sleep(CYCLE_INTERVAL)



if __name__ == "__main__":
    main()
