"""GSIS Institutional Volume Intelligence.

Two-category model:
1. Price-independent CME/market volume intelligence.
2. Price-dependent CME-to-MT5 translated intelligence gated by basis stability.
"""

from .models import BasisSnapshot, VolumeProfile, VolumeProfileLevel, MarketTrade
from .profile_engine import VolumeProfileEngine
from .alignment_engine import CrossMarketAlignmentEngine
from .authority_adapter import VolumeAuthorityAdapter, VolumeAuthoritySignal

__all__ = [
    "BasisSnapshot",
    "VolumeProfile",
    "VolumeProfileLevel",
    "MarketTrade",
    "VolumeProfileEngine",
    "CrossMarketAlignmentEngine",
    "VolumeAuthorityAdapter",
    "VolumeAuthoritySignal",
]
