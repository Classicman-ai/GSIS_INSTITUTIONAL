# ==========================================
# GSIS EQUITY CURVE ENGINE v1.0
# ==========================================

import json
import os

from datetime import datetime, timezone


EQUITY_FILE = "data/performance/equity_curve.json"


STARTING_EQUITY = 100000



def load_curve():

    if not os.path.exists(EQUITY_FILE):

        return []

    with open(EQUITY_FILE,"r") as f:

        return json.load(f)



def save_curve(curve):

    with open(EQUITY_FILE,"w") as f:

        json.dump(
            curve,
            f,
            indent=4
        )



def calculate():

    curve = load_curve()


    if len(curve) == 0:

        first = {

            "date":
            datetime.now(timezone.utc).isoformat(),

            "equity":
            STARTING_EQUITY,

            "return_percent":
            0,

            "cumulative_return":
            0

        }


        curve.append(first)

        save_curve(curve)


        print("INITIAL EQUITY CREATED")

        print(first)

        return



    current = curve[-1]["equity"]


    new_record = {

        "date":
        datetime.now(timezone.utc).isoformat(),

        "equity":
        current,

        "return_percent":
        0,

        "cumulative_return":
        round(
            ((current - STARTING_EQUITY)
            /
            STARTING_EQUITY)
            *100,
            2
        )

    }


    curve.append(new_record)

    save_curve(curve)


    print("EQUITY UPDATED")

    print(new_record)



def run():

    print("==============================")
    print("GSIS EQUITY CURVE ENGINE v1.0")
    print("==============================")


    calculate()



if __name__ == "__main__":

    run()
