import json
import os
import datetime


class PatternFeedbackEngine:

    def __init__(self):

        self.file = "data/gsis_outcome_memory.json"

        print("==============================")
        print("GSIS PATTERN FEEDBACK ENGINE v1.0 ONLINE")
        print("PATTERN PERFORMANCE LEARNING ACTIVE")
        print("==============================")


    def analyze_patterns(self):

        if not os.path.exists(self.file):

            return {
                "status": "NO MEMORY FOUND"
            }


        with open(self.file, "r") as f:

            memory = json.load(f)


        patterns = {}


        for trade in memory:

            pattern = trade.get(
                "pattern",
                "UNKNOWN"
            )

            result = trade.get(
                "result",
                "OPEN"
            )


            if pattern not in patterns:

                patterns[pattern] = {

                    "trades":0,
                    "wins":0,
                    "losses":0

                }


            patterns[pattern]["trades"] += 1


            if result == "WIN":

                patterns[pattern]["wins"] += 1


            elif result == "LOSS":

                patterns[pattern]["losses"] += 1



        for pattern,data in patterns.items():

            total = data["trades"]

            if total > 0:

                data["win_rate"] = round(
                    (data["wins"] / total) * 100,
                    2
                )


        output = {

            "status":
            "PATTERN ANALYSIS COMPLETE",

            "patterns":
            patterns,

            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }


        print("==============================")
        print("GSIS FEEDBACK RESULT")
        print("==============================")
        print(output)


        return output



if __name__ == "__main__":

    engine = PatternFeedbackEngine()

    engine.analyze_patterns()
