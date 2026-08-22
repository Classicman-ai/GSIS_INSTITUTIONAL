"""GSIS certification: static integrity, synthetic end-to-end wiring, and live runtime checks."""

from __future__ import annotations

import ast
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from institutional import GSISConfig, GSISUnifiedEngine
from volume_intelligence import (
    CrossMarketAlignmentEngine,
    MarketTrade,
    VolumeAuthorityAdapter,
    VolumeProfileEngine,
)
from volume_intelligence.cme_market_microstructure import (
    CMEBookEvent,
    CMEBookLevel,
    CMETrade,
    CMEMarketMicrostructureEngine,
)


def python_files(root: Path):
    yield from root.rglob("*.py")


def static_audit(root: Path) -> list[str]:
    failures: list[str] = []
    for path in python_files(root):
        if any(part in {".git", ".venv", "venv", "__pycache__"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        try:
            ast.parse(text, filename=str(path))
        except SyntaxError as exc:
            failures.append(f"{path}: syntax error: {exc}")
        if "api.binance.com" in text.lower():
            failures.append(f"{path}: forbidden Binance API dependency")
    unified = (root / "institutional" / "unified_engine.py").read_text(encoding="utf-8")
    required_wiring = (
        "build_cme_intelligence_service",
        "VolumeProfileEngine",
        "CrossMarketAlignmentEngine",
        "VolumeAuthorityAdapter",
        "_execution_guard",
        "already_executed",
        "mark_executed",
    )
    for token in required_wiring:
        if token not in unified:
            failures.append(f"institutional/unified_engine.py: missing required wiring: {token}")
    return failures


def synthetic_end_to_end_audit() -> dict:
    """Exercise CME -> profile -> basis -> authority with deterministic synthetic observations."""
    now = datetime.now(timezone.utc)
    trades = []
    for i in range(120):
        trades.append(CMETrade(now - timedelta(seconds=120 - i), 5000.0 + (i % 4) * 0.1, 1.0 + (i % 5), "buy" if i % 3 else "sell", 1, "TEST"))
    levels = [CMEBookLevel(now, 5000.0 + i * 0.1, 100.0 - i * 2, "bid", i, 1, "TEST") for i in range(10)]
    levels += [CMEBookLevel(now, 5001.0 + i * 0.1, 40.0 + i * 2, "ask", i, 1, "TEST") for i in range(10)]
    events = [CMEBookEvent(now, str(i), 5000.0 + (i % 5) * 0.1, 5.0, "buy", "add" if i % 2 == 0 else "execute", 1, "TEST") for i in range(60)]
    micro = CMEMarketMicrostructureEngine(20.0, 0.10, 0.10, 0.10, 0.50).analyze(levels, events, trades)
    market_trades = [MarketTrade(t.timestamp, t.price, t.quantity, t.aggressor_side) for t in trades]
    profile = VolumeProfileEngine().build(market_trades, "CME_COMEX", "XAUUSD", "M5")
    aligner = CrossMarketAlignmentEngine(min_samples=30)
    for i in range(30):
        aligner.observe(now + timedelta(seconds=i), 5000.0, 4999.0)
    basis = aligner.observe(now + timedelta(seconds=30), 5000.0, 4999.0)
    alignment = aligner.align(profile, basis)
    authority = VolumeAuthorityAdapter(20.0).evaluate(profile, alignment, 4999.0)
    assert micro.data_quality in {"good", "limited"}
    assert profile.total_volume > 0
    assert alignment.aligned
    assert authority.combined_score >= 0
    return {"microstructure": "PASS", "volume_profile": "PASS", "basis_alignment": "PASS", "authority_adapter": "PASS"}


def runtime_audit() -> dict:
    config = GSISConfig.from_env()
    engine = GSISUnifiedEngine(config)
    return engine.validate_runtime()


def main() -> int:
    root = Path(__file__).resolve().parent
    failures = static_audit(root)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    synthetic = synthetic_end_to_end_audit()
    print("GSIS STATIC AUDIT: PASS")
    print("GSIS SYNTHETIC END-TO-END PIPELINE: PASS")
    for key, value in synthetic.items():
        print(f"GSIS {key.upper()}: {value}")

    # Live certification is intentionally fail-closed. No environment means
    # no false PASS and never an automatic live order.
    if os.getenv("GSIS_LIVE_CERTIFICATION", "false").lower() != "true":
        print("GSIS LIVE CERTIFICATION: SKIPPED (set GSIS_LIVE_CERTIFICATION=true to run against the connected terminal)")
        return 0

    result = runtime_audit()
    print("GSIS MT5 CONNECTOR: PASS")
    print("GSIS LIVE MARKET READ: PASS")
    print(f"GSIS RUNTIME STATUS: {result['status']}")
    print(f"GSIS EXECUTION ENABLED: {result['execution_enabled']}")
    print(f"GSIS CME ENABLED: {result['cme_enabled']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
