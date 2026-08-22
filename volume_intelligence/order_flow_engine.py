from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Literal


BookSide = Literal["bid", "ask"]
MBOAction = Literal["add", "modify", "cancel", "execute"]


@dataclass(frozen=True)
class OrderBookLevel:
    price: float
    quantity: float
    side: BookSide

    def __post_init__(self) -> None:
        if self.price <= 0 or self.quantity < 0:
            raise ValueError("order-book price must be > 0 and quantity >= 0")


@dataclass(frozen=True)
class MBOEvent:
    timestamp: datetime
    order_id: str
    price: float
    quantity: float
    side: BookSide
    action: MBOAction

    def __post_init__(self) -> None:
        if not self.order_id:
            raise ValueError("order_id is required")
        if self.price <= 0 or self.quantity < 0:
            raise ValueError("MBO price must be > 0 and quantity >= 0")


@dataclass(frozen=True)
class OrderFlowSignal:
    """Exchange order-book intelligence; no synthetic flow is generated."""
    score: float
    direction: Literal["bullish", "bearish", "neutral"]
    dom_imbalance: float
    additions: float
    cancellations: float
    executions: float
    replenishment_score: float
    absorption_score: float
    exhaustion_score: float
    liquidity_withdrawal_score: float
    confidence: float
    data_quality: str
    reasons: list[str]


class OrderFlowIntelligenceEngine:
    """
    Analyze CME MBP-10/MBO data when supplied by an upstream exchange feed.

    MBP-10 is treated as displayed depth. MBO is treated as order-level book
    events. Executed trades should remain the source of realized trade flow;
    this engine never invents executions from resting liquidity.
    """

    def __init__(self, max_score: float = 20.0) -> None:
        if max_score <= 0:
            raise ValueError("max_score must be > 0")
        self.max_score = max_score

    @staticmethod
    def dom_imbalance(levels: Iterable[OrderBookLevel]) -> float:
        bids = sum(x.quantity for x in levels if x.side == "bid")
        asks = sum(x.quantity for x in levels if x.side == "ask")
        total = bids + asks
        return (bids - asks) / total if total else 0.0

    def analyze(
        self,
        levels: Iterable[OrderBookLevel],
        mbo_events: Iterable[MBOEvent] = (),
        trade_delta_ratio: float | None = None,
    ) -> OrderFlowSignal:
        levels = list(levels)
        events = list(mbo_events)
        imbalance = self.dom_imbalance(levels)

        additions = sum(e.quantity for e in events if e.action == "add")
        cancellations = sum(e.quantity for e in events if e.action == "cancel")
        executions = sum(e.quantity for e in events if e.action == "execute")

        # Replenishment: repeated add events at a price after executions at the
        # same price. This is a structural signal, not a claim of intent.
        executed_by_price: dict[tuple[BookSide, float], float] = {}
        added_by_price: dict[tuple[BookSide, float], float] = {}
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
        replenishment_score = min(1.0, replenishment_raw / max(executions, 1.0))

        cancellation_rate = cancellations / max(additions, 1.0)
        liquidity_withdrawal_score = min(1.0, cancellation_rate)

        # Absorption requires both executed flow and replenishment. Without
        # trade executions, resting depth alone cannot be called absorption.
        absorption_score = min(
            1.0,
            replenishment_score * (1.0 if executions > 0 else 0.0),
        )

        # Exhaustion is deliberately conservative: high cancellation/withdrawal
        # with low executions is a liquidity-quality warning, not a trade signal.
        exhaustion_score = min(
            1.0,
            liquidity_withdrawal_score * (1.0 if executions <= additions * 0.25 else 0.5),
        )

        score = 0.0
        reasons: list[str] = []

        if imbalance > 0.15:
            score += 5.0
            reasons.append("Displayed MBP depth is bid-heavy.")
        elif imbalance < -0.15:
            score -= 5.0
            reasons.append("Displayed MBP depth is ask-heavy.")
        else:
            reasons.append("Displayed MBP depth is relatively balanced.")

        if trade_delta_ratio is not None:
            if trade_delta_ratio > 0.10:
                score += 5.0
                reasons.append("Executed trade delta confirms buyer aggression.")
            elif trade_delta_ratio < -0.10:
                score -= 5.0
                reasons.append("Executed trade delta confirms seller aggression.")
            else:
                reasons.append("Executed trade delta is balanced.")
        else:
            reasons.append("Executed trade delta unavailable; no synthetic delta inferred.")

        if absorption_score >= 0.50:
            reasons.append("Order-level executions followed by replenishment indicate possible absorption.")
            score += 2.0 if imbalance >= 0 else -2.0

        if liquidity_withdrawal_score >= 0.50:
            reasons.append("High cancellation relative to additions indicates liquidity withdrawal risk.")
            score += -2.0 if imbalance < 0 else 2.0

        score = max(-self.max_score, min(self.max_score, score))
        direction = "bullish" if score > 2.0 else "bearish" if score < -2.0 else "neutral"

        sample_quality = "good" if len(levels) >= 10 and len(events) >= 50 else "limited"
        confidence = min(1.0, (len(levels) / 10.0) * 0.4 + (len(events) / 50.0) * 0.6)

        return OrderFlowSignal(
            score=round(score, 4),
            direction=direction,
            dom_imbalance=round(imbalance, 6),
            additions=additions,
            cancellations=cancellations,
            executions=executions,
            replenishment_score=round(replenishment_score, 6),
            absorption_score=round(absorption_score, 6),
            exhaustion_score=round(exhaustion_score, 6),
            liquidity_withdrawal_score=round(liquidity_withdrawal_score, 6),
            confidence=round(confidence, 6),
            data_quality=sample_quality,
            reasons=reasons,
        )
