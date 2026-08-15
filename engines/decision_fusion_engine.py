"""
GSIS DECISION FUSION ENGINE
VERSION 1.0

Institutional Intelligence Scoring Layer

Combines:
- State Vector
- Regime
- Structure
- Liquidity
- Confidence
"""

from core.logger import Logger
from engines.state_vector_engine import StateVectorEngine
from core.database import Database
import time



class DecisionFusionEngine:


    engine_name = "DECISION_FUSION_ENGINE"
    version = "1.0"



    def __init__(self):

        self.logger = Logger(
            self.engine_name
        )

        self.state_engine = StateVectorEngine()

        self.db = Database()

        self.create_table()



    def create_table(self):

        self.db.execute("""

        CREATE TABLE IF NOT EXISTS decision_fusion (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            symbol TEXT,

            timestamp INTEGER,

            market_bias TEXT,

            confidence REAL,

            decision_score REAL,

            setup_quality TEXT,

            decision_state TEXT

        )

        """)



    def start(self):

        self.logger.info(
            "DECISION FUSION ENGINE ONLINE"
        )



    def analyze(self, symbol):


        vector = self.state_engine.build(
            symbol
        )


        score = 0



        # Structure weight

        if vector["structure"] in [
            "BULLISH",
            "BULLISH_BREAK"
        ]:

            score += 25


        elif vector["structure"] in [
            "BEARISH",
            "BEARISH_BREAK"
        ]:

            score -= 25



        # Regime weight

        if vector["regime"] == "TRENDING_UP":

            score += 25


        elif vector["regime"] == "TRENDING_DOWN":

            score -= 25



        # Liquidity weight

        if vector["liquidity"] == "BUY_SIDE":

            score += 15


        elif vector["liquidity"] == "SELL_SIDE":

            score -= 15



        # Confidence weight

        confidence = vector["confidence"] or 0


        score += confidence * 35



        decision = self.decision(score)



        result = {

            "symbol": symbol,

            "market_bias": vector["market_bias"],

            "confidence": confidence,

            "decision_score": round(score,2),

            "setup_quality": vector["quality"],

            "decision_state": decision

        }



        self.save(result)



        return result



    def decision(self,score):


        if score >= 70:

            return "STRONG_LONG"


        elif score >= 40:

            return "LONG_BIAS"


        elif score <= -70:

            return "STRONG_SHORT"


        elif score <= -40:

            return "SHORT_BIAS"


        return "NO_TRADE"



    def save(self,data):


        self.db.execute("""

        INSERT INTO decision_fusion

        (

        symbol,
        timestamp,
        market_bias,
        confidence,
        decision_score,
        setup_quality,
        decision_state

        )

        VALUES (?,?,?,?,?,?,?)

        """,

        (

        data["symbol"],
        int(time.time()),
        data["market_bias"],
        data["confidence"],
        data["decision_score"],
        data["setup_quality"],
        data["decision_state"]

        ))
