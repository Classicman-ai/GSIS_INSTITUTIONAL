import datetime


class SystemHealthMonitorEngine:

    def __init__(self):

        print("==============================")
        print("GSIS SYSTEM HEALTH MONITOR ENGINE v1.0 ONLINE")
        print("INSTITUTIONAL SYSTEM MONITORING ACTIVE")
        print("==============================")


    def check(
        self,
        engines_loaded,
        market_feed,
        memory_system,
        execution_system
    ):

        score = 100
        checks = []


        if engines_loaded:

            checks.append(
                "ALL ENGINES LOADED"
            )

        else:

            score -= 30

            checks.append(
                "ENGINE LOADING FAILURE"
            )



        if market_feed:

            checks.append(
                "MARKET DATA ACTIVE"
            )

        else:

            score -= 25

            checks.append(
                "MARKET DATA FAILURE"
            )



        if memory_system:

            checks.append(
                "MEMORY SYSTEM ACTIVE"
            )

        else:

            score -= 20

            checks.append(
                "MEMORY SYSTEM FAILURE"
            )



        if execution_system:

            checks.append(
                "EXECUTION SYSTEM READY"
            )

        else:

            score -= 25

            checks.append(
                "EXECUTION SYSTEM FAILURE"
            )



        if score >= 90:

            status = "SYSTEM READY"

        elif score >= 60:

            status = "SYSTEM WARNING"

        else:

            status = "SYSTEM OFFLINE"



        result = {

            "status":
                status,

            "health_score":
                score,

            "checks":
                checks,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS HEALTH RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = SystemHealthMonitorEngine()


    engine.check(

        engines_loaded=True,

        market_feed=True,

        memory_system=True,

        execution_system=True

    )
