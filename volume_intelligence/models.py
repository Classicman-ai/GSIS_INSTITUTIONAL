from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, Optional

Side = Literal["buy", "sell", "unknown"]

@dataclass(frozen=True)
class MarketTrade:
    timestamp: datetime
    price: float
    volume: float
    side: Side = "unknown"

    def __post_init__(self) -> None:
        if self.price <= 0:
            raise ValueError("price must be > 0")
        if self.volume < 0:
            raise ValueError("volume must be >= 0")

@dataclass(frozen=True)
class VolumeProfileLevel:
    price: float
    total_volume: float
    buy_volume: float
    sell_volume: float

    @property
    def delta(self) -> float:
        return self.buy_volume - self.sell_volume

@dataclass
class VolumeProfile:
    source: str
    symbol: str
    timeframe: str
    levels: list[VolumeProfileLevel]
    poc: Optional[float] = None
    vah: Optional[float] = None
    val: Optional[float] = None
    hvn: list[float] = field(default_factory=list)
    lvn: list[float] = field(default_factory=list)
    total_volume: float = 0.0
    buy_volume: float = 0.0
    sell_volume: float = 0.0
    cumulative_delta: float = 0.0
    value_area_volume_fraction: float = 0.70
    quality: str = "unknown"

    @property
    def net_delta(self) -> float:
        return self.buy_volume - self.sell_volume

@dataclass(frozen=True)
class BasisSnapshot:
    timestamp: datetime
    cme_price: float
    mt5_price: float
    basis: float
    mean_basis: Optional[float]
    basis_std: Optional[float]
    z_score: Optional[float]
    stable: bool
    sample_count: int

@dataclass(frozen=True)
class AlignmentResult:
    aligned: bool
    status: str
    reason: str
    basis: Optional[float]
    basis_z_score: Optional[float]
    translated_poc: Optional[float]
    translated_vah: Optional[float]
    translated_val: Optional[float]
    translated_hvn: list[float]
    translated_lvn: list[float]
    confidence: float

@dataclass(frozen=True)
class VolumeAuthoritySignal:
    price_independent_score: float
    price_dependent_score: float
    price_dependent_enabled: bool
    combined_score: float
    direction: Literal["bullish", "bearish", "neutral"]
    reasons: list[str]
    data_quality: str
