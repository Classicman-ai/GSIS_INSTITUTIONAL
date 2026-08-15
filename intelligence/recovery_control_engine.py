import datetime


class RecoveryControlEngine:

    def __init__(self):

        print("==============================")
        print("GSIS RECOVERY CONTROL ENGINE v1.0 ONLINE")
        print("AUTONOMOUS FAILURE RECOVERY ACTIVE")
        print("==============================")


    def monitor(
        self,
        module_status
    ):

        failed_modules = []

        for module, status in module_status.items():

            if status != "ONLINE":

                failed_modules.append(module)


        if len(failed_modules) == 0:

            system_state = "ALL SYSTEMS HEALTHY"

            action = "NO RECOVERY REQUIRED"


        else:

            system_state = "DEGRADED SYSTEM"

            action = "RECOVERY MODE ACTIVATED"



        result = {

            "status":
                "RECOVERY CHECK COMPLETE",

            "system_state":
                system_state,

            "failed_modules":
                failed_modules,

            "action":
                action,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS RECOVERY RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = RecoveryControlEngine()


    engine.monitor({

        "INTELLIGENCE":
            "ONLINE",

        "RISK":
            "ONLINE",

        "EXECUTION":
            "ONLINE",

        "BROKER":
            "ONLINE"

    })
