import sqlite3
import datetime


class GSISKnowledgeEngine:

    def __init__(self):

        print("==============================")
        print("GSIS KNOWLEDGE ENGINE v1.0 ONLINE")
        print("HISTORICAL INTELLIGENCE ANALYSIS ACTIVE")
        print("==============================")

        self.database = "database/gsis_intelligence.db"


    def connect(self):

        return sqlite3.connect(
            self.database
        )


    def total_memory(self):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM market_reactions"
        )

        result = cursor.fetchone()[0]

        conn.close()

        return result


    def analyze_event(
        self,
        event
    ):

        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT
            COUNT(*),
            AVG(confidence),
            AVG(rr)

            FROM market_reactions

            WHERE event = ?

            """,

            (event,)

        )


        result = cursor.fetchone()

        conn.close()


        if result[0] == 0:

            return {

                "status":
                "NO HISTORICAL DATA",

                "event":
                event,

                "samples":
                0

            }


        return {

            "status":
            "KNOWLEDGE ANALYSIS COMPLETE",

            "event":
            event,

            "historical_samples":
            result[0],

            "average_confidence":
            round(
                result[1],
                2
            ),

            "average_rr":
            round(
                result[2],
                2
            ),

            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }


    def store_learning(
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


    engine = GSISKnowledgeEngine()


    print("==============================")
    print("GSIS KNOWLEDGE STATUS")
    print("==============================")

    print({

        "memory_records":
        engine.total_memory()

    })


    print(
        engine.analyze_event(
            "NFP"
        )
    )


    engine.store_learning(

        "BEARISH_ENGULFING",

        "NFP + LIQUIDITY SWEEP + BOS",

        "WIN",

        94

    )


    print("==============================")
    print("LEARNING MEMORY UPDATED")
    print("==============================")
