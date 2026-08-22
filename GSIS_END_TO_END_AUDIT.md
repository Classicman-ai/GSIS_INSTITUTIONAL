# GSIS INSTITUTIONAL — END-TO-END AUTONOMY AUDIT

Audit date: 2026-08-22
Repository: `Classicman-ai/GSIS_INSTITUTIONAL`
Branch: `main`

## Executive result

**END-TO-END AUTONOMOUS CERTIFICATION: FAIL — NOT READY FOR AUTONOMOUS LIVE TRADING.**

The repository contains a functioning-looking canonical MT5 loop, but the canonical runtime is not yet the complete GSIS institutional system described by the architecture. The newly added CME/COMEX intelligence stack is currently separate from, and not invoked by, `institutional.GSISUnifiedEngine`.

A live end-to-end certification could not be truthfully marked PASS from repository inspection alone because it requires a live MT5 connector/account and configured CME/Databento credentials. The current certification script also contains a false-positive/false-negative design defect described below.

## Audit matrix

| Layer | Static | Runtime path | End-to-end | Status |
|---|---|---|---|---|
| Configuration | PASS | PASS when env is complete | NOT VERIFIED | AMBER |
| MT5 connector | PASS by integration contract | Requires live host | NOT LIVE-VERIFIED here | AMBER |
| Tick data | PASS by adapter path | Requires MT5 | NOT LIVE-VERIFIED | AMBER |
| Candle data | PASS by adapter path | Requires MT5 | NOT LIVE-VERIFIED | AMBER |
| MT5 order flow | PASS | Wired into canonical engine | YES structurally | PASS |
| Market intelligence | PASS | Wired | YES structurally | PASS |
| Risk sizing | PASS | Wired | YES structurally | PASS |
| Execution | PASS by call path | Broker-dependent | NOT LIVE-VERIFIED | AMBER |
| SQLite persistence | PASS | Wired | YES structurally | PASS |
| Autonomous loop | PASS | `run_forever()` | YES structurally | PASS |
| CME Databento adapter | PASS | Separate service | Not connected to canonical runtime | FAIL |
| CME microstructure | PASS | Separate service | Not connected to canonical runtime | FAIL |
| CME volume profile | PASS | Standalone engine | Not connected to canonical runtime | FAIL |
| CME↔MT5 alignment | PASS | Standalone engine | Not connected to canonical runtime | FAIL |
| Volume authority | PASS | Standalone adapter | Not connected to canonical runtime | FAIL |
| Institutional authority/governance | PARTIAL | Not in canonical cycle | Not verified | FAIL |
| Full execution controls | PARTIAL | Canonical engine bypasses compatibility config | Not verified | FAIL |
| Trade lifecycle/management | PARTIAL | Not present in canonical loop | Not verified | FAIL |
| Autonomous health/recovery | PARTIAL | Exception logging only | No health/recovery controller | FAIL |

## Critical findings

### 1. CME intelligence is not actually in the autonomous trading path — CRITICAL

The canonical runtime creates only:

`MT5UniversalConnectorAdapter -> UnifiedOrderFlowEngine -> UnifiedMarketIntelligenceEngine -> UnifiedRiskEngine -> optional MT5 execution -> SQLite`

The CME path exists separately as:

`DatabentoCMEDataSource -> CMEIntelligenceService -> CMEMarketMicrostructureEngine`

but `institutional/unified_engine.py` does not import or instantiate the CME service, volume profile engine, alignment engine, or volume authority adapter.

Therefore the system currently cannot truthfully claim that CME/COMEX intelligence participates in autonomous GSIS decisions.

### 2. The canonical runtime bypasses the existing execution configuration — HIGH

`config/execution_config.py` defines execution mode, long/short permissions, max open trades, max pending orders, slippage, commission, break-even, trailing, timeout, retry count, and trade-history controls.

The canonical `GSISUnifiedEngine` does not consume this compatibility configuration. It directly calls the MT5 connector's `buy()`/`sell()` methods when `GSIS_EXECUTION_ENABLED=true`.

This creates a governance gap between configured execution controls and the actual autonomous runtime.

### 3. Risk configuration is duplicated and inconsistent — HIGH

`config/risk_config.py` contains a legacy `MAX_RISK_PER_TRADE = 0.05` (5%), while the canonical runtime uses `GSIS_RISK_PER_TRADE` from environment configuration.

