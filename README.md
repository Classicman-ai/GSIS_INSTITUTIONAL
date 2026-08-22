# GSIS INSTITUTIONAL

## Canonical runtime

GSIS now has one production runtime: `institutional.GSISUnifiedEngine`.

The runtime flow is:

`MT5_UNIVERSAL_CONNECTOR -> live tick/candles -> unified order flow -> unified market intelligence -> risk sizing -> decision -> optional MT5 execution -> audit persistence -> repeat`

Market symbols, timeframes, loop timing, history depth, risk parameters, execution state, connector location, and database location are runtime configuration. They are not embedded in the trading code.

## Start

Set the required variables from `.env.example`, then run:

```bash
python run_gsis.py
```

## Certification

The certification harness performs a static source audit and then a live-read validation through `MT5_UNIVERSAL_CONNECTOR`:

```bash
python gsis_certification.py
```

Certification requires a reachable MT5 terminal and a valid connector path. A static pass alone is not a claim of live broker connectivity.

## Canonical compatibility policy

Legacy import paths for the order-flow engine, API gateway, and master orchestrator delegate to the canonical implementations. They do not maintain independent production logic.

The former synthetic order-flow implementation and credential-bearing Telegram backups have been removed from the active codebase.
