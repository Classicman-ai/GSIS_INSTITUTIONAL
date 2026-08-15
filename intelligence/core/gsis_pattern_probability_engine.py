import os
import sqlite3
import datetime


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


PATTERN_DATABASE = os.path.join(
    BASE_DIR,
    "database",
    "pattern_memory.sqlite"
)



class GSISPatternProbabilityEngine:


    def __init__(self):

        print("==============================")
        print("GSIS PATTERN PROBABILITY ENGINE v2.0 ONLINE")
        print("HISTORICAL PATTERN LEARNING ACTIVE")
        print("==============================")


        self.database = PATTERN_DATABASE



    def connect(self):

        return sqlite3.connect(
            self.database
        )



    def analyze_pattern(
        self,
        pattern
    ):


        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT
            samples,
            wins,
            losses,
            win_rate

            FROM pattern_memory

            WHERE pattern=?

            ORDER BY id DESC

            LIMIT 1

            """,
            (
                pattern,
            )
        )


        row = cursor.fetchone()


        conn.close()



        if not row:

            return {

                "status":
                "NO PATTERN DATA",

                "pattern":
                pattern,

                "samples":
                0,

                "historical_probability":
                0

            }



        samples = row[0]
        wins = row[1]
        losses = row[2]
        probability = row[3]



        return {


            "status":
            "PATTERN PROBABILITY COMPLETE",


            "pattern":
            pattern,


            "samples":
            samples,


            "wins":
            wins,


            "losses":
            losses,


            "historical_probability":
            probability,


            "win_probability":
            probability,


            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }



    # Compatibility layer
    def analyze(
        self,
        pattern
    ):

        return self.analyze_pattern(
            pattern
        )



    def store_pattern_result(

        self,

        pattern,

        context,

        outcome,

        confidence

    ):


        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute(

            """
            INSERT INTO pattern_memory

            (

            symbol,

            pattern,

            direction,

            samples,

            wins,

            losses,

            win_rate

            )

            VALUES (?,?,?,?,?,?,?)

            """,

            (

            "XAUUSD",

            pattern,

            context,

            1,

            1 if outcome=="WIN" else 0,

            0 if outcome=="WIN" else 1,

            confidence

            )

        )


        conn.commit()

        conn.close()



if __name__ == "__main__":


    engine = GSISPatternProbabilityEngine()


    print(
        engine.analyze_pattern(
            "BULLISH_CANDLE"
        )
    )
