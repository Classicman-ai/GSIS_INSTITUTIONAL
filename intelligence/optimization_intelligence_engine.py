"""
=========================================================
GSIS INSTITUTIONAL

OPTIMIZATION INTELLIGENCE ENGINE

Version 1.0

Self Improvement Analysis System

=========================================================
"""


from datetime import datetime



class OptimizationIntelligenceEngine:


    def __init__(self):

        self.name = "Optimization Intelligence Engine"

        self.status = "CREATED"

        self.reports = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("OPTIMIZATION INTELLIGENCE ENGINE ONLINE")
        print("==============================")





    def analyze(self, records):


        total = len(records)


        wins = 0

        losses = 0


        confidence_total = 0



        for record in records:


            confidence_total += record.get(
                "confidence",
                0
            )


            if record.get(
                "outcome"
            ) == "WIN":

                wins += 1



            elif record.get(
                "outcome"
            ) == "LOSS":

                losses += 1





        win_rate = 0


        if total > 0:

            win_rate = (
                wins / total
            ) * 100



        average_confidence = 0


        if total > 0:

            average_confidence = (
                confidence_total / total
            )



        report = {


            "timestamp":

            str(datetime.utcnow()),


            "samples":

            total,


            "win_rate":

            round(
                win_rate,
                2
            ),


            "average_confidence":

            round(
                average_confidence,
                2
            ),


            "recommendation":

            self.recommend(
                win_rate
            )

        }



        self.reports.append(report)


        return report






    def recommend(self, win_rate):


        if win_rate >= 70:

            return "PROMOTE PATTERN"



        elif win_rate >= 50:

            return "CONTINUE MONITORING"



        else:

            return "REVIEW AND OPTIMIZE"






    def latest(self):


        if self.reports:

            return self.reports[-1]


        return None
