"""
=========================================================
GSIS INSTITUTIONAL

INSTITUTIONAL RISK INTELLIGENCE ENGINE (IRIE)

Version: 2.0

Functions:
- Evaluate institutional risk
- Calculate confidence
- Approve or reject execution

=========================================================
"""


from datetime import datetime
import uuid



class RiskEngine:


    def __init__(self):

        self.name = "Institutional Risk Intelligence Engine"

        self.status = "CREATED"

        self.history = []



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("RISK INTELLIGENCE ENGINE ONLINE")
        print("==============================")



    def analyze(
            self,
            smart_money_score,
            mtf_score,
            volatility,
            stop_distance,
            account_risk):


        risk_score = 0


        # Smart Money quality

        risk_score += (
            smart_money_score
            *
            0.35
        )


        # MTF alignment

        risk_score += (
            mtf_score
            *
            0.25
        )


        # Volatility

        if volatility == "LOW":

            risk_score += 20


        elif volatility == "NORMAL":

            risk_score += 15


        else:

            risk_score += 5



        # Stop distance

        if stop_distance > 0:

            risk_score += 10



        # Account risk control

        if account_risk <= 1:

            risk_score += 10



        confidence = min(
            round(risk_score,2),
            100
        )


        decision = self.decision(
            confidence
        )


        report = {


            "risk_id":

            str(uuid.uuid4()),


            "timestamp":

            str(datetime.utcnow()),


            "confidence":

            confidence,


            "risk_level":

            self.risk_level(
                confidence
            ),


            "decision":

            decision

        }


        self.history.append(report)


        return report



    def decision(
            self,
            confidence):


        if confidence >= 80:

            return "APPROVED"


        elif confidence >= 60:

            return "CAUTION"


        else:

            return "REJECTED"



    def risk_level(
            self,
            confidence):


        if confidence >= 85:

            return "LOW RISK"


        elif confidence >= 65:

            return "MEDIUM RISK"


        else:

            return "HIGH RISK"



    def report(self):

        return self.history
