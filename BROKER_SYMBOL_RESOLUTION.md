# Broker-Neutral Symbol Resolution

GSIS INSTITUTIONAL must never depend on a broker-specific symbol name.

## Canonical contract

GSIS requests a canonical instrument identity, for example `GOLD`. The MT5 Universal Connector discovers the connected broker's symbol inventory, resolves the canonical instrument to the broker's actual tradable symbol, validates its metadata, and returns the resolution to GSIS.

```text
GSIS canonical instrument
        |
        v
MT5 Universal Connector
        |
        +--> discover broker symbols
        +--> resolve canonical instrument
        +--> validate symbol metadata
        |
        v
resolved broker symbol
        |
        v
live market data / risk / execution
```

The resolver must be broker-neutral. No IC Markets, XM, Exness, JustMarkets, MEX Atlantic, or other broker-specific symbol names are embedded in GSIS.

## Required connector boundary

The external MT5 Universal Connector should expose a capability equivalent to:

- `discover_symbols()`
- `resolve_symbol(canonical_instrument)`

The returned resolution must include the canonical instrument, the actual broker symbol, and broker-supplied metadata needed by GSIS.

## Fail-closed behavior

If the connector cannot resolve the requested canonical instrument, GSIS must stop the trading cycle for that instrument rather than guessing a symbol or falling back to a hardcoded alias.

## Certification requirement

Broker neutrality is not certified merely because no broker name appears in source code. The same GSIS build must be connected to multiple independent MT5 broker environments and demonstrate successful discovery, resolution, market-data retrieval, risk calculation, and execution without changing GSIS source code.
