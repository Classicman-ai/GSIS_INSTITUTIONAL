"""
=========================================================
GSIS INSTITUTIONAL

PREDICTIVE SYSTEM RELIABILITY ENGINE (PSRE)

Version: 1.0

Functions:
- Analyze system stability
- Track reliability trends
- Predict operational risk

=========================================================
"""


from datetime import datetime



class ReliabilityEngine:


    def __init__(self):


        self.name = "Predictive Reliability Engine"

        self.status = "CREATED"

        self.history = []



    def initialize(self):


        self.status = "ONLINE"


        print("==============================")

        print(
            "RELIABILITY ENGINE ONLINE"
        )

        print("==============================")



    def analyze(
            self,
            component,
            errors,
            latency):


        risk = 0



        # Error contribution

        if errors > 10:

            risk += 40

        elif errors > 5:

            risk += 20



        # Latency contribution

        if latency > 1000:

            risk += 40

        elif latency > 500:

            risk += 20



        reliability = 100 - risk



        grade = self.grade(
            reliability
        )


        forecast = {


            "component":
            component,


            "timestamp":
            str(datetime.utcnow()),


            "reliability_score":
            reliability,


            "grade":
            grade,


            "risk":
            risk,


            "status":
            self.status_action(
                grade
            )

        }


        self.history.append(
            forecast
        )


        return forecast



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



    def status_action(
            self,
            grade):


        if grade in ["A+", "A", "B+"]:

            return "NORMAL_OPERATION"


        elif grade in ["B", "C"]:

            return "MONITOR"


        else:

            return "PREVENTIVE_ACTION_REQUIRED"
