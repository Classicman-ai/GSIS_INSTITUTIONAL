"""
=========================================================
GSIS INSTITUTIONAL

AI LEARNING & PATTERN EVOLUTION ENGINE

Version 1.0

Adaptive Pattern Intelligence System

=========================================================
"""


from datetime import datetime



class AILearningEngine:



    def __init__(self):

        self.name = "AI Learning Engine"

        self.status = "CREATED"

        self.pattern_memory = {}

        self.learning_history = []





    def initialize(self):


        self.status = "ONLINE"


        print("==============================")
        print("AI LEARNING ENGINE ONLINE")
        print("==============================")





    def learn_pattern(
            self,
            pattern,
            outcome):


        if pattern not in self.pattern_memory:


            self.pattern_memory[pattern] = {


                "wins":0,

                "losses":0,

                "confidence":50

            }



        if outcome == "WIN":

            self.pattern_memory[pattern]["wins"] += 1


        elif outcome == "LOSS":

            self.pattern_memory[pattern]["losses"] += 1




        self.update_confidence(
            pattern
        )


        return self.pattern_memory[pattern]






    def update_confidence(
            self,
            pattern):


        data = self.pattern_memory[pattern]


        total = (
            data["wins"]
            +
            data["losses"]
        )


        if total == 0:

            return



        success = (
            data["wins"]
            /
            total
        ) * 100



        if success >= 75:


            data["confidence"] += 5



        elif success < 40:


            data["confidence"] -= 5



        data["confidence"] = max(
            0,
            min(
                100,
                data["confidence"]
            )
        )





    def analyze_pattern(
            self,
            pattern):


        if pattern not in self.pattern_memory:

            return None



        data = self.pattern_memory[pattern]


        report = {


            "timestamp":

            str(datetime.utcnow()),


            "pattern":

            pattern,


            "statistics":

            data,


            "recommendation":

            self.recommend(
                data["confidence"]
            )

        }



        self.learning_history.append(
            report
        )


        return report






    def recommend(
            self,
            confidence):


        if confidence >= 80:

            return "PROMOTE"



        elif confidence >= 50:

            return "MONITOR"



        return "DEPRIORITIZE"






    def latest(self):


        if self.learning_history:

            return self.learning_history[-1]


        return None
