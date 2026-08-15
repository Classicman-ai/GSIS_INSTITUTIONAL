import sqlite3
import datetime


class GSISAdaptiveLearningEngine:

    def __init__(self):

        print("==============================")
        print("GSIS ADAPTIVE LEARNING ENGINE v1.0 ONLINE")
        print("SELF IMPROVEMENT LEARNING ACTIVE")
        print("==============================")

        self.database = "database/gsis_intelligence.db"



    def connect(self):

        return sqlite3.connect(
            self.database
        )



    def evaluate_pattern(

        self,

        pattern

    ):

        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute(

            """

            SELECT

            COUNT(*),

            SUM(

                CASE

                WHEN outcome='WIN'

                THEN 1

                ELSE 0

                END

            )

            FROM learning_memory

            WHERE pattern=?

            """,

            (pattern,)

        )


        result = cursor.fetchone()


        conn.close()


        samples = result[0] or 0

        wins = result[1] or 0


        if samples == 0:

            return {

                "status":
                "NO LEARNING DATA",

                "pattern":
                pattern

            }



        win_rate = round(

            (wins / samples) * 100,

            2

        )


        adjustment = self.calculate_adjustment(

            win_rate,

            samples

        )


        return {

            "status":

            "ADAPTIVE ANALYSIS COMPLETE",


            "pattern":

            pattern,


            "samples":

            samples,


            "wins":

            wins,


            "win_rate":

            win_rate,


            "confidence_adjustment":

            adjustment,


            "timestamp":

            datetime.datetime.now(

                datetime.timezone.utc

            ).isoformat()

        }



    def calculate_adjustment(

        self,

        win_rate,

        samples

    ):


        if samples < 20:

            return 0


        if win_rate >= 75:

            return "+10"


        elif win_rate >= 60:

            return "+5"


        elif win_rate >= 50:

            return "0"


        else:

            return "-10"





    def store_feedback(

        self,

        pattern,

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

            "ADAPTIVE_FEEDBACK",

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


    engine = GSISAdaptiveLearningEngine()


    print("==============================")
    print("GSIS LEARNING RESULT")
    print("==============================")


    print(

        engine.evaluate_pattern(

            "BEARISH_ENGULFING"

        )

    )


    engine.store_feedback(

        "BEARISH_ENGULFING",

        "WIN",

        92

    )


    print("==============================")
    print("ADAPTIVE MEMORY UPDATED")
    print("==============================")
