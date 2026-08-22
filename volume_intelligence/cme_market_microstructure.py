from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Literal


CMESide = Literal["buy", "sell", "unknown"]
CMEBookSide = Literal["bid", "ask"]
CMEBookAction = Literal["add", "modify", "cancel", "execute"]


@dataclass(frozen=True)
class CMETrade:
    """Normalized external CME execution; produced by a data adapter."""

    timestamp: datetime
    price: float
    quantity: float
    aggressor_side: CMESide
    instrument_id: int
    source: str


@dataclass(frozen=True)
class CMEBookLevel:
    """Normalized external CME MBP-10 level."""

    timestamp: datetime
    price: float
    quantity: float
    side: CMEBookSide
    depth: int
    instrument_id: int
    source: str


@dataclass(frozen=True)
class CMEBookEvent:
    """Normalized external CME MBO event."""

    timestamp: datetime
    order_id: str
    price: float
    quantity: float
    side: CMESide
    action: CMEBookAction
    instrument_id: int
    source: str


@dataclass(frozen=True)
class CMEMicrostructureSignal:
    source: str
    score: float
    direction: Literal["bullish", "bearish", "neutral"]
    depth_imbalance: float
    additions: float
    cancellations: float
    executions: float
    trade_buy_volume: float
    trade_sell_volume: float
    trade_delta_ratio: float
    replenishment_score: float
    absorption_score: float
    liquidity_withdrawal_score: float
    confidence: float
    data_quality: str
    reasons: tuple[str, ...]


class CMEMarketMicrostructureEngine:
    """
    CME/COMEX-specific intelligence calculator.

    IMPORTANT: this engine contains no market data and no feed connection.
    Every observation must arrive from an external CME data adapter.
    """

    SOURCE = "CME_COMEX"

    def __init__(
        self,
        max_score: float,
        depth_imbalance_threshold: float,
        delta_ratio_threshold: float,
        absorption_threshold: float,
        withdrawal_threshold: float,
    ) -> None:
        if max_score <= 0:
            raise ValueError("max_score must be > 0")
        for name, value in (
            ("depth_imbalance_threshold", depth_imbalance_threshold),
            ("delta_ratio_threshold", delta_ratio_threshold),
            ("absorption_threshold", absorption_threshold),
            ("withdrawal_threshold", withdrawal_threshold),
        ):
            if not 0 < value <= 1:
                raise ValueError(f"{name} must be in (0, 1]")
        self.max_score = max_score
        self.depth_imbalance_threshold = depth_imbalance_threshold
        self.delta_ratio_threshold = delta_ratio_threshold
        self.absorption_threshold = absorption_threshold
        self.withdrawal_threshold = withdrawal_threshold

    @staticmethod
    def depth_imbalance(levels: Iterable[CMEBookLevel]) -> float:
        bids = sum(x.quantity for x in levels if x.side == "bid")
        asks = sum(x.quantity for x in levels if x.side == "ask")
        total = bids + asks
        return (bids - asks) / total if total else 0.0

    def analyze(
        self,
        levels: Iterable[CMEBookLevel],
        events: Iterable[CMEBookEvent],
        trades: Iterable[CMETrade],
    ) -> CMEMicrostructureSignal:
        levels = list(levels)
        events = list(events)
        trades = list(trades)
        if not levels and not events and not trades:
            raise ValueError("no external CME observations supplied")

        imbalance = self.depth_imbalance(levels)
        additions = sum(x.quantity for x in events if x.action == "add")
        cancellations = sum(x.quantity for x in events if x.action == "cancel")
        executions = sum(x.quantity for x in events if x.action == "execute")
        buy_volume = sum(x.quantity for x in trades if x.aggressor_side == "buy")
        sell_volume = sum(x.quantity for x in trades if x.aggressor_side == "sell")
        total_traded = buy_volume + sell_volume
        delta_ratio = (buy_volume - sell_volume) / total_traded if total_traded else 0.0

        executed_by_price: dict[tuple[str, float], float] = {}
        added_by_price: dict[tuple[str, float], float] = {}
        for event in events:
            key = (event.side, event.price)
            if event.action == "execute":
                executed_by_price[key] = executed_by_price.get(key, 0.0) + event.quantity
            elif event.action == "add":
                added_by_price[key] = added_by_price.get(key, 0.0) + event.quantity

        replenishment_raw = sum(
            min(executed_by_price[key], added_by_price.get(key, 0.0))
            for key in executed_by_price
        )
        replenishment_score = replenishment_raw / executions if executions else 0.0
        replenishment_score = min(1.0, replenishment_score)
        absorption_score = replenishment_score if executions > 0 else 0.0
        withdrawal_score = min(1.0, cancellations / additions) if additions else 0.0

        score = 0.0
        reasons: list[str] = []
        if imbalance >= self.depth_imbalance_threshold:
            score += self.max_score * 0.25
            reasons.append("CME displayed depth is bid-heavy.")
        elif imbalance <= -self.depth_imbalance_threshold:
            score -= self.max_score * 0.25
            reasons.append("CME displayed depth is ask-heavy.")
        else:
            reasons.append("CME displayed depth is balanced.")

        if delta_ratio >= self.delta_ratio_threshold:
            score += self.max_score * 0.25
            reasons.append("CME executed trade flow confirms buyer aggression.")
        elif delta_ratio <= -self.delta_ratio_threshold:
            score -= self.max_score * 0.25
            reasons.append("CME executed trade flow confirms seller aggression.")
        else:
            reasons.append("CME executed trade flow is balanced or unavailable.")

        if absorption_score >= self.absorption_threshold:
            reasons.append("CME MBO executions followed by replenishment indicate possible absorption.")
            score += self.max_score * 0.10 if imbalance >= 0 else -self.max_score * 0.10

        if withdrawal_score >= self.withdrawal_threshold:
            reasons.append("CME MBO cancellation/addition ratio indicates liquidity withdrawal.")
            score += self.max_score * 0.10 if imbalance >= 0 else -self.max_score * 0.10

        score = max(-self.max_score, min(self.max_score, score))
        direction = "bullish" if score > self.max_score * 0.10 else "bearish" if score < -self.max_score * 0.10 else "neutral"

        depth_quality = min(1.0, len(levels) / 10.0)
        event_quality = min(1.0, len(events) / 50.0)
        trade_quality = min(1.0, len(trades) / 50.0)
        confidence = round(depth_quality * 0.30 + event_quality * 0.40 + trade_quality * 0.30, 6)
        quality = "good" if confidence >= 0.80 else "limited" if confidence > 0 else "unavailable"

        return CMEMicrostructureSignal(
            source=self.SOURCE,
            score=round(score, 6),
            direction=direction,
            depth_imbalance=round(imbalance, 8),
            additions=additions,
            cancellations=cancellations,
            executions=executions,
            trade_buy_volume=buy_volume,
            trade_sell_volume=sell_volume,
            trade_delta_ratio=round(delta_ratio, 8),
            replenishment_score=round(replenishment_score, 8),
            absorption_score=round(absorption_score, 8),
            liquidity_withdrawal_score=round(withdrawal_score, 8),
            confidence=confidence,
            data_quality=quality,
            reasons=tuple(reasons),
        )
