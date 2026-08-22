"""Compatibility facade for the canonical GSIS order-flow engine."""

from institutional.unified_engine import UnifiedOrderFlowEngine


class OrderFlowEngine(UnifiedOrderFlowEngine):
    """All order-flow calculations are delegated to the canonical engine."""

    def run(self, context):
        rates = getattr(context, "rates", None)
        if rates is None and isinstance(context, dict):
            rates = context.get("rates")
        if rates is None:
            raise RuntimeError("Broker rates are required; order-flow cannot use synthetic data")
        return self.calculate(rates)
