"""Compatibility access to canonical GSIS runtime configuration.

Runtime values are intentionally loaded from the environment; this module
contains no market symbols, prices, timeframes, risk values, or test data.
"""

from institutional.unified_engine import GSISConfig


def load_config() -> GSISConfig:
    return GSISConfig.from_env()
