"""GSIS Institutional Volume Intelligence.

Category A: price-independent CME volume intelligence.
Category B: price-dependent CME-to-MT5 intelligence gated by basis stability.
CME microstructure is explicitly separate from the existing MT5 Order Flow Engine.
"""

from .models import BasisSnapshot, VolumeProfile, VolumeProfileLevel, MarketTrade
from .profile_engine import VolumeProfileEngine
from .alignment_engine import CrossMarketAlignmentEngine
from .authority_adapter import VolumeAuthorityAdapter, VolumeAuthoritySignal
from .cme_market_microstructure import (
    CMEBookEvent,
    CMEBookLevel,
    CMETrade,
    CMEMarketMicrostructureEngine,
    CMEMicrostructureSignal,
)

__all__ = [
    "BasisSnapshot",
    "VolumeProfile",
    "VolumeProfileLevel",
    "MarketTrade",
    "VolumeProfileEngine",
    "CrossMarketAlignmentEngine",
    "VolumeAuthorityAdapter",
    "VolumeAuthoritySignal",
    "CMEBookEvent",
    "CMEBookLevel",
    "CMETrade",
    "CMEMarketMicrostructureEngine",
    "CMEMicrostructureSignal",
]
