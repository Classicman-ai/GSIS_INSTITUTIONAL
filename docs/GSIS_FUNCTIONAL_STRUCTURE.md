# GSIS INSTITUTIONAL — Functional System Structure

## Purpose

This document defines the canonical functional flow of GSIS INSTITUTIONAL, including the live broker-data path, intelligence fusion, decision governance, execution, audit/learning loop, and notification outputs.

## Canonical Architecture

```text
                    ┌─────────────────────────┐
                    │ MT5 UNIVERSAL CONNECTOR │
                    │   LIVE BROKER DATA      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ DATA VALIDATION          │
                    │ freshness / integrity    │
                    └────────────┬────────────┘
                                 │
                                 ▼
              ┌─────────────────────────────────────┐
              │       MARKET INTELLIGENCE            │
              │                                     │
              │ Structure                           │
              │ Liquidity / Order Flow              │
              │ Price Action                        │
              │ Multi-Timeframe                     │
              │ Market Regime                       │
              │ Patterns                            │
              │ Statistics / Probability            │
              │ Events / News                       │
              └──────────────────┬──────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ INTELLIGENCE FUSION     │
                    │                         │
                    │ Combine all evidence    │
                    │ into one market view    │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ CONFIDENCE / PROBABILITY│
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ RISK & POSITION ENGINE  │
                    │                         │
                    │ Equity                  │
                    │ Exposure                │
                    │ Position size           │
                    │ Stop / target            │
                    │ Portfolio risk          │
                    └────────────┬────────────┘
                                 │
                                 ▼
                 ┌────────────────────────────────┐
                 │      DECISION GOVERNOR          │
                 │                                │
                 │ BUY / SELL / WAIT              │
                 │ Confidence                     │
                 │ Evidence and reasoning         │
                 │ Risk assessment                │
                 │ Invalidation conditions        │
                 └───────────────┬────────────────┘
                                 │
                 ┌───────────────┴────────────────┐
                 │                                │
                 ▼                                ▼
      ┌─────────────────────┐          ┌────────────────────────┐
      │ NOTIFICATION BUS    │          │ EXECUTION GOVERNOR     │
      │                     │          │                        │
      │ BUY / SELL / WAIT   │          │ Execution permission   │
      │ Reasoning           │          │ Risk approval           │
      │ Confidence          │          │ Broker availability     │
      │ Market context      │          │ Conditions valid        │
      └──────────┬──────────┘          └────────────┬───────────┘
                 │                                  │
          ┌──────┴───────┐                          ▼
          │              │               ┌──────────────────────┐
          ▼              ▼               │ MT5 UNIVERSAL        │
      ┌─────────┐   ┌──────────┐         │ CONNECTOR            │
      │ TELEGRAM│   │ WHATSAPP │         │ LIVE BROKER EXECUTION│
      └────┬────┘   └────┬─────┘         └──────────┬───────────┘
           │             │                          │
           └──────┬──────┘                          │
                  │                                 │
                  ▼                                 ▼
          ┌─────────────────────────────────────────────┐
          │              TRADE LIFECYCLE                │
          │                                             │
          │ Open → Monitor → Manage → Close             │
          └──────────────────────┬──────────────────────┘
                                 │
                                 ▼
          ┌─────────────────────────────────────────────┐
          │ AUDIT / JOURNAL / TELEMETRY / PERFORMANCE   │
          └──────────────────────┬──────────────────────┘
                                 │
                                 ▼
          ┌─────────────────────────────────────────────┐
          │ MEMORY / LEARNING / OUTCOME ANALYSIS        │
          └──────────────────────┬──────────────────────┘
                                 │
                                 ▼
                         NEXT MARKET CYCLE
                                 │
                                 └──────────────► MT5
```

## Canonical Decision Principle

The Decision Governor is the single source of truth for the trading decision. It produces one canonical decision object, which is then distributed to both execution and notification paths.

```text
Market Data
    ↓
Intelligence
    ↓
Decision Governor
    ↓
Canonical Decision
    ├──────────────► Execution
    │
    └──────────────► Notification
                         ├── Telegram
                         └── WhatsApp
```

Notification components must not independently generate conflicting BUY/SELL/WAIT decisions. They should consume the same canonical decision and its dynamically generated evidence, reasoning, confidence, risk state, and invalidation conditions.

## Example Signal Payload

```text
GSIS SIGNAL
────────────────────────

SYMBOL: <live symbol>
DECISION: <BUY | SELL | WAIT>
CONFIDENCE: <live calculated confidence>

REASONING:
• <dynamic market evidence>
• <dynamic structure/liquidity evidence>
• <dynamic regime/context evidence>
• <dynamic multi-timeframe evidence>

RISK:
• Risk state: <dynamic>
• Position sizing: <dynamic>
• Execution gate: <dynamic>

INVALIDATION:
<dynamic condition derived from current market state>

STATUS:
<dynamic execution status>

GSIS INSTITUTIONAL
```

## Design Constraints

- Market prices, account state, signals, and risk inputs must come from live connected sources rather than hardcoded market values.
- The notification path must consume the canonical decision rather than creating a second decision engine.
- Telegram and WhatsApp are output channels and must not become competing sources of truth.
- Execution remains subject to risk and execution-governance gates.
- Every decision/execution cycle should feed audit, telemetry, performance, memory, and learning subsystems.
- The runtime should continuously repeat the cycle as new broker data arrives.
