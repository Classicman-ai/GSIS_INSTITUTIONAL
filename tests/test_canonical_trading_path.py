"""Hard guardrails for the single canonical GSIS trading path."""

import ast
from pathlib import Path

from intelligence.canonical_trade_signal import CanonicalTradeSignal
from intelligence.decision_governor_engine import DecisionGovernorEngine
from institutional.unified_engine import UnifiedRiskEngine


ROOT = Path(__file__).resolve().parents[1]


def test_canonical_signal_contract_is_complete():
    signal = CanonicalTradeSignal(
        signal_id="TEST:M5:1",
        symbol="TEST",
        timeframe="M5",
        decision="BUY",
        confidence=1.0,
        entry=100.0,
        stop_loss=99.0,
        take_profits=[103.0],
        risk_fraction=0.01,
    )
    assert signal.is_trade
    assert signal.entry == 100.0
    assert signal.stop_loss == 99.0
    assert signal.take_profits == [103.0]
    assert signal.risk_fraction == 0.01


def test_decision_governor_is_the_signal_authority():
    governor = DecisionGovernorEngine()
    signal = governor.evaluate(
        intelligence={
            "symbol": "TEST",
            "direction": "BUY",
            "confidence": 2.0,
            "pattern_match": 2.0,
            "governor_thresholds": {
                "confidence": 1.0,
                "pattern": 1.0,
                "approval": 1.0,
                "confidence_weight": 0.5,
                "pattern_weight": 0.5,
            },
        },
        risk={"approved": True, "state": "PRE_RISK_APPROVED"},
        market={"symbol": "TEST", "timeframe": "M5"},
        trade_plan={
            "signal_id": "TEST:M5:1",
            "symbol": "TEST",
            "timeframe": "M5",
            "entry": 100.0,
            "stop_loss": 99.0,
            "take_profits": [103.0],
            "risk_fraction": 0.01,
        },
    )
    assert isinstance(signal, CanonicalTradeSignal)
    assert signal.decision == "BUY"


def test_risk_consumes_and_updates_canonical_signal():
    signal = CanonicalTradeSignal(
        signal_id="TEST:M5:2",
        symbol="TEST",
        timeframe="M5",
        decision="BUY",
        confidence=1.0,
        entry=100.0,
        stop_loss=99.0,
        take_profits=[103.0],
        risk_fraction=0.01,
    )
    result = UnifiedRiskEngine().size(
        signal,
        {"equity": 10000.0},
        {
            "trade_tick_size": 1.0,
            "trade_tick_value": 10.0,
            "volume_min": 0.01,
            "volume_max": 10.0,
            "volume_step": 0.01,
        },
    )
    assert result is signal
    assert signal.position_size == 0.01
    assert signal.risk_state == "APPROVED"


def test_unified_cycle_cannot_bypass_canonical_path():
    source = (ROOT / "institutional" / "unified_engine.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    cycle = next(
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "cycle"
    )
    cycle_source = ast.get_source_segment(source, cycle) or ""

    required = [
        "self.governor.evaluate",
        "self.risk.size",
        "self.market.execute_signal",
        "canonical_signal",
    ]
    for token in required:
        assert token in cycle_source, f"canonical path missing: {token}"

    forbidden = [
        "_direction_score(",
        "self.market.execute(",
        "decision = direction",
    ]
    for token in forbidden:
        assert token not in cycle_source, f"bypass detected: {token}"