The audit must therefore treat the repository as having multiple risk authorities until one canonical risk configuration is enforced.

### 4. The canonical signal model is much simpler than the institutional architecture — HIGH

The canonical market intelligence currently derives direction mainly from first-vs-last close and a simple volume delta/ATR score.

It does not demonstrate integration of the broader institutional decision stack, including the separate volume authority, regime controls, quality gates, multi-agent coordination, confidence calibration, trade lifecycle, or other legacy institutional modules.

### 5. Autonomous error recovery is incomplete — HIGH

`run_forever()` catches exceptions, records an error in SQLite, prints the exception, waits, and retries the cycle.

That is basic retry behavior, not a full autonomous health/recovery layer. There is no demonstrated circuit breaker, connector health state machine, stale-data detector, CME feed health gate, execution reconciliation, or escalation policy in the canonical loop.

### 6. Existing certification script is not sufficient for end-to-end certification — HIGH

`gsis_certification.py` performs a static AST/pattern audit and then calls `validate_runtime()`. It prints PASS labels after the runtime call succeeds, but it does not verify:

- CME feed connectivity;
- CME data freshness;
- MBO/MBP-10/trades actually arriving;
- CME microstructure output;
- volume profile output;
- CME↔MT5 basis stability;
- volume authority reaching the decision engine;
- execution control gates;
- trade execution reconciliation;
- persistence after an actual decision/execution cycle;
- autonomous recovery from controlled failures.

Additionally, its current `buy_volume = [0-9]` / `sell_volume = [0-9]` regex is broad enough to flag legitimate initialization such as `buy_volume = 0.0` in the canonical order-flow engine. The certification logic therefore needs correction before it can be trusted.

### 7. Live certification cannot be claimed from source inspection — BLOCKER

The current `.env.example` intentionally contains placeholders for MT5 connector location, symbols, risk parameters, CME credentials, CME symbols, and CME microstructure parameters.

The repository's historical dependency audit also records that the `MetaTrader5` Python package is unavailable in the Termux/Android environment and that MT5 connectivity requires the remote bridge/compatible host architecture.

Consequently, a true autonomous certification requires execution on the actual MT5 host with the real connector and, separately, configured CME/Databento credentials.

## Required certification sequence

Before declaring GSIS autonomous, the system must pass all of the following in one controlled audit run:

1. Configuration validation.
2. MT5 connector discovery and connection.
3. Broker/account identity read.
4. Symbol discovery and metadata validation.
5. Live tick validation.
6. Multi-timeframe candle validation.
7. MT5 order-flow calculation.
8. CME Databento connection.
9. CME MBO stream validation.
10. CME MBP-10 stream validation.
11. CME trades stream validation.
12. CME microstructure calculation.
13. CME volume-profile calculation.
14. CME↔MT5 basis collection.
15. Basis stability gate.
16. CME volume authority calculation.
17. Fusion of CME intelligence into the canonical GSIS decision.
18. Long/short permission gate.
19. Risk-per-trade gate.
20. Position-size calculation.
21. Maximum-position/open-trade gate.
22. Execution gate.
23. Controlled demo execution test.
24. Execution response validation.
25. Position reconciliation.
26. Stop-loss/take-profit validation.
27. SQLite persistence validation.
28. Audit-trail validation.
29. Controlled connector-failure recovery test.
30. Controlled CME-feed failure recovery test.
31. Stale-data rejection test.
32. Duplicate-execution protection test.
33. Autonomous restart/recovery test.
34. Final PASS only if every mandatory gate passes.

## Current certification decision

**GSIS is NOT certified as a complete autonomous institutional trading system yet.**

The current canonical runtime can be described as an autonomous **MT5 market-read → simplified analysis → risk sizing → optional execution → persistence loop**, but not yet as the complete CME-enhanced institutional GSIS architecture.

## Priority remediation order

1. Wire CME microstructure + volume profile + alignment + authority into `GSISUnifiedEngine`.
2. Establish one canonical execution-control/risk-control authority and eliminate bypasses.
3. Add execution reconciliation and position lifecycle management.
4. Add feed-health, stale-data, circuit-breaker, and recovery controls.
5. Replace the current certification script with a true staged end-to-end harness.
6. Run that harness on the real MT5 host with a demo account and configured CME feed.
7. Only then enable autonomous execution.
