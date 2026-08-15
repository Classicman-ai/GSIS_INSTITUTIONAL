"""
=========================================================
GSIS INSTITUTIONAL
VALIDATION ENGINE
Version: 2.0
Managed Module Architecture
=========================================================
"""


class ValidationEngine:


    def __init__(self):

        self.name = "Validation Engine"

        self.status = "CREATED"



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("GSIS VALIDATION ENGINE ONLINE")
        print("==============================")



    def validate_candle(
            self,
            candle):


        if candle is None:

            return False



        required = [

            "open",

            "high",

            "low",

            "close"

        ]


        for field in required:

            if field not in candle:

                print(
                    "MISSING FIELD:",
                    field
                )

                return False



        # Price validation

        if candle["high"] < candle["low"]:

            print(
                "INVALID HIGH/LOW"
            )

            return False



        if candle["close"] > candle["high"]:

            print(
                "INVALID CLOSE"
            )

            return False



        if candle["close"] < candle["low"]:

            print(
                "INVALID CLOSE"
            )

            return False



        return True



    def update(
            self,
            candles):


        validated = {}



        if not candles:

            return validated



        for timeframe, candle in candles.items():


            if self.validate_candle(candle):


                validated[timeframe] = candle


                print(

                    "VALIDATED:",

                    timeframe

                )


            else:

                print(

                    "REJECTED:",

                    timeframe

                )



        return validated



    def shutdown(self):

        self.status = "OFFLINE"

        print(
            "VALIDATION ENGINE STOPPED"
        )
