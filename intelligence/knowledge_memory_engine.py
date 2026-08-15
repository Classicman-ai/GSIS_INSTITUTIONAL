"""
=========================================================
GSIS INSTITUTIONAL

KNOWLEDGE MEMORY & EXPERIENCE INTELLIGENCE ENGINE

Version 1.0

Institutional Memory Layer

=========================================================
"""


from datetime import datetime
import uuid



class KnowledgeMemoryEngine:


    def __init__(self):

        self.name = "Knowledge Memory Engine"

        self.status = "CREATED"

        self.memories = []

        self.patterns = []

        self.lessons = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("KNOWLEDGE MEMORY ENGINE ONLINE")
        print("==============================")





    def store_memory(
            self,
            category,
            information):


        memory = {


            "id":

            str(uuid.uuid4()),


            "category":

            category,


            "information":

            information,


            "time":

            str(datetime.utcnow())

        }



        self.memories.append(memory)


        return memory






    def store_pattern(
            self,
            pattern,
            outcome,
            confidence):


        record = {


            "pattern":

            pattern,


            "outcome":

            outcome,


            "confidence":

            confidence,


            "time":

            str(datetime.utcnow())

        }



        self.patterns.append(record)


        return record






    def search_pattern(
            self,
            pattern):


        return [

            item

            for item in self.patterns

            if pattern.lower()
            in item["pattern"].lower()

        ]






    def record_lesson(
            self,
            lesson):


        data = {


            "lesson":

            lesson,


            "time":

            str(datetime.utcnow())

        }



        self.lessons.append(data)


        return data






    def memory_report(self):


        return {


            "status":

            self.status,


            "memories":

            len(self.memories),


            "patterns":

            len(self.patterns),


            "lessons":

            len(self.lessons)

        }
