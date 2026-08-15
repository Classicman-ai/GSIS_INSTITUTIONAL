import os
import sqlite3
from datetime import datetime, timezone


print("==============================")
print("GSIS INTELLIGENCE MEMORY CONNECTOR v1.0 ONLINE")
print("MEMORY TO DECISION INTELLIGENCE BRIDGE ACTIVE")
print("==============================")


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


PATTERN_MEMORY_DB = os.path.join(
    BASE_DIR,
    "database",
    "pattern_memory.sqlite"
)


MARKET_MEMORY_DB = os.path.join(
    BASE_DIR,
    "database",
    "gsis_market_database.sqlite"
)



class GSISIntelligenceMemoryConnector:


    def __init__(self):

        self.pattern_db = sqlite3.connect(
            PATTERN_MEMORY_DB
        )

        self.market_db = sqlite3.connect(
            MARKET_MEMORY_DB
        )



    def get_pattern_memory(
        self,
        pattern=None
    ):

        cursor = self.pattern_db.cursor()


        if pattern:


            cursor.execute(

                """
                SELECT
                symbol,
                pattern,
                direction,
                samples,
                wins,
                losses,
                win_rate

                FROM pattern_memory

                WHERE pattern=?

                ORDER BY id DESC

                """,

                (
                    pattern,
                )

            )


        else:


            cursor.execute(

                """
                SELECT
                symbol,
                pattern,
                direction,
                samples,
                wins,
                losses,
                win_rate

                FROM pattern_memory

                ORDER BY id DESC

                """

            )



        rows = cursor.fetchall()


        memory = []


        for row in rows:


            memory.append(

                {

                    "symbol": row[0],

                    "pattern": row[1],

                    "direction": row[2],

                    "samples": row[3],

                    "wins": row[4],

                    "losses": row[5],

                    "win_rate": row[6]

                }

            )


        return memory




    def calculate_memory_score(
        self,
        pattern_memory
    ):


        if not pattern_memory:

            return 0



        total = 0


        for item in pattern_memory:


            total += item["win_rate"]



        score = (

            total
            /
            len(pattern_memory)

        )


        return round(
            score,
            2
        )




    def build_intelligence_profile(
        self,
        pattern=None
    ):


        memory = self.get_pattern_memory(
            pattern
        )


        score = self.calculate_memory_score(
            memory
        )


        return {


            "status":
            "MEMORY INTELLIGENCE READY",


            "pattern":
            pattern,


            "historical_samples":
            len(memory),


            "historical_probability":
            score,


            "memory_records":
            memory,


            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()

        }





if __name__ == "__main__":


    engine = GSISIntelligenceMemoryConnector()


    print("==============================")
    print("GSIS MEMORY INTELLIGENCE RESULT")
    print("==============================")


    result = engine.build_intelligence_profile()


    print(result)
