from __future__ import annotations

from collections import deque
from datetime import datetime
from statistics import mean, pstdev
from typing import Optional

from .models import AlignmentResult, BasisSnapshot, VolumeProfile


class CrossMarketAlignmentEngine:
    """Gate CME price-dependent levels before they can influence MT5 authority."""

    def __init__(self, max_history: int = 500, min_samples: int = 30,
                 max_abs_z_score: float = 3.0, max_basis_jump: Optional[float] = None) -> None:
        self.history: deque[float] = deque(maxlen=max_history)
        self.min_samples = min_samples
        self.max_abs_z_score = max_abs_z_score
        self.max_basis_jump = max_basis_jump

    def observe(self, timestamp: datetime, cme_price: float, mt5_price: float) -> BasisSnapshot:
        if cme_price <= 0 or mt5_price <= 0:
            raise ValueError("prices must be > 0")

        basis = cme_price - mt5_price
        previous = self.history[-1] if self.history else None
        jump_invalid = (
            self.max_basis_jump is not None
            and previous is not None
            and abs(basis - previous) > self.max_basis_jump
        )
        self.history.append(basis)
        mu = mean(self.history)
        sigma = pstdev(self.history) if len(self.history) > 1 else None
        z = (basis - mu) / sigma if sigma and sigma > 0 else None
        stable = (
            len(self.history) >= self.min_samples
            and not jump_invalid
            and (z is None or abs(z) <= self.max_abs_z_score)
        )
        return BasisSnapshot(timestamp, cme_price, mt5_price, basis, mu, sigma, z,
                             stable, len(self.history))

    def align(self, profile: VolumeProfile, snapshot: BasisSnapshot) -> AlignmentResult:
        if snapshot.sample_count < self.min_samples:
            return AlignmentResult(False, "INSUFFICIENT_BASIS_HISTORY",
                f"Need {self.min_samples} observations; have {snapshot.sample_count}.",
                snapshot.basis, snapshot.z_score, None, None, None, [], [], 0.0)
        if not snapshot.stable:
            return AlignmentResult(False, "BASIS_UNSTABLE",
                "CME-MT5 basis is outside the configured stability regime.",
                snapshot.basis, snapshot.z_score, None, None, None, [], [], 0.0)

        confidence = 1.0
        if snapshot.z_score is not None:
            confidence = max(0.0, min(1.0, 1.0 - abs(snapshot.z_score) / self.max_abs_z_score))
        offset = snapshot.basis
        # CME = MT5 + basis, therefore MT5-equivalent = CME - basis.
        translate = lambda value: None if value is None else value - offset
        return AlignmentResult(True, "ALIGNED", "CME-MT5 basis is statistically stable.",
            snapshot.basis, snapshot.z_score,
            translate(profile.poc), translate(profile.vah), translate(profile.val),
            [x - offset for x in profile.hvn],
            [x - offset for x in profile.lvn], confidence)
