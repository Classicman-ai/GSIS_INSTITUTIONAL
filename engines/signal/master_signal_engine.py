import os
import json
import time
from datetime import datetime, timezone


ENGINE="GSIS_MASTER_SIGNAL_ENGINE_v3.0"

OUTPUT="data/live/master_signal.json"



def now():

    return datetime.now(
        timezone.utc
    ).isoformat()



def load(path):

    try:
        with open(path,"r") as f:
            return json.load(f)

    except:

        return {}



def save(path,data):

    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    with open(path,"w") as f:
        json.dump(
            data,
            f,
            indent=4
        )



def generate_signal():


    regime = load(
        "data/live/regime_score.json"
    )


    risk = load(
        "data/live/RISK_state.json"
    )


    confirmation = load(
        "data/live/CONFIRMATION_state.json"
    )



    regime_state = regime.get(
        "state",
        {}
    )


    score = regime_state.get(
        "score",
        0
    )


    bias = regime_state.get(
        "bias",
        "NEUTRAL"
    )



    risk_state = risk.get(
        "state",
        {}
    )


    risk_status = risk_state.get(
        "risk_status",
        "BLOCKED"
    )



    confirmation_state = confirmation.get(
        "state",
        {}
    )


    confirmed = confirmation_state.get(
        "confirmed",
        False
    )



    signal="WAIT"
    direction="NONE"



    reasons=[]



    if score >= 50:

        signal="SELL"
        direction="SHORT"

        reasons.append(
            "BEARISH_REGIME_SCORE"
        )


    elif score <= -50:

        signal="BUY"
        direction="LONG"

        reasons.append(
            "BULLISH_REGIME_SCORE"
        )


    else:

        reasons.append(
            "WEAK_REGIME_SCORE"
        )



    if not confirmed:

        reasons.append(
            "NO_CONFIRMATION"
        )

        signal="WAIT"
        direction="NONE"



    if risk_status != "APPROVED":

        reasons.append(
            "RISK_BLOCKED"
        )

        signal="WAIT"
        direction="NONE"



    confidence=min(
        abs(score)+20,
        95
    )



    return {

        "symbol":"BTCUSDT",

        "signal":signal,

        "direction":direction,

        "confidence":confidence,

        "institutional_score":score,

        "bias":bias,

        "risk_status":risk_status,

        "confirmation":confirmed,

        "reasons":reasons

    }



def run():

    print("==============================")
    print("GSIS MASTER SIGNAL ENGINE v3.0")
    print("==============================")


    while True:


        result=generate_signal()


        state={

            "engine":ENGINE,

            "status":"ACTIVE",

            "heartbeat":time.time(),

            "timestamp":now(),

            "state":result

        }


        save(
            OUTPUT,
            state
        )


        print("------------------------------")
        print("GSIS MASTER SIGNAL")
        print(state)


        time.sleep(30)



if __name__=="__main__":

    run()
