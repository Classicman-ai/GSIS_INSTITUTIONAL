# ==========================================================
# GSIS PATTERN MEMORY ENGINE v1.0
# Institutional Learning Memory Layer
# ==========================================================


from datetime import datetime, timezone


class PatternMemoryEngine:


    def __init__(self):

        self.memory = []

        print("==============================")
        print("GSIS PATTERN MEMORY ENGINE v1.0 ONLINE")
        print("==============================")
        print("PERSISTENT PATTERN MEMORY ACTIVE")



    def store(self, decision):


        pattern = {


            "symbol":
                decision.get(
                    "symbol",
                    "UNKNOWN"
                ),


            "pattern_type":
                decision.get(
                    "decision",
                    "UNKNOWN"
                ),


            "market_state":
                decision.get(
                    "trend",
                    "UNKNOWN"
                ),


            "momentum":
                decision.get(
                    "momentum",
                    "UNKNOWN"
                ),


            "confidence":
                decision.get(
                    "confidence",
                    0
                ),


            "timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat()

        }


        self.memory.append(pattern)


        print("==============================")
        print("GSIS EXPERIENCE MEMORY")
        print("==============================")

        print(pattern)

        print(
            "TOTAL PATTERNS:",
            len(self.memory)
        )


        return pattern




    def save(self, decision):

        return self.store(decision)



    def process(self, decision):

        return self.store(decision)



# Global engine required by pipeline

engine = PatternMemoryEngine()
