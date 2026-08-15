import datetime
import json
import os


class AuditComplianceEngine:

    def __init__(self):

        print("==============================")
        print("GSIS AUDIT COMPLIANCE ENGINE v1.0 ONLINE")
        print("INSTITUTIONAL AUDIT CONTROL ACTIVE")
        print("==============================")

        self.file = "intelligence/gsis_audit_log.json"


    def record(
        self,
        event,
        status,
        details
    ):

        entry = {

            "event":
                event,

            "status":
                status,

            "details":
                details,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        logs = []


        if os.path.exists(self.file):

            try:

                with open(
                    self.file,
                    "r"
                ) as f:

                    logs = json.load(f)

            except:

                logs = []


        logs.append(entry)


        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                logs,
                f,
                indent=4
            )


        result = {

            "status":
                "AUDIT RECORDED",

            "event":
                event,

            "total_records":
                len(logs),

            "timestamp":
                entry["timestamp"]

        }


        print("==============================")
        print("GSIS AUDIT RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = AuditComplianceEngine()


    engine.record(

        event="PIPELINE_TEST",

        status="SUCCESS",

        details={

            "module":
                "AUDIT ENGINE",

            "environment":
                "SIMULATION"

        }

    )
