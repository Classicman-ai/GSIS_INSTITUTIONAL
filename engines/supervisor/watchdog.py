"""
=========================================
GSIS WATCHDOG ENGINE
Version : 2.0
=========================================
"""

from engines.supervisor.health_monitor import run_health_monitor


def generate_actions(state):

    actions = []


    for engine, info in state["engines"].items():

        status = info["status"]


        if status == "OFFLINE":

            actions.append(
                f"{engine}: restart required"
            )


        elif status == "STALE":

            actions.append(
                f"{engine}: heartbeat delayed"
            )


        elif status == "ERROR":

            actions.append(
                f"{engine}: repair state file"
            )


        elif status == "SLEEPING":

            actions.append(
                f"{engine}: monitor activity"
            )


    if not actions:

        actions.append(
            "All systems operating normally"
        )


    return actions



def run_watchdog():


    health = run_health_monitor()


    actions = generate_actions(
        health
    )


    return {

        "engine":
        "GSIS_WATCHDOG_v2.0",

        "system_status":
        health["system_status"],

        "health":
        health["system_health"],

        "actions":
        actions

    }



if __name__ == "__main__":


    print("==============================")
    print("GSIS WATCHDOG v2.0")
    print("==============================")


    state = run_watchdog()


    print("------------------------------")
    print("GSIS WATCHDOG STATE")
    print(state)
