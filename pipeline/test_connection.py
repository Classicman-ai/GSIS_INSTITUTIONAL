from core.engine_registry import EngineRegistry
from engines.adapters.regime_adapter import RegimeAdapter


print("===================================")
print("GSIS ENGINE CONNECTION TEST")
print("===================================")


registry = EngineRegistry()


regime = RegimeAdapter()


registry.register(regime)


registry.start_all()


print("-----------------------------------")

print(
    registry.status()
)

print("-----------------------------------")
print("CONNECTION TEST COMPLETE")
