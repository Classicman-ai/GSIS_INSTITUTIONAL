"""
=========================================================
GSIS INSTITUTIONAL

INTELLIGENCE CONTEXT MEMORY ENGINE (ICME)

Version: 1.0

Functions:
- Store market intelligence events
- Retrieve historical patterns
- Calculate memory confidence

=========================================================
"""


from datetime import datetime
import uuid



class ContextMemoryEngine:


    def __init__(self):

        self.name = "Intelligence Context Memory Engine"

        self.status = "CREATED"

        self.memory = []



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("CONTEXT MEMORY ENGINE ONLINE")
        print("==============================")



    def store(
            self,
            context):


        record = {


            "memory_id":

            str(uuid.uuid4()),


            "timestamp":

            str(datetime.utcnow()),


            "asset":

            context.get(
                "asset"
            ),


            "pattern":

            context.get(
                "pattern"
            ),


            "direction":

            context.get(
                "direction"
            ),


            "score":

            context.get(
                "score"
            ),


            "outcome":

            context.get(
                "outcome",
                "UNKNOWN"
            )

        }


        self.memory.append(record)


        return record



    def search(
            self,
            pattern):


        matches = []


        for item in self.memory:


            if item["pattern"] == pattern:

                matches.append(item)



        return matches



    def confidence(
            self,
            matches):


        if not matches:

            return 0



        wins = 0


        for item in matches:


            if item["outcome"] == "WIN":

                wins += 1



        return round(

            (wins / len(matches))
            *
            100,

            2

        )



    def all_memory(self):

        return self.memory
