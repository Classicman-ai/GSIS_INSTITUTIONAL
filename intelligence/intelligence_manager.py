"""
=========================================================
GSIS INSTITUTIONAL
INTELLIGENCE MANAGER
Version: 2.1

Complete Intelligence Coordination Layer
=========================================================
"""


from intelligence.market_regime_engine import MarketRegimeEngine
from intelligence.bayesian_engine import BayesianEngine
from intelligence.decision_engine import DecisionEngine

from intelligence.pattern_discovery_engine import PatternDiscoveryEngine
from intelligence.pattern_memory_connector import PatternMemoryConnector

from intelligence.event_intelligence_engine import EventIntelligenceEngine
from intelligence.confidence_classifier import ConfidenceClassifier

from intelligence.intelligence_memory_writer import IntelligenceMemoryWriter



class IntelligenceManager:


    def __init__(self):


        self.regime_engine = MarketRegimeEngine()

        self.bayesian_engine = BayesianEngine()

        self.decision_engine = DecisionEngine()

        self.pattern_engine = PatternDiscoveryEngine()

        self.pattern_memory = PatternMemoryConnector()

        self.event_engine = EventIntelligenceEngine()

        self.confidence = ConfidenceClassifier()

        self.memory_writer = IntelligenceMemoryWriter()



    def initialize(self):


        print("==============================")
        print("GSIS INTELLIGENCE SYSTEM ONLINE")
        print("==============================")


        self.regime_engine.initialize()

        self.bayesian_engine.initialize()

        self.decision_engine.initialize()

        self.pattern_engine.initialize()

        self.pattern_memory.initialize()

        self.event_engine.initialize()

        self.confidence.initialize()

        self.memory_writer.initialize()



    def analyze(self, features):


        if not features:

            return None



        regime = self.regime_engine.analyze(
            features
        )



        pattern = self.pattern_engine.discover(
            features
        )


        pattern["regime"] = regime.get(
            "regime",
            "UNKNOWN"
        )



        pattern_id = self.pattern_memory.store_pattern(
            pattern
        )



        probability = self.bayesian_engine.calculate_probability(
            0,
            0,
            0
        )



        confidence = self.confidence.classify(
            {

                "probability":
                probability["probability"],

                "similarity":
                0,

                "regime":
                regime.get("regime"),

                "event_risk":
                False,

                "risk_reward":
                0

            }
        )



        decision = self.decision_engine.evaluate(
            confidence["score"],
            regime.get("regime"),
            confidence["grade"]
        )



        intelligence = {


            "pattern_id":

            pattern_id,


            "regime":

            regime,


            "probability":

            probability,


            "confidence":

            confidence,


            "decision":

            decision

        }



        self.memory_writer.save_intelligence(

            intelligence,

            features

        )



        return intelligence
