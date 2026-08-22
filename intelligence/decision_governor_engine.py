"""GSIS canonical decision governor.

The governor is the only production component allowed to finalize BUY/SELL/WAIT.
It returns the single CanonicalTradeSignal consumed by risk, execution and
notification paths.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from intelligence.canonical_trade_signal import CanonicalTradeSignal


class DecisionGovernorEngine:
    """Single source of truth for the market decision."""

    def evaluate(
        self,
        intelligence: Dict[str, Any],
        risk: Optional[Dict[str, Any]] = None,
        market: Optional[Dict[str, Any]] = None,
        trade_plan: Optional[Dict[str, Any]] = None,
    ) -> CanonicalTradeSignal:
        intelligence = intelligence or {}
        risk = risk or {}
        market = market or {}
        trade_plan = trade_plan or {}

        confidence = float(intelligence.get("confidence", 0) or 0)
        pattern_score = float(intelligence.get("pattern_match", 0) or 0)
        direction = str(intelligence.get("direction") or intelligence.get("bias") or "WAIT").upper()
        reasons = list(intelligence.get("reasons", []) or [])
        thresholds = intelligence.get("governor_thresholds", {}) or {}
        approval_score = 0.0

        confidence_threshold = thresholds.get("confidence")
        pattern_threshold = thresholds.get("pattern")
        approval_threshold = thresholds.get("approval")
        if confidence_threshold is not None:
            if confidence >= float(confidence_threshold):
                approval_score += float(thresholds.get("confidence_weight", 0))
                reasons.append("CONFIDENCE ACCEPTED")
            else:
                reasons.append("LOW CONFIDENCE")
        if pattern_threshold is not None:
            if pattern_score >= float(pattern_threshold):
                approval_score += float(thresholds.get("pattern_weight", 0))
                reasons.append("PATTERN ACCEPTED")
            else:
                reasons.append("WEAK PATTERN")
        if risk.get("approved") is True:
            approval_score += float(thresholds.get("risk_weight", 0))
            reasons.append("RISK VALIDATED")
        elif risk.get("approved") is False:
            reasons.append("RISK BLOCKED")
        if market.get("liquidity_state"):
            reasons.append(f"LIQUIDITY: {market['liquidity_state']}")
        if market.get("volatility"):
            reasons.append(f"VOLATILITY: {market['volatility']}")

        if direction not in {"BUY", "SELL"}:
            direction = "WAIT"
        approved = (
            approval_threshold is not None
            and approval_score >= float(approval_threshold)
            and risk.get("approved", True) is not False
            and direction in {"BUY", "SELL"}
        )
        decision = direction if approved else "WAIT"

        return CanonicalTradeSignal(
            signal_id=str(trade_plan.get("signal_id") or ""),
            symbol=str(trade_plan.get("symbol") or market.get("symbol") or intelligence.get("symbol") or ""),
            timeframe=str(trade_plan.get("timeframe") or market.get("timeframe") or ""),
            decision=decision,
            confidence=confidence,
            reasoning=reasons,
            entry=trade_plan.get("entry") if approved else None,
            stop_loss=trade_plan.get("stop_loss") if approved else None,
            take_profits=list(trade_plan.get("take_profits", []) or []) if approved else [],
            risk_fraction=trade_plan.get("risk_fraction"),
            risk_state=str(risk.get("state", "APPROVED" if approved else "BLOCKED")),
            execution_status="READY" if approved else "BLOCKED",
            invalidation=trade_plan.get("invalidation"),
            metadata={"approval_score": approval_score, "pattern_score": pattern_score, "governor": "DecisionGovernorEngine"},
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
