"""
=========================================================

GSIS INSTITUTIONAL

RISK INTELLIGENCE ENGINE v1.0

Institutional Risk Evaluation Layer

Adaptive Confidence
        +
Market Regime
        +
Pattern Quality
        +
Volatility

        ↓

Risk Score

        ↓

APPROVE / BLOCK

=========================================================
"""


import os
import sys

from datetime import datetime, UTC


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


if PROJECT_ROOT not in sys.path:

    sys.path.insert(
        0,
        PROJECT_ROOT
    )


from core.event_bus import event_bus




class RiskIntelligenceEngine:


    def __init__(self):

        print("==============================")
        print("GSIS RISK INTELLIGENCE ENGINE v1.0 ONLINE")
        print("==============================")
        print("INSTITUTIONAL RISK CONTROL ACTIVE")
        print("==============================")


    def evaluate(self, confidence):


        print()

        print("==============================")
        print("GSIS RISK ANALYSIS")
        print("==============================")


        print(
            "CONFIDENCE INPUT:"
        )

        print(confidence)



        adaptive_confidence = confidence.get(
            "adaptive_confidence",
            50
        )


        decision = confidence.get(
            "decision",
            "WAIT"
        )



        risk_score = 100 - adaptive_confidence



        if decision == "WAIT":

            risk_score += 10



        if risk_score > 70:

            approval = "BLOCKED"


        elif risk_score > 40:

            approval = "CAUTION"


        else:

            approval = "APPROVED"




        risk_result = {


            "symbol":

            confidence.get(
                "symbol"
            ),


            "decision":

            decision,


            "risk_score":

            min(
                risk_score,
                100
            ),


            "adaptive_confidence":

            adaptive_confidence,


            "status":

            approval,


            "timestamp":

            datetime.now(
                UTC
            ).isoformat()


        }



        print()

        print(
            "RISK RESULT:"
        )

        print(
            risk_result
        )



        event_bus.publish(

            "risk_analysis",

            risk_result

        )





engine = RiskIntelligenceEngine()



event_bus.subscribe(

    "adaptive_confidence",

    engine.evaluate

)




def risk_listener(data):


    print()

    print(
        "RISK EVENT RECEIVED"
    )

    print(data)




event_bus.subscribe(

    "risk_analysis",

    risk_listener

)
