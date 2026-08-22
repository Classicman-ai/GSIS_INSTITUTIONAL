"""Compatibility execution configuration loaded entirely from the environment."""

import os


def required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required execution configuration: {name}")
    return value


EXECUTION_MODE = required("GSIS_EXECUTION_MODE")
EXECUTION_ENABLED = required("GSIS_EXECUTION_ENABLED").lower() == "true"
DEFAULT_ORDER_TYPE = required("GSIS_ORDER_TYPE")
ALLOW_LONG = required("GSIS_ALLOW_LONG").lower() == "true"
ALLOW_SHORT = required("GSIS_ALLOW_SHORT").lower() == "true"
MAX_OPEN_TRADES = int(required("GSIS_MAX_OPEN_TRADES"))
MAX_PENDING_ORDERS = int(required("GSIS_MAX_PENDING_ORDERS"))
SLIPPAGE = float(required("GSIS_SLIPPAGE"))
COMMISSION = float(required("GSIS_COMMISSION"))
ENABLE_BREAK_EVEN = required("GSIS_ENABLE_BREAK_EVEN").lower() == "true"
ENABLE_TRAILING_STOP = required("GSIS_ENABLE_TRAILING_STOP").lower() == "true"
BREAK_EVEN_AFTER = required("GSIS_BREAK_EVEN_AFTER")
TRAIL_AFTER = required("GSIS_TRAIL_AFTER")
TIMEOUT_SECONDS = float(required("GSIS_EXECUTION_TIMEOUT_SECONDS"))
RETRY_COUNT = int(required("GSIS_EXECUTION_RETRY_COUNT"))
SAVE_EXECUTION_LOG = required("GSIS_SAVE_EXECUTION_LOG").lower() == "true"
SAVE_TRADE_HISTORY = required("GSIS_SAVE_TRADE_HISTORY").lower() == "true"
