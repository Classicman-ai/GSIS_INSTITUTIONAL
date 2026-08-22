"""Canonical trade signal contract shared by decision, planning, risk, execution and notification."""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class CanonicalTradeSignal:
    """The single authoritative GSIS trade object."""

    signal_id: str
    symbol: str
    timeframe: str
    decision: str
    confidence: float
    reasoning: List[str] = field(default_factory=list)
    entry: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profits: List[float] = field(default_factory=list)
    risk_fraction: Optional[float] = None
    position_size: Optional[float] = None
    risk_state: str = "PENDING"
    execution_status: str = "PENDING"
    invalidation: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self) -> None:
        self.decision = str(self.decision).upper()
        if self.decision not in {"BUY", "SELL", "WAIT"}:
            raise ValueError("decision must be BUY, SELL, or WAIT")
        if not self.signal_id:
            raise ValueError("signal_id is required")
        if not self.symbol:
            raise ValueError("symbol is required")
        if not self.timeframe:
            raise ValueError("timeframe is required")
        if self.decision in {"BUY", "SELL"}:
            if self.entry is None or self.stop_loss is None:
                raise ValueError("approved trade signals require entry and stop_loss")
            if not self.take_profits:
                raise ValueError("approved trade signals require at least one take profit")

    @property
    def is_trade(self) -> bool:
        return self.decision in {"BUY", "SELL"}

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
