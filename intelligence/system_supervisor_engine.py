import datetime
import os


class SystemSupervisorEngine:

    def __init__(self):

        print("==============================")
        print("GSIS SYSTEM SUPERVISOR ENGINE v1.0 ONLINE")
        print("INSTITUTIONAL SYSTEM HEALTH CONTROL ACTIVE")
        print("==============================")


        self.required_modules = [

            "intelligence_bridge.py",
            "pattern_matching_engine.py",
            "confidence_engine.py",
            "trade_lifecycle_engine.py",
            "execution_control_engine.py",
            "broker_execution_gate.py",
            "risk_position_engine.py",
            "decision_governor_engine.py",
            "portfolio_risk_governor_engine.py",
            "capital_protection_engine.py",
            "final_approval_gate_engine.py"

        ]


    def check_system(self):

        available = []
        missing = []


        for module in self.required_modules:

            path = (
                "intelligence/"
                +
                module
            )


            if os.path.exists(path):

                available.append(module)

            else:

                missing.append(module)



        if len(missing) == 0:

            status = "SYSTEM READY"
            decision = "START PIPELINE"

        else:

            status = "SYSTEM DEGRADED"
            decision = "REPAIR REQUIRED"



        result = {

            "status":
                status,

            "decision":
                decision,

            "modules_available":
                len(available),

            "modules_missing":
                len(missing),

            "missing":
                missing,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS SUPERVISOR RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = SystemSupervisorEngine()

    engine.check_system()
