"""GSIS canonical decision governor.

The governor decides BUY/SELL/WAIT from supplied live intelligence and risk
state. It does not calculate broker prices or send notifications itself.
A canonical signal is returned for both the execution and notification paths.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from intelligence.canonical_trade_signal import CanonicalTradeSignal


class DecisionGovernorEngine:
    """Single source of truth for the market decision."""

    def __init__(self):
        print("==============================")
        print("GSIS DECISION GOVERNOR ENGINE v2.0 ONLINE")
        print("CANONICAL DECISION CONTROL ACTIVE")
        print("==============================")

    def evaluate(
        self,
        intelligence: Dict[str, Any],
        risk: Optional[Dict[str, Any]] = None,
        market: Optional[Dict[str, Any]] = None,
        trade_plan: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Evaluate supplied live state and return one canonical signal.

        Thresholds are supplied through the caller/configuration rather than
        embedding market-specific values in the notification or execution path.
        """
        intelligence = intelligence or {}
        risk = risk or {}
        market = market or {}
        trade_plan = trade_plan or {}

        confidence = float(intelligence.get("confidence", 0) or 0)
        pattern_score = float(intelligence.get("pattern_match", 0) or 0)
        direction = str(
            intelligence.get("direction")
            or intelligence.get("bias")
            or "WAIT"
        ).upper()

        reasons = list(intelligence.get("reasons", []) or [])
        approval_score = 0.0

        # Governance thresholds must be supplied by configuration.
        thresholds = intelligence.get("governor_thresholds", {}) or {}
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

        signal = CanonicalTradeSignal(
            symbol=str(
                trade_plan.get("symbol")
                or market.get("symbol")
                or intelligence.get("symbol")
                or ""
            ),
            decision=decision,
            confidence=confidence,
            reasoning=reasons,
            entry=trade_plan.get("entry"),
            stop_loss=trade_plan.get("stop_loss"),
            take_profits=list(trade_plan.get("take_profits", []) or []),
            risk_state=str(risk.get("state", "APPROVED" if approved else "PENDING")),
            execution_status="READY" if approved else "BLOCKED",
            invalidation=trade_plan.get("invalidation"),
            metadata={
                "approval_score": approval_score,
                "pattern_score": pattern_score,
            },
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        result = signal.to_dict()

        print("==============================")
        print("GSIS CANONICAL GOVERNOR RESULT")
        print("==============================")
        print(result)
        return result


if __name__ == "__main__":
    print("Decision Governor requires live intelligence/configuration input.")
