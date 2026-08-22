"""Compatibility view of the canonical GSIS runtime risk configuration.

No independent risk values are defined here. The environment is the single
source of truth used by institutional.unified_engine.
"""

import os


def _required_float(name: str) -> float:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing canonical runtime risk configuration: {name}")
    return float(value)


def _required_int(name: str) -> int:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing canonical runtime risk configuration: {name}")
    return int(value)


def _required_bool(name: str) -> bool:
    value = os.getenv(name, "").strip().lower()
    if value not in {"true", "false"}:
        raise RuntimeError(f"Missing/invalid canonical runtime risk configuration: {name}")
    return value == "true"


TRADING_MODE = os.getenv("GSIS_TRADING_MODE", "SWING")
MAX_RISK_PER_TRADE = _required_float("GSIS_RISK_PER_TRADE")
MIN_RISK_REWARD = _required_float("GSIS_MIN_RISK_REWARD")
MAX_RISK_REWARD = _required_float("GSIS_MAX_RISK_REWARD")
TP_LEVELS = {
    "TP1": {"rr": _required_float("GSIS_TP1_RR"), "close_percent": _required_float("GSIS_TP1_CLOSE_PERCENT")},
    "TP2": {"rr": _required_float("GSIS_TP2_RR"), "close_percent": _required_float("GSIS_TP2_CLOSE_PERCENT")},
    "TP3": {"rr": _required_float("GSIS_TP3_RR"), "close_percent": _required_float("GSIS_TP3_CLOSE_PERCENT")},
    "TP4": {"rr": _required_float("GSIS_TP4_RR"), "close_percent": _required_float("GSIS_TP4_CLOSE_PERCENT")},
}
MOVE_TO_BREAK_EVEN_AFTER = os.getenv("GSIS_BREAK_EVEN_AFTER", "TP1")
ENABLE_TRAILING_STOP = _required_bool("GSIS_ENABLE_TRAILING_STOP")
MAX_OPEN_TRADES = _required_int("GSIS_MAX_OPEN_TRADES")
ALLOW_PARTIAL_CLOSE = _required_bool("GSIS_ALLOW_PARTIAL_CLOSE")
ALLOW_MULTIPLE_POSITIONS = _required_bool("GSIS_ALLOW_MULTIPLE_POSITIONS")
