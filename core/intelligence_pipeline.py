"""
=========================================================
GSIS INSTITUTIONAL
Intelligence Pipeline Manager
Version: 1.0
=========================================================
"""

from intelligence.feature_manager import FeatureManager
from intelligence.market_regime_engine import MarketRegimeEngine
from intelligence.bayesian_engine import BayesianEngine
from intelligence.decision_engine import DecisionEngine


class IntelligencePipeline:


    def __init__(self):

        self.feature_manager = FeatureManager()

        self.regime_engine = MarketRegimeEngine()

        self.bayesian_engine = BayesianEngine()

        self.decision_engine = DecisionEngine()



    def initialize(self):

        print(
            "================================"
        )

        print(
            "GSIS INTELLIGENCE PIPELINE ONLINE"
        )

        print(
            "================================"
        )


        self.feature_manager.initialize()

        self.regime_engine.initialize()

        self.bayesian_engine.initialize()

        self.decision_engine.initialize()



    def analyze(
            self,
            symbol,
            timeframe):


        print(
            "[PIPELINE] ANALYSIS START"
        )


        # Generate features

        features = (
            self.feature_manager
            .engine
            .analyze(
                symbol,
                timeframe
            )
        )



        # Analyze market regime

        regime = (
            self.regime_engine
            .analyze(
                features
            )
        )



        # Placeholder historical result

        # Later connected to Pattern Database

        probability = (
            self.bayesian_engine
            .calculate_probability(
                0,
                0
            )
        )



        # Final evaluation

        decision = (

            self.decision_engine
            .evaluate(

                probability[
                    "probability"
                ],

                regime[
                    "regime"
                ],

                probability[
                    "confidence"
                ]

            )

        )


        return decision
