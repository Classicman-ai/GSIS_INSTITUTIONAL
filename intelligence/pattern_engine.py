"""
=========================================================
GSIS INSTITUTIONAL
Pattern Recognition Engine
Version: 1.0
=========================================================
"""

from core.base_engine import BaseEngine


class PatternEngine(BaseEngine):

    def __init__(self):

        super().__init__("Pattern Recognition Engine")

        self.pattern_library = []


    def initialize(self):

        super().initialize()

        print("================================")
        print("PATTERN ENGINE ONLINE")
        print("Historical Pattern Analysis Ready")
        print("================================")


    def add_pattern(self, pattern):

        self.pattern_library.append(pattern)

        print(
            "[PATTERN ADDED]",
            pattern.get("id")
        )


    def search_similarity(self, market_state):

        matches = []

        for pattern in self.pattern_library:

            similarity = self.compare(
                market_state,
                pattern["conditions"]
            )

            if similarity > 0:

                matches.append(
                    {
                        "pattern": pattern["id"],
                        "similarity": similarity,
                        "historical_probability":
                            pattern.get(
                                "probability",
                                0
                            )
                    }
                )

        return matches


    def compare(self, current, historical):

        total = len(historical)

        if total == 0:
            return 0

        matched = 0

        for key in historical:

            if key in current:

                if current[key] == historical[key]:
                    matched += 1


        return round(
            (matched / total) * 100,
            2
        )


    def run(self):

        self.status = "RUNNING"

        print(
            "[Pattern Engine] Scanning market patterns..."
        )


    def shutdown(self):

        super().shutdown()
