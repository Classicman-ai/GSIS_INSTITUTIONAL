"""
=========================================================
GSIS INSTITUTIONAL
Feature Intelligence Manager
Version: 1.0
=========================================================
"""

from intelligence.feature_engine import FeatureEngine
from database.feature_database import FeatureDatabase


class FeatureManager:


    def __init__(self):

        self.engine = FeatureEngine()

        self.database = FeatureDatabase()



    def initialize(self):

        print(
            "[FEATURE MANAGER] Starting..."
        )

        self.database.initialize()



    def process_market(
            self,
            symbol,
            timeframe):


        features = self.engine.analyze(
            symbol,
            timeframe
        )


        saved = 0


        for feature in features:


            self.database.save_feature(

                symbol,

                timeframe,

                feature

            )


            saved += 1



        print(
            "FEATURES SAVED:",
            saved
        )


        return saved



    def get_history(
            self,
            symbol,
            timeframe,
            limit=100):


        return self.database.get_features(

            symbol,

            timeframe,

            limit

        )
