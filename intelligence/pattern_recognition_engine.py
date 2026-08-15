import sqlite3
import os
from collections import Counter


DB_PATH = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    ),
    "database",
    "gsis_memory.db"
)


class PatternRecognitionEngine:


    def __init__(self):

        print("==============================")
        print("GSIS PATTERN RECOGNITION ENGINE v1.0 ONLINE")
        print("==============================")
        print("INSTITUTIONAL PATTERN LEARNING ACTIVE")
        print("==============================")



    def load_signals(self):

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()


        cursor.execute("""
        SELECT
        symbol,
        direction,
        confidence,
        reason

        FROM signals

        """)


        data = cursor.fetchall()


        conn.close()


        return data



    def analyze_patterns(self):


        signals = self.load_signals()


        if not signals:

            return {

                "status":"NO DATA",

                "patterns":[]

            }



        patterns = Counter()



        for signal in signals:


            symbol = signal[0]

            direction = signal[1]

            reason = signal[3]


            pattern = (
                symbol
                +
                "_"
                +
                direction
                +
                "_"
                +
                "_".join(
                    reason.split(",")
                )
            )


            patterns[pattern] += 1



        result = {


            "total_signals":
                len(signals),


            "patterns":
                patterns.most_common(10),


            "status":
                "LEARNING ACTIVE"

        }



        return result





if __name__ == "__main__":


    engine = PatternRecognitionEngine()


    result = engine.analyze_patterns()


    print("==============================")
    print("GSIS PATTERN ANALYSIS")
    print("==============================")

    print(result)
