# GSIS Engine Authority Classification

## Canonical production path

Only the following path may create or execute a trading decision:

`External Market Data -> MT5 Order Flow / CME Intelligence -> Unified Market Intelligence -> DecisionGovernorEngine -> CanonicalTradeSignal -> Canonical Risk -> Canonical Execution`

## Authoritative production engines

- `institutional/unified_engine.py` — canonical runtime and orchestration.
- `intelligence/decision_governor_engine.py` — sole BUY/SELL/WAIT authority.
- `intelligence/canonical_trade_signal.py` — sole canonical trade object.
- `volume_intelligence/*` — CME/volume intelligence inputs; not independent trade authorities.
- `adapters/cme/*` — external CME data acquisition only.

## Non-authoritative / legacy engines

Other historical signal, strategy, agent, planning, notification, and orchestration modules are **non-canonical** unless explicitly wired into the canonical path above. They must not independently place orders or create a competing BUY/SELL/WAIT signal for production execution.

They may be used for research, analytics, diagnostics, migration, or future integration.

## Notification rule

Telegram, WhatsApp, and any future notification publisher must consume `CanonicalTradeSignal`. Notification code is not permitted to infer a new market decision.

## Certification rule

A future engine can become authoritative only after it is explicitly connected to the canonical path and covered by the canonical-path certification tests.
