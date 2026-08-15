"""
=========================================================

GSIS INSTITUTIONAL

OUTCOME MEMORY ENGINE v1.0

Decision Result Learning Layer

Decision
    ↓
Market Movement
    ↓
Outcome Evaluation
    ↓
Learning Update

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

from database.database_engine import DatabaseEngine




class OutcomeMemoryEngine:


    def __init__(self):

        self.database = DatabaseEngine()

        print("==============================")
        print("GSIS OUTCOME MEMORY ENGINE v1.0 ONLINE")
        print("==============================")
        print("RESULT LEARNING ACTIVE")
        print("==============================")




    def evaluate(self, decision):


        print()

        print("==============================")
        print("GSIS OUTCOME EVALUATION")
        print("==============================")


        print(
            "DECISION RECEIVED:"
        )

        print(decision)



        # Temporary evaluation logic
        # Will later connect to live price tracking

        if decision.get("decision") == "WAIT":

            outcome = "NEUTRAL"

        else:

            outcome = "PENDING"



        result = {


            "symbol":
            decision.get(
                "symbol"
            ),


            "decision":
            decision.get(
                "decision"
            ),


            "outcome":
            outcome,


            "confidence":
            decision.get(
                "confidence",
                0
            ),


            "timestamp":
            datetime.now(
                UTC
            ).isoformat()

        }



        print()

        print(
            "OUTCOME RESULT:"
        )

        print(result)



        event_bus.publish(

            "market_outcome",

            result

        )





engine = OutcomeMemoryEngine()



event_bus.subscribe(

    "market_decision",

    engine.evaluate

)




def outcome_listener(data):


    print()

    print(
        "OUTCOME EVENT RECEIVED"
    )

    print(data)




event_bus.subscribe(

    "market_outcome",

    outcome_listener

)
