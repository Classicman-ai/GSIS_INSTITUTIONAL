import os
import json
import time
from datetime import datetime, timezone


ENGINE = "GSIS_REPORT_ENGINE_v3.0"

OUTPUT = "data/live/REPORT_state.json"


def now():
    return datetime.now(timezone.utc).isoformat()



def load(path):

    try:
        with open(path, "r") as f:
            return json.load(f)

    except:
        return {}



def save(path, data):

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



def generate_report():


    signal = load(
        "data/live/master_signal.json"
    )

    probability = load(
        "data/live/bayesian_state.json"
    )

    qualification = load(
        "data/live/QUALIFICATION_state.json"
    )

    risk = load(
        "data/live/RISK_state.json"
    )

    execution = load(
        "data/live/EXECUTION_state.json"
    )

    regime = load(
        "data/live/regime_score.json"
    )

    confirmation = load(
        "data/live/CONFIRMATION_state.json"
    )



    signal_state = signal.get(
        "state",
        {}
    )

    probability_state = probability.get(
        "state",
        {}
    )

    qualification_state = qualification.get(
        "state",
        {}
    )

    risk_state = risk.get(
        "state",
        {}
    )

    execution_state = execution.get(
        "state",
        {}
    )

    regime_state = regime.get(
        "state",
        {}
    )

    confirmation_state = confirmation.get(
        "state",
        {}
    )



    decision = "WAIT"


    if execution_state.get(
        "execution_status"
    ) == "READY":

        decision = "EXECUTE"



    return {


        "symbol":"BTCUSDT",

        "market_regime":
            probability_state.get(
                "market",
                {}
            ).get(
                "regime",
                regime_state.get(
                    "bias",
                    "UNKNOWN"
                )
            ),


        "regime_score":
            regime_state.get(
                "score",
                0
            ),


        "signal":
            signal_state.get(
                "signal",
                "WAIT"
            ),


        "direction":
            signal_state.get(
                "direction",
                "NONE"
            ),


        "probability":
            probability_state.get(
                "adjusted_confidence",
                0
            ),


        "qualification":
            qualification_state.get(
                "qualification",
                "NO_TRADE"
            ),


        "qualification_score":
            qualification_state.get(
                "qualification_score",
                0
            ),


        "confirmation":
            confirmation_state.get(
                "confirmed",
                False
            ),


        "confirmation_score":
            confirmation_state.get(
                "confirmation_score",
                0
            ),


        "risk_status":
            risk_state.get(
                "risk_status",
                "BLOCKED"
            ),


        "execution_status":
            execution_state.get(
                "execution_status",
                "BLOCKED"
            ),


        "final_decision":
            decision,


        "reason":

            "WAITING_FOR_CONFIRMATION"
            if decision == "WAIT"
            else
            "EXECUTION_APPROVED"

    }



def run():

    print("==============================")
    print("GSIS REPORT ENGINE v3.0")
    print("==============================")


    while True:


        report = generate_report()


        state = {


            "engine":ENGINE,

            "status":"ACTIVE",

            "heartbeat":time.time(),

            "timestamp":now(),

            "state":report

        }


        save(
            OUTPUT,
            state
        )


        print("------------------------------")
        print("GSIS INSTITUTIONAL REPORT")
        print(state)


        time.sleep(30)



if __name__=="__main__":
    run()
