"""Broker-neutral symbol resolution contract for the MT5 Universal Connector.

GSIS works with canonical instrument identities (for example, ``GOLD``).
The external MT5 Universal Connector is responsible for discovering the
broker's actual tradable symbol and returning validated metadata.

This module intentionally contains no broker names, symbol aliases, prices,
or market assumptions. It is a contract/helper, not a trading engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Protocol


@dataclass(frozen=True)
class ResolvedBrokerSymbol:
    """Validated broker-side representation of a canonical instrument."""

    canonical_instrument: str
    broker_symbol: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.canonical_instrument.strip():
            raise ValueError("canonical_instrument is required")
        if not self.broker_symbol.strip():
            raise ValueError("broker_symbol is required")


class BrokerSymbolResolver(Protocol):
    """Interface the MT5 Universal Connector must expose."""

    def discover_symbols(self) -> Iterable[Mapping[str, Any]]:
        """Return the connected broker's currently available MT5 symbols."""
        ...

    def resolve_symbol(self, canonical_instrument: str) -> ResolvedBrokerSymbol:
        """Resolve and validate a canonical instrument against broker symbols."""
        ...


def validate_resolution(result: ResolvedBrokerSymbol) -> ResolvedBrokerSymbol:
    """Fail closed if the connector returns an incomplete resolution."""
    if not result.canonical_instrument.strip():
        raise ValueError("EMPTY_CANONICAL_INSTRUMENT")
    if not result.broker_symbol.strip():
        raise ValueError("EMPTY_BROKER_SYMBOL")
    return result
