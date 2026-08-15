"""
=========================================================

GSIS INSTITUTIONAL

PATTERN MEMORY ENGINE v1.2

Persistent Experience Learning Layer

Decision
    ↓
Pattern Extraction
    ↓
Learning Database
    ↓
Future Recognition

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
    sys.path.insert(0, PROJECT_ROOT)



from core.event_bus import event_bus

from database.database_engine import DatabaseEngine




class PatternMemoryEngine:


    def __init__(self):

        self.database = DatabaseEngine()

        self.memory_count = 0


        print("==============================")
        print("GSIS PATTERN MEMORY ENGINE v1.2 ONLINE")
        print("==============================")
        print("PERSISTENT LEARNING ACTIVE")
        print("==============================")




    def store_pattern(self, decision):


        pattern = {


            "symbol":
            decision.get(
                "symbol",
                "UNKNOWN"
            ),


            "pattern_type":
            decision.get(
                "decision",
                "UNKNOWN"
            ),


            "market_state":
            decision.get(
                "trend",
                "UNKNOWN"
            ),


            "momentum":
            decision.get(
                "momentum",
                "UNKNOWN"
            ),


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

        print("==============================")
        print("GSIS EXPERIENCE MEMORY")
        print("==============================")

        print(pattern)



        try:


            self.database.save_learning_memory(
                pattern
            )


            self.memory_count += 1


            print(
                "PATTERN SAVED TO LEARNING MEMORY"
            )


            print(
                "TOTAL PATTERNS:",
                self.memory_count
            )


        except Exception as error:


            print(
                "LEARNING MEMORY ERROR:",
                error
            )



        event_bus.publish(

            "pattern_memory",

            pattern

        )





engine = PatternMemoryEngine()



event_bus.subscribe(

    "market_decision",

    engine.store_pattern

)




def pattern_listener(data):


    print()

    print(
        "PATTERN MEMORY EVENT RECEIVED"
    )

    print(data)



event_bus.subscribe(

    "pattern_memory",

    pattern_listener

)
