"""Compatibility execution configuration.

Execution values are supplied by the canonical GSIS runtime environment.
"""

import os


EXECUTION_MODE = os.environ.get("GSIS_EXECUTION_MODE", "LIVE")
EXECUTION_ENABLED = os.environ.get("GSIS_EXECUTION_ENABLED", "false").lower() == "true"

DEFAULT_ORDER_TYPE = os.environ.get("GSIS_ORDER_TYPE", "MARKET")
ALLOW_LONG = os.environ.get("GSIS_ALLOW_LONG", "true").lower() == "true"
ALLOW_SHORT = os.environ.get("GSIS_ALLOW_SHORT", "true").lower() == "true"

MAX_OPEN_TRADES = int(os.environ["GSIS_MAX_OPEN_TRADES"])
MAX_PENDING_ORDERS = int(os.environ["GSIS_MAX_PENDING_ORDERS"])

SLIPPAGE = float(os.environ["GSIS_SLIPPAGE"])
COMMISSION = float(os.environ["GSIS_COMMISSION"])

ENABLE_BREAK_EVEN = os.environ.get("GSIS_ENABLE_BREAK_EVEN", "true").lower() == "true"
ENABLE_TRAILING_STOP = os.environ.get("GSIS_ENABLE_TRAILING_STOP", "true").lower() == "true"
BREAK_EVEN_AFTER = os.environ["GSIS_BREAK_EVEN_AFTER"]
TRAIL_AFTER = os.environ["GSIS_TRAIL_AFTER"]

TIMEOUT_SECONDS = float(os.environ["GSIS_EXECUTION_TIMEOUT_SECONDS"])
RETRY_COUNT = int(os.environ["GSIS_EXECUTION_RETRY_COUNT"])

SAVE_EXECUTION_LOG = os.environ.get("GSIS_SAVE_EXECUTION_LOG", "true").lower() == "true"
SAVE_TRADE_HISTORY = os.environ.get("GSIS_SAVE_TRADE_HISTORY", "true").lower() == "true"
