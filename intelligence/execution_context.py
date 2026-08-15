"""
=========================================================
GSIS INSTITUTIONAL

EXECUTION CONTEXT

Version: 1.0

Shared execution object used by all execution engines.

=========================================================
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ExecutionContext:

    # Market
    asset: str = ""
    signal: str = "NONE"
    timestamp: str = field(
        default_factory=lambda: str(datetime.utcnow())
    )

    # Market State
    price: float = 0.0
    spread: float = 0.0
    volatility: str = "UNKNOWN"
    liquidity: str = "UNKNOWN"
    order_flow: str = "UNKNOWN"

    # Intelligence
    risk_score: float = 0.0
    liquidity_score: float = 0.0
    impact_score: float = 0.0
    confidence: float = 0.0

    # Execution
    execution_mode: str = "NONE"
    routing: str = ""
    broker: str = ""
    order_type: str = ""
    position_size: float = 0.0

    # Final Decision
    approved: bool = False
    decision: str = "WAIT"

    # Audit Trail
    history: list = field(default_factory=list)

    def log(self, source, message):

        self.history.append({

            "time": str(datetime.utcnow()),

            "source": source,

            "message": message

        })

    def summary(self):

        return {

            "asset": self.asset,

            "signal": self.signal,

            "price": self.price,

            "risk_score": self.risk_score,

            "liquidity_score": self.liquidity_score,

            "impact_score": self.impact_score,

            "confidence": self.confidence,

            "decision": self.decision,

            "approved": self.approved

        }
