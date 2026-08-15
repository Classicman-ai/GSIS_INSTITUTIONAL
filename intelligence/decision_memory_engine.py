import datetime
import json
import os


class DecisionMemoryEngine:

    def __init__(self):

        print("==============================")
        print("GSIS DECISION MEMORY ENGINE v1.0 ONLINE")
        print("AI DECISION HISTORY STORAGE ACTIVE")
        print("==============================")

        self.file = "intelligence/decision_memory.json"


    def store(
        self,
        decision,
        score,
        reasons
    ):

        record = {

            "decision":
                decision,

            "score":
                score,

            "reasons":
                reasons,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        memory = []


        if os.path.exists(self.file):

            try:

                with open(
                    self.file,
                    "r"
                ) as f:

                    memory = json.load(f)

            except:

                memory = []


        memory.append(record)


        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                memory,
                f,
                indent=4
            )


        result = {

            "status":
                "DECISION STORED",

            "decision":
                decision,

            "memory_size":
                len(memory),

            "timestamp":
                record["timestamp"]

        }


        print("==============================")
        print("GSIS DECISION MEMORY RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = DecisionMemoryEngine()


    engine.store(

        decision="EXECUTION APPROVED",

        score=90,

        reasons=[

            "INTELLIGENCE APPROVED",

            "RISK APPROVED",

            "CAPITAL APPROVED"

        ]

    )
