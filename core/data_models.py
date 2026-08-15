from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class GSISContext:

    symbol: str

    timestamp: str = field(
        default_factory=lambda:
        datetime.now(timezone.utc).isoformat()
    )

    market: dict = None
    volume: dict = None
    flow: dict = None
    regime: dict = None
    adaptive: dict = None

    fusion: dict = None
    signal: dict = None
    risk: dict = None
    quality: dict = None

    execution: dict = None
    journal: dict = None


    def update(self, key, value):
        setattr(self, key, value)


    def snapshot(self):

        return {
            "symbol": self.symbol,
            "timestamp": self.timestamp,
            "market": self.market,
            "volume": self.volume,
            "flow": self.flow,
            "regime": self.regime,
            "adaptive": self.adaptive,
            "fusion": self.fusion,
            "signal": self.signal,
            "risk": self.risk,
            "quality": self.quality,
            "execution": self.execution,
            "journal": self.journal
        }
