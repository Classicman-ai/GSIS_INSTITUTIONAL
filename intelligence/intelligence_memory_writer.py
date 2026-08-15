"""
=========================================================
GSIS INSTITUTIONAL
INTELLIGENCE MEMORY WRITER
Version: 1.0

Stores complete intelligence decisions
=========================================================
"""


from database.memory_connector import MemoryConnector



class IntelligenceMemoryWriter:


    def __init__(self):

        self.memory = MemoryConnector()

        self.status = "CREATED"



    def initialize(self):

        self.memory.initialize()

        self.status = "ONLINE"

        print("==============================")
        print("INTELLIGENCE MEMORY WRITER ONLINE")
        print("==============================")



    def save_intelligence(
            self,
            intelligence,
            features):


        record = {


            "timestamp":

            features.get(
                "timestamp"
            ),


            "symbol":

            features.get(
                "symbol",
                "XAUTUSDT"
            ),


            "timeframe":

            features.get(
                "timeframe",
                "M1"
            ),


            "close":

            features.get(
                "close"
            ),


            "return_pct":

            features.get(
                "return_pct"
            ),


            "volatility":

            features.get(
                "volatility"
            ),


            "direction":

            features.get(
                "direction"
            ),


            "volatility_state":

            features.get(
                "volatility_state"
            ),


            "regime":

            str(
                intelligence.get(
                    "regime"
                )
            ),


            "pattern_id":

            intelligence.get(
                "pattern_id"
            ),


            "probability":

            intelligence.get(
                "probability",
                {}
            ).get(
                "probability"
            ),


            "confidence_grade":

            intelligence.get(
                "confidence",
                {}
            ).get(
                "grade"
            ),


            "decision":

            str(
                intelligence.get(
                    "decision"
                )
            ),


            "outcome":

            None

        }


        return self.memory.store_market_state(

            record

        )
