from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .models import AlignmentResult, VolumeProfile


@dataclass(frozen=True)
class VolumeAuthoritySignal:
    """Bounded Volume Intelligence contribution to GSIS authority."""
    price_independent_score: float
    price_dependent_score: float
    price_dependent_enabled: bool
    combined_score: float
    direction: Literal["bullish", "bearish", "neutral"]
    reasons: list[str]
    data_quality: str


class VolumeAuthorityAdapter:
    """Convert volume intelligence into an advisory authority contribution."""

    def __init__(self, max_score: float = 20.0) -> None:
        if max_score <= 0:
            raise ValueError("max_score must be > 0")
        self.max_score = max_score

    def evaluate(self, profile: VolumeProfile, alignment: AlignmentResult | None = None,
                 mt5_price: float | None = None) -> VolumeAuthoritySignal:
        reasons: list[str] = []
        total = profile.buy_volume + profile.sell_volume
        delta_ratio = profile.net_delta / total if total else 0.0
        independent = 0.0

        if delta_ratio > 0.10:
            independent += 7.0
            direction = "bullish"
            reasons.append("Positive CME trade delta indicates buyer aggression.")
        elif delta_ratio < -0.10:
            independent += 7.0
            direction = "bearish"
            reasons.append("Negative CME trade delta indicates seller aggression.")
        else:
            direction = "neutral"
            reasons.append("CME delta is balanced; no strong directional participation.")

        independent += 3.0 if profile.quality == "good" else 1.0
        reasons.append(
            "Volume profile has sufficient trade observations."
            if profile.quality == "good"
            else "Volume profile is based on limited observations."
        )
        independent = min(independent, self.max_score * 0.50)

        dependent = 0.0
        enabled = bool(alignment and alignment.aligned and mt5_price is not None)
        if enabled:
            if alignment.translated_val is not None and alignment.translated_vah is not None:
                if alignment.translated_val <= mt5_price <= alignment.translated_vah:
                    dependent += 4.0
                    reasons.append("MT5 price is inside translated CME value area.")
                elif mt5_price > alignment.translated_vah:
                    reasons.append("MT5 price is above translated CME value area.")
                else:
                    reasons.append("MT5 price is below translated CME value area.")
            if alignment.translated_poc is not None and abs(mt5_price - alignment.translated_poc) <= 2.0:
                dependent += 2.0
                reasons.append("MT5 price is near translated CME POC.")
            dependent *= alignment.confidence
        else:
            reasons.append(
                "CME price-dependent levels DISABLED because cross-market alignment is not valid."
            )

        combined = min(self.max_score, independent + dependent)
        final_direction = direction if direction != "neutral" and combined >= self.max_score * 0.50 else "neutral"
        return VolumeAuthoritySignal(
            round(independent, 4), round(dependent, 4), enabled,
            round(combined, 4), final_direction, reasons,
            "aligned" if enabled else "price-independent-only",
        )
