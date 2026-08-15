"""
=========================================================
GSIS INSTITUTIONAL
PATTERN MEMORY CONNECTOR
Version: 1.0

Pattern Discovery + Pattern Library Integration
=========================================================
"""


from database.pattern_library import PatternLibraryDatabase



class PatternMemoryConnector:


    def __init__(self):

        self.library = PatternLibraryDatabase()

        self.status = "CREATED"



    def initialize(self):

        self.library.initialize()

        self.status = "ONLINE"


        print(
            "PATTERN MEMORY CONNECTOR ONLINE"
        )



    def store_pattern(
            self,
            pattern):


        record = {


            "pattern_name":

            self.generate_name(

                pattern

            ),


            "symbol":

            pattern.get(

                "symbol",

                "UNKNOWN"

            ),


            "timeframe":

            pattern.get(

                "timeframe",

                "UNKNOWN"

            ),


            "regime":

            pattern.get(

                "regime",

                "UNKNOWN"

            ),


            "direction":

            pattern.get(

                "direction",

                "NEUTRAL"

            ),


            "confidence_grade":

            "UNDEFINED",


            "probability":

            0

        }



        pattern_id = (

            self.library.create_pattern(

                record

            )

        )


        return pattern_id



    def generate_name(
            self,
            pattern):


        direction = pattern.get(

            "direction",

            "UNKNOWN"

        )


        volatility = pattern.get(

            "volatility_state",

            "UNKNOWN"

        )


        return (

            direction

            +

            "_"

            +

            volatility

        )
