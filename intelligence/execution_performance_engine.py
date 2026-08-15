"""
=========================================================
GSIS INSTITUTIONAL

INSTITUTIONAL EXECUTION PERFORMANCE
INTELLIGENCE ENGINE (IEPIE)

Version: 1.0

Functions:
- Measure execution quality
- Analyze execution costs
- Rank execution performance

=========================================================
"""


from datetime import datetime
import uuid



class ExecutionPerformanceEngine:


    def __init__(self):


        self.name = "Institutional Execution Performance Intelligence Engine"

        self.status = "CREATED"

        self.reports = []



    def initialize(self):


        self.status = "ONLINE"


        print("==============================")

        print(
            "EXECUTION PERFORMANCE ENGINE ONLINE"
        )

        print("==============================")



    def analyze(
            self,
            expected_price,
            executed_price,
            order_type,
            venue):


        slippage = abs(
            expected_price -
            executed_price
        )


        quality = 100



        if slippage > 0.05:


            quality -= 30



        elif slippage > 0.02:


            quality -= 15



        if order_type == "MARKET":


            quality -= 5



        grade = self.grade(
            quality
        )



        report = {


            "report_id":
            str(uuid.uuid4()),


            "timestamp":
            str(datetime.utcnow()),


            "venue":
            venue,


            "order_type":
            order_type,


            "slippage":
            round(
                slippage,
                5
            ),


            "execution_score":
            quality,


            "grade":
            grade

        }



        self.reports.append(
            report
        )


        return report



    def grade(
            self,
            score):


        if score >= 95:

            return "A+"


        elif score >= 85:

            return "A"


        elif score >= 70:

            return "B"


        else:

            return "C"



    def history(self):


        return self.reports
