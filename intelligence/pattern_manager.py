"""
=========================================================
GSIS INSTITUTIONAL
Pattern Intelligence Manager
Version: 1.0
=========================================================
"""

from intelligence.pattern_engine import PatternEngine
from database.pattern_database import PatternDatabase


class PatternManager:


    def __init__(self):

        self.pattern_engine = PatternEngine()

        self.database = PatternDatabase()



    def initialize(self):

        print(
            "[PATTERN MANAGER] Initializing..."
        )

        self.database.initialize()

        self.pattern_engine.initialize()



    def create_pattern(
            self,
            asset,
            timeframe,
            pattern_type,
            conditions):


        pattern_id = self.database.add_pattern(
            asset,
            timeframe,
            pattern_type,
            conditions
        )


        self.pattern_engine.add_pattern(
            {
                "id": pattern_id,
                "conditions": conditions,
                "probability": 0
            }
        )


        print(
            "[NEW PATTERN]",
            pattern_id
        )


        return pattern_id



    def analyze_market(
            self,
            market_state):


        results = (
            self.pattern_engine
            .search_similarity(
                market_state
            )
        )


        return results



    def record_outcome(
            self,
            pattern_id,
            success):


        self.database.update_result(
            pattern_id,
            success
        )


        print(
            "[PATTERN UPDATED]",
            pattern_id
        )
