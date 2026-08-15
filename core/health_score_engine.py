"""
=========================================================
GSIS INSTITUTIONAL

SYSTEM HEALTH SCORING ENGINE (SHSE)

Version: 1.0

Functions:
- Calculate system health
- Assign institutional grade
- Generate operational status

=========================================================
"""


class HealthScoreEngine:


    def __init__(self):


        self.name = "System Health Scoring Engine"

        self.status = "CREATED"



    def initialize(self):


        self.status = "ONLINE"


        print("==============================")

        print(
            "HEALTH SCORE ENGINE ONLINE"
        )

        print("==============================")



    def calculate(
            self,
            engine_score,
            data_score,
            communication_score,
            error_score):


        total = (

            engine_score * 0.30

            +

            data_score * 0.30

            +

            communication_score * 0.20

            +

            error_score * 0.20

        )


        grade = self.grade(
            total
        )


        return {


            "health_score":
            round(total,2),


            "grade":
            grade,


            "status":
            self.status_from_grade(
                grade
            )

        }



    def grade(
            self,
            score):


        if score >= 95:

            return "A+"

        elif score >= 90:

            return "A"

        elif score >= 80:

            return "B+"

        elif score >= 70:

            return "B"

        elif score >= 60:

            return "C"

        else:

            return "F"



    def status_from_grade(
            self,
            grade):


        if grade in ["A+","A","B+"]:

            return "OPERATIONAL"


        elif grade in ["B","C"]:

            return "DEGRADED"


        else:

            return "CRITICAL"
