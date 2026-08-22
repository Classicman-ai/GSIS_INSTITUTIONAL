"""Canonical trade signal contract shared by decision, planning, execution, and notification."""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class CanonicalTradeSignal:
    symbol: str
    decision: str
    confidence: float
    reasoning: List[str] = field(default_factory=list)
    entry: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profits: List[float] = field(default_factory=list)
    risk_state: str = "PENDING"
    execution_status: str = "PENDING"
    invalidation: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self):
        self.decision = str(self.decision).upper()
        if self.decision not in {"BUY", "SELL", "WAIT"}:
            raise ValueError("decision must be BUY, SELL, or WAIT")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
