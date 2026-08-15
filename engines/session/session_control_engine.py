# ==========================================
# GSIS SESSION CONTROL ENGINE v1.0
# ==========================================

import json
import os
import uuid

from datetime import datetime, timezone


SESSION_FILE = "data/session/current_session.json"


def create_session():

    session_id = (
        "GSIS-SESSION-"
        + datetime.now(timezone.utc)
        .strftime("%Y%m%d-%H%M%S")
        + "-"
        + str(uuid.uuid4())[:8]
    )


    session = {

        "engine":
        "GSIS_SESSION_CONTROL_ENGINE_v1.0",

        "session_id":
        session_id,

        "status":
        "ACTIVE",

        "created":
        datetime.now(timezone.utc)
        .isoformat(),

        "trade_lock":
        "ENABLED"

    }


    with open(SESSION_FILE,"w") as f:

        json.dump(
            session,
            f,
            indent=4
        )


    return session



def load_session():

    if not os.path.exists(SESSION_FILE):

        return create_session()


    with open(SESSION_FILE,"r") as f:

        return json.load(f)



def validate_trade(trade_session):

    session = load_session()


    if trade_session != session["session_id"]:

        return {

            "allowed": False,

            "reason":
            "OLD_SESSION_BLOCKED"

        }


    return {

        "allowed": True,

        "reason":
        "CURRENT_SESSION"

    }



def run():

    print("==============================")
    print("GSIS SESSION CONTROL ENGINE v1.0")
    print("==============================")


    session = create_session()


    print(session)



if __name__ == "__main__":

    run()
