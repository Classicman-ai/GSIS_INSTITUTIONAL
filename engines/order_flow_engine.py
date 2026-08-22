"""Compatibility facade for the single canonical GSIS order-flow engine."""

from institutional.unified_engine import UnifiedOrderFlowEngine


class OrderFlowEngine(UnifiedOrderFlowEngine):
    """Canonical order-flow implementation exposed at the legacy import path."""

    pass
