import datetime


class FailsafeRecoveryEngine:

    def __init__(self):

        print("==============================")
        print("GSIS FAILSAFE RECOVERY ENGINE v1.0 ONLINE")
        print("SYSTEM PROTECTION AND RECOVERY ACTIVE")
        print("==============================")


    def check(
        self,
        modules_status,
        execution_status,
        broker_status
    ):

        score = 100
        reasons = []


        if modules_status == "HEALTHY":

            reasons.append(
                "MODULE HEALTH VERIFIED"
            )

        else:

            score -= 40

            reasons.append(
                "MODULE FAILURE DETECTED"
            )



        if execution_status == "AUTHORIZED":

            reasons.append(
                "EXECUTION CONTROL HEALTHY"
            )

        else:

            score -= 30

            reasons.append(
                "EXECUTION ISSUE DETECTED"
            )



        if broker_status == "READY":

            reasons.append(
                "BROKER CONNECTION HEALTHY"
            )

        else:

            score -= 30

            reasons.append(
                "BROKER ISSUE DETECTED"
            )



        if score >= 80:

            system_status = "SYSTEM HEALTHY"
            action = "CONTINUE PIPELINE"

        elif score >= 50:

            system_status = "SYSTEM WARNING"
            action = "MONITOR AND REPAIR"

        else:

            system_status = "SYSTEM FAILURE"
            action = "STOP EXECUTION"



        result = {

            "status":
                system_status,

            "action":
                action,

            "health_score":
                score,

            "checks":
                reasons,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS FAILSAFE RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = FailsafeRecoveryEngine()


    engine.check(

        modules_status="HEALTHY",

        execution_status="AUTHORIZED",

        broker_status="READY"

    )
