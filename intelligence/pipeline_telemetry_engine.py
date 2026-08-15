import datetime
import json
import os


class PipelineTelemetryEngine:

    def __init__(self):

        print("==============================")
        print("GSIS PIPELINE TELEMETRY ENGINE v1.0 ONLINE")
        print("INSTITUTIONAL PIPELINE MONITORING ACTIVE")
        print("==============================")

        self.file = "intelligence/pipeline_telemetry.json"



    def record(
        self,
        stage,
        status,
        data
    ):

        event = {

            "stage":
                stage,

            "status":
                status,

            "data":
                data,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        records = []


        if os.path.exists(self.file):

            try:

                with open(
                    self.file,
                    "r"
                ) as f:

                    records = json.load(f)

            except:

                records = []



        records.append(event)


        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                records,
                f,
                indent=4
            )


        result = {

            "status":
                "TELEMETRY RECORDED",

            "stage":
                stage,

            "total_events":
                len(records),

            "timestamp":
                event["timestamp"]

        }


        print("==============================")
        print("GSIS TELEMETRY RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = PipelineTelemetryEngine()


    engine.record(

        stage="SYSTEM_START",

        status="SUCCESS",

        data={

            "module":
                "TELEMETRY",

            "mode":
                "SIMULATION"

        }

    )
