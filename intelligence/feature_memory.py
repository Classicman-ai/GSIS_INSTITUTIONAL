"""
=========================================================

GSIS INSTITUTIONAL

FEATURE MEMORY ENGINE v1.1

Stores Statistical Intelligence

Database Connected Version

=========================================================
"""

import os
import sys


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from database.database_engine import DatabaseEngine
from core.event_bus import event_bus



class FeatureMemory:


    def __init__(self):

        self.database = DatabaseEngine()

        try:

            self.database.initialize()

            print(
                "FEATURE MEMORY DATABASE CONNECTED"
            )

        except Exception as error:

            print(
                "DATABASE INITIALIZATION ERROR:",
                error
            )


        print("==============================")
        print("GSIS FEATURE MEMORY v1.1 ONLINE")
        print("==============================")



    def save_feature(self, feature):


        print()

        print(
            "FEATURE STORED:"
        )

        print(feature)


        try:


            self.database.log_event(

                "Market feature generated"

            )


            print(
                "FEATURE MEMORY UPDATED"
            )


        except Exception as error:


            print(

                "MEMORY STORAGE ERROR:",

                error

            )



memory = FeatureMemory()



event_bus.subscribe(

    "market_features",

    memory.save_feature

)
