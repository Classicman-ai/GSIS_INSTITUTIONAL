"""Compatibility facade for the canonical GSIS order-flow engine.

The former standalone infinite loop and local JSON market-data reader have
been removed. The unified runtime owns scheduling and receives broker data
through MT5_UNIVERSAL_CONNECTOR.
"""

from institutional.unified_engine import UnifiedOrderFlowEngine


class OrderFlowEngine(UnifiedOrderFlowEngine):
    pass
