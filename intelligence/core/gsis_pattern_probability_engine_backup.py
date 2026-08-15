import sqlite3
import datetime


class GSISPatternProbabilityEngine:

    def __init__(self):

        print("==============================")
        print("GSIS PATTERN PROBABILITY ENGINE v1.0 ONLINE")
        print("PATTERN PERFORMANCE ANALYSIS ACTIVE")
        print("==============================")

        self.database = "database/gsis_intelligence.db"


    def connect(self):

        return sqlite3.connect(
            self.database
        )


    def analyze_pattern(self, pattern):

        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute(

            """
            SELECT
            COUNT(*)

            FROM learning_memory

            WHERE pattern = ?

            """,

            (pattern,)

        )


        samples = cursor.fetchone()[0]


        cursor.execute(

            """
            SELECT
            COUNT(*)

            FROM learning_memory

            WHERE

            pattern = ?

            AND

            outcome = 'WIN'

            """,

            (pattern,)

        )


        wins = cursor.fetchone()[0]


        conn.close()


        if samples == 0:

            return {

                "status":
                "NO PATTERN DATA",

                "pattern":
                pattern,

                "samples":
                0

            }


        probability = round(

            (wins / samples) * 100,

            2

        )


        return {

            "status":
            "PATTERN PROBABILITY COMPLETE",

            "pattern":
            pattern,

            "samples":
            samples,

            "wins":
            wins,

            "win_probability":
            probability,

            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }



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

            INSERT INTO learning_memory

            (

            pattern,

            context,

            outcome,

            confidence,

            timestamp

            )

            VALUES (?,?,?,?,?)

            """,

            (

            pattern,

            context,

            outcome,

            confidence,

            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

            )

        )


        conn.commit()

        conn.close()



if __name__ == "__main__":


    engine = GSISPatternProbabilityEngine()


    print("==============================")
    print("GSIS PATTERN ANALYSIS RESULT")
    print("==============================")


    print(

        engine.analyze_pattern(

            "BEARISH_ENGULFING"

        )

    )


    engine.store_pattern_result(

        "BEARISH_ENGULFING",

        "SUPPLY_ZONE + LIQUIDITY_SWEEP + CHOCH",

        "WIN",

        92

    )


    print("==============================")
    print("PATTERN MEMORY UPDATED")
    print("==============================")
