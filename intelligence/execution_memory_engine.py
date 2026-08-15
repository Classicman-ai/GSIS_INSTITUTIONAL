"""
=========================================================
GSIS INSTITUTIONAL

INSTITUTIONAL EXECUTION MEMORY &
KNOWLEDGE ENGINE (IEMKE)

Version: 1.0

Functions:
- Store execution history
- Retrieve previous executions
- Build execution knowledge

=========================================================
"""


from datetime import datetime
import uuid



class ExecutionMemoryEngine:


    def __init__(self):


        self.name = "Institutional Execution Memory Engine"

        self.status = "CREATED"

        self.memory = []



    def initialize(self):


        self.status = "ONLINE"


        print("==============================")

        print(
            "EXECUTION MEMORY ENGINE ONLINE"
        )

        print("==============================")



    def store(
            self,
            execution_data):


        record = {


            "memory_id":

            str(uuid.uuid4()),


            "timestamp":

            str(datetime.utcnow()),


            "execution":

            execution_data

        }


        self.memory.append(
            record
        )


        return record



    def search(
            self,
            asset=None,
            condition=None):


        results = []


        for item in self.memory:


            execution = item["execution"]



            if asset:


                if execution.get(
                    "asset"
                ) != asset:

                    continue



            if condition:


                if execution.get(
                    "condition"
                ) != condition:

                    continue



            results.append(
                item
            )


        return results



    def count(self):


        return len(
            self.memory
        )



    def history(self):


        return self.memory
