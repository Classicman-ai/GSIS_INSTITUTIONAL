"""GSIS risk compatibility view.

The live runtime is the sole authority for risk. These values mirror the
same environment variables consumed by institutional.unified_engine and do
not contain a second hard-coded risk policy.
"""

import os


def _float(name: str, default: str) -> float:
    return float(os.getenv(name, default))


def _int(name: str, default: str) -> int:
    return int(os.getenv(name, default))


def _bool(name: str, default: str) -> bool:
    return os.getenv(name, default).strip().lower() == "true"


TRADING_MODE = os.getenv("GSIS_TRADING_MODE", "SWING")
MAX_RISK_PER_TRADE = _float("GSIS_RISK_PER_TRADE", "0.01")
MIN_RISK_REWARD = _float("GSIS_MIN_RISK_REWARD", "2")
MAX_RISK_REWARD = _float("GSIS_MAX_RISK_REWARD", "10")

TP_LEVELS = {
    "TP1": {"rr": _float("GSIS_TP1_RR", "2"), "close_percent": _float("GSIS_TP1_CLOSE_PERCENT", "30")},
    "TP2": {"rr": _float("GSIS_TP2_RR", "5"), "close_percent": _float("GSIS_TP2_CLOSE_PERCENT", "30")},
    "TP3": {"rr": _float("GSIS_TP3_RR", "8"), "close_percent": _float("GSIS_TP3_CLOSE_PERCENT", "25")},
    "TP4": {"rr": _float("GSIS_TP4_RR", "10"), "close_percent": _float("GSIS_TP4_CLOSE_PERCENT", "15")},
}

MOVE_TO_BREAK_EVEN_AFTER = os.getenv("GSIS_BREAK_EVEN_AFTER", "TP1")
ENABLE_TRAILING_STOP = _bool("GSIS_ENABLE_TRAILING_STOP", "true")
MAX_OPEN_TRADES = _int("GSIS_MAX_OPEN_TRADES", "3")
ALLOW_PARTIAL_CLOSE = _bool("GSIS_ALLOW_PARTIAL_CLOSE", "true")
ALLOW_MULTIPLE_POSITIONS = _bool("GSIS_ALLOW_MULTIPLE_POSITIONS", "false")
