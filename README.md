# GSIS INSTITUTIONAL

## Gold Strategic Intelligence System — Institutional Architecture, Operational Catalogue and Reverse-Engineering Guide

GSIS INSTITUTIONAL is a multi-engine market-intelligence, decision, risk, execution, research, learning, audit and autonomous-runtime framework. Its design goal is to transform broker-supplied market data and approved external intelligence into a governed, explainable `CanonicalTradeSignal`, then optionally carry that signal through risk-controlled execution and post-trade learning.

This README is the project's master orientation document. It explains **what happens first, what happens next, what has authority, what is downstream, what is historical/research infrastructure, and which components are supporting or legacy rather than independent trading authorities**.

> **Certification principle:** the existence of an engine file does not mean that engine is part of the live production path. Production authority belongs to the canonical runtime and its explicitly wired dependencies.

---

## 1. Mission

GSIS exists to provide a broker-neutral institutional trading intelligence system that can:

- ingest live market information from the connected trading environment;
- normalize market and broker information;
- build multi-timeframe market context;
- analyze structure, liquidity, price action, order flow, volume and market regime;
- incorporate approved event/news and external market intelligence;
- compare present conditions with historical observations and validated patterns;
- produce a single governed decision: `BUY`, `SELL`, or `WAIT`;
- represent that decision as one `CanonicalTradeSignal`;
- apply broker-aware risk and position sizing;
- pass the canonical signal to execution through the MT5 Universal Connector;
- publish the same canonical signal to communication channels without creating a competing decision;
- record decisions, executions and outcomes for audit and learning;
- continuously improve knowledge only through validated research/learning processes.

GSIS is therefore intended to behave as a **closed-loop intelligence system**, not as a collection of unrelated trading scripts.

---

## 2. Core architectural laws

### Law 1 — One production authority

`institutional.GSISUnifiedEngine` is the intended production runtime. Legacy orchestrators and historical implementations are not allowed to become competing production authorities merely because their files remain in the repository.

### Law 2 — One canonical decision

`DecisionGovernorEngine` is the decision authority. Its output is `CanonicalTradeSignal`.

### Law 3 — One canonical trade object

After the decision is approved, the canonical signal carries the trade plan and downstream state rather than creating parallel, competing trade objects.

### Law 4 — One execution boundary

GSIS does not become broker-specific. MT5 broker interaction belongs at the MT5 Universal Connector boundary.

### Law 5 — Broker metadata is runtime data

Symbol names, digits, tick size/value, volume limits, account conditions, execution constraints and other broker properties must be discovered from the connected trading environment rather than assumed from a particular broker.

### Law 6 — Communication is downstream

Telegram/WhatsApp receive the canonical signal. They are communication boundaries, not decision engines. A future bidirectional communication unit may accept user commands, but it must still route requests through governed system interfaces.

### Law 7 — Learning cannot silently override governance

Historical statistics, pattern memory, machine-learning outputs and adaptive models may provide evidence, probabilities or validated knowledge. They must not bypass the Decision Governor or directly place trades.

### Law 8 — No fake certification

Static tests are not live broker certification. A live certification requires the actual connected MT5 terminal, connector, broker session and any required external intelligence credentials.

---

# 3. The system in one graph

```text
                         ┌──────────────────────────────┐
                         │      MT5 UNIVERSAL           │
                         │         CONNECTOR            │
                         │                              │
                         │ Broker discovery             │
                         │ Symbol resolution            │
                         │ Live ticks / candles         │
                         │ Account / symbol metadata    │
                         │ Positions / execution        │
                         └──────────────┬───────────────┘
                                        │
                                        ▼
                         ┌──────────────────────────────┐
                         │     MARKET DATA LAYER        │
                         │ normalization / quality      │
                         │ candles / ticks / MTF        │
                         └──────────────┬───────────────┘
                                        │
                    ┌───────────────────┼────────────────────┐
                    │                   │                    │
                    ▼                   ▼                    ▼
              Market Structure      Order Flow          Volume/CME
              Liquidity             Price Action        Microstructure
              Supply/Demand         Regime              External Events
                    │                   │                    │
                    └───────────────────┼────────────────────┘
                                        ▼
                              INTELLIGENCE FUSION
                                        │
                         ┌──────────────┴──────────────┐
                         │                             │
                         ▼                             ▼
                Historical / Research          Pattern / Memory
                Statistics / Backtest          Bayesian / HMM
                         │                             │
                         └──────────────┬──────────────┘
                                        ▼
                               STRATEGY / SETUP
                                        │
                                        ▼
                              DECISION GOVERNOR
                                        │
                              BUY / SELL / WAIT
                                        │
                                        ▼
                              CanonicalTradeSignal
                                        │
                    ┌───────────────────┼────────────────────┐
                    │                   │                    │
                    ▼                   ▼                    ▼
                  RISK              AUDIT              NOTIFICATION
                    │                                      │
                    ▼                                  Telegram
              Position Size                             WhatsApp
                    │
                    ▼
             EXECUTION GOVERNOR
                    │
                    ▼
             MT5 UNIVERSAL CONNECTOR
                    │
                    ▼
                  BROKER
                    │
                    ▼
              ACTUAL OUTCOME
                    │
                    ├──────────────► Journal / Audit
                    │
                    └──────────────► Learning / Memory
                                         │
                                         └──────► future intelligence
```

---

# 4. Operational stages — what comes first, second, third...

The following sequence describes the intended behavior of the production system.

## Stage 0 — Bootstrap and configuration

The system loads environment configuration, validates required services, initializes databases/state, establishes logging and checks that the runtime is allowed to operate.

Nothing should trade merely because the Python process started.

## Stage 1 — Broker and connector discovery

GSIS relies on the MT5 Universal Connector to identify the connected MT5 environment. The connector is responsible for broker/server/account awareness and broker-specific symbol discovery/resolution.

GSIS should consume the connector's normalized representation instead of containing broker-specific assumptions.

## Stage 2 — Market-data acquisition

Live market information enters through the approved data boundary. This includes ticks, candles, market depth/order-flow information where available, and broker metadata required for calculations.

The data layer is responsible for normalization and data-quality checks before intelligence engines consume it.

## Stage 3 — Candle and timeframe construction

Raw market data is converted into the timeframes required by the intelligence layer. Multi-timeframe context is built before a trade decision is considered.

The repository contains candle builders, live candle engines and multi-timeframe engines for this purpose.

## Stage 4 — Market-state construction

GSIS determines the current market context. Relevant subsystems include:

- market structure;
- liquidity;
- price action;
- order flow and microstructure;
- supply/demand;
- market regime;
- volume profile;
- CME/COMEX intelligence when enabled;
- event/news intelligence;
- cross-asset/context intelligence.

This stage answers: **what is happening now?**

## Stage 5 — External intelligence and event context

Approved external feeds can provide economic-calendar, news, sentiment, CME and other contextual information. These feeds enrich intelligence; they do not become independent trading authorities.

The repository contains dedicated provider and adapter boundaries for Alpha Vantage, Twelve Data, Finnhub, FMP, news, CME/Databento and other optional sources.

## Stage 6 — Historical and statistical comparison

Historical data, pattern memory, statistical models, Bayesian state, regime history and prior outcomes can be consulted to determine whether the present market resembles previously observed conditions.

This stage is particularly important for the planned research/learning loop. Historical evidence should be time-causal: information unavailable at the decision timestamp must never leak into that decision.

## Stage 7 — Pattern recognition and strategy qualification

Pattern and strategy engines identify candidate setups. Examples include structure, liquidity, candlestick, displacement, supply/demand, order-flow, regime and pattern-probability components.

A candidate setup is **not yet a trade**.

## Stage 8 — Intelligence fusion

Evidence from the relevant engines is combined. The system should preserve provenance so that a later audit can determine why a particular condition contributed to the decision.

Fusion answers: **how strong and coherent is the evidence?**

## Stage 9 — Decision Governor

The Decision Governor is the final decision authority.

It resolves the evidence into:

```text
BUY
SELL
WAIT
```

The decision is accompanied by confidence, reasoning, risk state and the information needed to construct the canonical trade plan.

## Stage 10 — CanonicalTradeSignal creation

The decision becomes the single authoritative `CanonicalTradeSignal`.

The signal is the handoff contract between intelligence, risk, execution, audit and notification.

Typical fields include:

- `signal_id`
- canonical instrument/symbol information
- timeframe
- decision
- confidence
- reasoning
- entry
- stop loss
- take profit(s)
- risk fraction
- position size
- risk state
- execution status
- invalidation
- metadata
- timestamp

## Stage 11 — Risk and position sizing

Risk consumes the canonical signal and broker/account metadata. Position size must respect the actual broker's trading constraints and the system's configured risk policy.

Risk can reject a signal even when the directional decision is BUY or SELL.

## Stage 12 — Execution governance

The execution layer validates that the canonical signal is executable, checks execution conditions, prevents duplicate execution and sends the signal through the MT5 Universal Connector.

GSIS does not directly assume a broker implementation.

## Stage 13 — Broker execution

The connector translates the canonical execution request into the connected MT5 environment. The broker returns the actual execution result.

The actual fill, rejection, slippage and broker response become part of the system record.

## Stage 14 — Notification

The canonical signal can be published downstream to Telegram and WhatsApp.

```text
CanonicalTradeSignal
        │
        ├──► Telegram publisher
        └──► WhatsApp publisher
```

The publishers must not create or modify a trading decision.

## Stage 15 — Position lifecycle and monitoring

After execution, position and trade-management components monitor the live position, lifecycle events, execution state, protection and broker state.

## Stage 16 — Audit and journal

The system records the decision, inputs, reasoning, risk state, execution result and eventual outcome. This creates an auditable chain:

```text
market state → evidence → decision → canonical signal → risk → execution → outcome
```

## Stage 17 — Outcome learning

Once the trade outcome is known, the outcome is stored against the original signal and market context.

This is the feedback boundary for adaptive learning.

## Stage 18 — Research / learning update

Validated historical and live outcomes can be used to update pattern statistics, regime memory, confidence calibration, strategy research and other learning artifacts.

Learning must be validated before becoming production knowledge.

## Stage 19 — Continuous loop

The runtime returns to Stage 1/2 and repeats.

```text
DISCOVER → INGEST → CONTEXT → ANALYZE → FUSE → GOVERN
       → CANONICAL SIGNAL → RISK → EXECUTE → OBSERVE
       → RECORD → LEARN → VALIDATE → NEXT CYCLE
```

---

# 5. Ranking and authority behavior

GSIS is multi-engine, but multi-engine does **not** mean every engine has equal authority.

The practical ranking is:

### Tier 1 — Infrastructure authority

The connector, configuration, data-quality, persistence, runtime and safety boundaries determine whether the system can safely operate.

### Tier 2 — Market-state authority

Market data, structure, order flow, liquidity, price action, regime and approved external intelligence describe the market.

### Tier 3 — Research and learning evidence

Historical statistics, pattern memory, Bayesian/HMM state, outcome memory and adaptive models provide evidence and learned context.

### Tier 4 — Strategy/setup qualification

Strategy and setup engines turn market context into candidate opportunities.

### Tier 5 — Decision authority

`DecisionGovernorEngine` resolves the candidate evidence into BUY/SELL/WAIT and produces the canonical signal.

### Tier 6 — Risk authority

Risk can reject or resize the canonical signal based on account and broker conditions.

### Tier 7 — Execution authority

Execution governance determines whether the canonical signal can actually be transmitted to the broker.

### Tier 8 — Broker execution

The MT5 Universal Connector and connected broker produce the actual market result.

### Tier 9 — Learning feedback

Actual outcomes become evidence for future research and model validation.

**No lower tier should silently bypass a higher governing tier.**

---

# 6. The CanonicalTradeSignal contract

`CanonicalTradeSignal` is the central trade-state contract.

The desired lifecycle is:

```text
Candidate evidence
      ↓
Decision Governor
      ↓
CanonicalTradeSignal
      ↓
Trade plan
      ↓
Risk enrichment
      ↓
Execution state
      ↓
Broker result
      ↓
Outcome
```

This prevents the historical problem of several engines independently producing BUY/SELL decisions, entry prices, risk instructions or execution commands.

---

# 7. Market intelligence catalogue

The repository contains a large intelligence family. The principal functional groups are:

### Market data and normalization

- `gsis_market_data_hub.py`
- `gsis_market_data_orchestrator.py`
- `gsis_data_normalizer.py`
- provider manager/registry components
- historical data loaders/importers
- live market processors
- candle and timeframe engines

### Structure

- `market_structure_engine.py`
- `market_structure_intelligence_engine.py`
- `structure_break_engine.py`
- `smc_structure_engine.py`
- `supply_demand_engine.py`
- institutional zone components

### Liquidity

- `liquidity_engine.py`
- `liquidity_intelligence_engine.py`
- `liquidity_mapping_engine.py`
- `liquidity_sweep_engine.py`
- liquidity quality components

### Order flow / microstructure

- `order_flow_engine.py`
- `order_flow_microstructure_engine.py`
- `microstructure_engine.py`
- live order-flow components
- rolling order-flow components
- CME microstructure components

### Volume / CME

- `volume_profile_engine.py`
- `volume_intelligence/*`
- CME/Databento adapter
- alignment and authority components

### Price action / patterns

- `price_action_intelligence_engine.py`
- `candlestick_intelligence_engine.py`
- `chart_pattern_intelligence_engine.py`
- pattern discovery, recognition, matching, library and probability components

### Regime / probability

- market-regime engines
- HMM regime model
- Bayesian engine
- Markov engine
- probability engine
- confidence and calibration engines

### Intelligence fusion

- intelligence fusion core/engine
- multi-agent intelligence fusion
- institutional fusion
- adaptive intelligence bridges
- state-vector and context engines

---

# 8. Strategy layer versus Signal Generation

These are deliberately different concepts.

**Strategy** determines **what type of setup should be considered and under what market conditions**.

**Signal generation** turns qualified evidence into a candidate directional/action representation.

The **Decision Governor** is above both and decides whether the evidence is sufficient for the authoritative BUY/SELL/WAIT outcome.

Therefore:

```text
Strategy
   ↓
Candidate setup
   ↓
Signal evidence
   ↓
Decision Governor
   ↓
CanonicalTradeSignal
```

A strategy engine must not become a second Decision Governor.

---

# 9. Historical backtesting and research architecture

Historical research is a separate but essential dimension of GSIS.

Relevant repository components include:

- `intelligence/backtesting_engine.py`
- `intelligence/backtesting_validation_engine.py`
- `intelligence/backtest_controller.py`
- `intelligence/historical_replay_engine.py`
- `intelligence/market_replay_controller.py`
- `intelligence/data/gsis_historical_data_importer.py`
- `intelligence/data/gsis_historical_market_downloader.py`
- `intelligence/data/gsis_historical_pattern_memory_engine.py`
- `engines/backtest/backtest_engine.py`
- historical database/import components
- research and statistical engines.

The correct long-term architecture is:

```text
Historical data
     ↓
Feature/context reconstruction
     ↓
Historical replay
     ↓
Same strategy/decision logic
     ↓
CanonicalTradeSignal
     ↓
Simulated risk/execution
     ↓
Outcome
     ↓
Performance statistics
     ↓
Research validation
```

The strongest test is not a separate backtest strategy that merely resembles live trading. It is a **historical replay of the same canonical decision path with time-causal data**.

---

# 10. Machine learning and adaptive learning

GSIS contains learning-related infrastructure, including:

- `ai_learning_engine.py`
- `adaptive_learning_engine.py`
- `adaptive_strategy_engine.py`
- `strategy_adaptation_engine.py`
- `strategy_evolution_engine.py`
- `pattern_discovery_engine.py`
- `pattern_auto_generator.py`
- `pattern_library_engine.py`
- `pattern_memory_engine.py`
- `outcome_memory_engine.py`
- `gsis_pattern_probability_engine.py`
- `gsis_confidence_calibration_engine.py`
- Bayesian/HMM/Markov components
- learning databases and memory stores.

The intended closed loop is:

```text
Past market data
      ↓
Patterns / features / regimes
      ↓
Historical outcomes
      ↓
Statistics / probability / model training
      ↓
Validated knowledge
      ↓
Current market comparison
      ↓
Intelligence fusion
      ↓
Decision Governor
```

And after live trading:

```text
Canonical signal
      ↓
Actual outcome
      ↓
Outcome memory
      ↓
Pattern/statistical update
      ↓
Validation
      ↓
Approved knowledge
      ↓
Future decisions
```

**Important:** the repository contains the components and data stores for this architecture, but full end-to-end certification of the learning loop requires separate testing to prove that historical knowledge is actually consumed by the production canonical path and that live outcomes safely return to validated learning.

---

# 11. External intelligence

The repository contains provider boundaries for market/news/context information, including Alpha Vantage, Twelve Data, Finnhub, FMP, news and CME/Databento components.

External feeds are contextual inputs. They do not automatically become authoritative trade decisions.

For live CME intelligence, the repository explicitly separates the external CME connection from the microstructure calculator. CME connectivity belongs to the adapter; the intelligence engine consumes normalized data.

---

# 12. Event and news reaction architecture

Event intelligence is intended to answer questions such as:

- Is a major scheduled event approaching?
- What was the actual result versus expectation?
- What market reaction occurred?
- Is the reaction consistent with historical event behavior?
- Should risk/execution conditions change?

The same architecture can support live monitoring of major central-bank events, speeches and other market-moving events, provided the relevant external feed is configured and the resulting information is routed through governed intelligence rather than a direct trading bypass.

---

# 13. Risk architecture

Risk is not a strategy selector. It is a safety and sizing layer.

It considers actual account/broker information and the canonical trade plan.

The conceptual sequence is:

```text
CanonicalTradeSignal
       ↓
Account state
       ↓
Broker symbol metadata
       ↓
Risk calculation
       ↓
Position size
       ↓
Risk approval/rejection
```

The risk subsystem also includes portfolio, position, capital-protection, risk-guard, stress-testing and trade-safety components.

---

# 14. Execution architecture

Execution is downstream from intelligence.

```text
CanonicalTradeSignal
        ↓
Risk-approved signal
        ↓
Execution governance
        ↓
MT5 Universal Connector
        ↓
Connected MT5 terminal
        ↓
Broker
```

The broker-neutral requirement means GSIS must not contain separate production logic for individual brokers.

The same GSIS build should be capable of operating against any supported MT5 broker through the connector, subject to the broker's actual trading capabilities and restrictions.

---

# 15. Symbol neutrality

GSIS should operate on a canonical instrument identity and allow the MT5 Universal Connector to resolve the actual broker symbol.

```text
GSIS canonical instrument
        ↓
MT5 Universal Connector
        ↓
broker symbol discovery/resolution
        ↓
actual MT5 symbol
```

GSIS must not maintain a hardcoded broker-specific alias table as a competing source of truth when the Universal Connector already owns this responsibility.

---

# 16. Communication architecture

Communication is deliberately downstream:

```text
Decision Governor
       ↓
CanonicalTradeSignal
       ├────────► Telegram
       └────────► WhatsApp
```

Current repository boundaries include:

- `communication/canonical_notification_bus.py`
- `communication/telegram_canonical_publisher.py`
- `communication/whatsapp_canonical_publisher.py`

The publisher interfaces do not constitute proof of live provider connectivity. Provider tokens/credentials and transport implementation belong to the communication deployment layer.

A future bidirectional communication unit can be added without changing the canonical trading authority.

---

# 17. Audit, transparency and observability

The repository contains audit, journal, telemetry, transparency, monitoring, health, incident and recovery components.

The desired audit chain is:

```text
Data snapshot
   ↓
Features/context
   ↓
Engine evidence
   ↓
Decision reasoning
   ↓
CanonicalTradeSignal
   ↓
Risk result
   ↓
Execution request
   ↓
Broker response
   ↓
Position lifecycle
   ↓
Outcome
   ↓
Learning record
```

This allows post-event reconstruction rather than relying on a final BUY/SELL label alone.

---

# 18. Runtime supervision and resilience

System supervision includes health monitoring, watchdogs, process locking, recovery, background guards, disaster recovery and service supervision.

The autonomous runtime should therefore be understood as:

```text
Start
 ↓
Validate dependencies
 ↓
Connect / recover
 ↓
Run cycle
 ↓
Capture state
 ↓
Handle errors
 ↓
Recover where safe
 ↓
Run next cycle
```

An exception in one cycle must not automatically destroy the entire autonomous service, while safety-critical failures should prevent trading rather than force execution.

---

# 19. Engine catalogue and repository organization

The repository is large and intentionally multi-subsystem. Major directories include:

| Directory | Primary role |
|---|---|
| `adapters/` | External/system integration boundaries |
| `agents/` | Multi-agent coordination |
| `analytics/` | Performance analytics |
| `api/`, `api_gateway/` | API interfaces |
| `audit/` | Audit trail |
| `communication/` | Canonical notification boundaries and data bus |
| `config/`, `configuration/` | Runtime/configuration control |
| `core/` | Foundational infrastructure, engines, governance, events, security |
| `data/` | Runtime state, historical/live data and persistence artifacts |
| `data_gateway/` | Market-data gateways |
| `data_quality/` | Data integrity/quality |
| `database/` | Databases and memory stores |
| `decision/` | Decision command infrastructure |
| `deployment/` | Deployment support |
| `docs/` | Architecture/reverse-engineering documentation |
| `engines/` | Large organized engine catalogue, including legacy/supporting components |
| `execution/` | Execution optimization/support |
| `explainability/` | Explainable decision output |
| `health/` | Health subsystem |
| `institutional/` | Unified production runtime |
| `intelligence/` | Main intelligence, decision, risk, strategy, research and trade engines |
| `knowledge/` | Knowledge graph |
| `learning/` | Adaptive learning and pattern memory |
| `market/`, `market_data/` | Candle/market-data support |
| `memory/` | Knowledge memory |
| `monitoring/` | Runtime monitoring |
| `orchestration/` | Event orchestration |
| `pipeline/` | Pipeline controllers/tests |
| `portfolio/` | Portfolio intelligence |
| `research/` | Autonomous research |
| `resilience/` | Disaster recovery |
| `risk/` | Risk intelligence/management |
| `runtime/` | Production runtime support |
| `security/` | Security governance |
| `simulation/` | Scenario/stress simulation |
| `strategy/` | Autonomous strategy/evolution |
| `streaming/` | Streaming/WebSocket infrastructure |
| `system/` | Health/recovery |
| `validation/` | Model validation |
| `volume_intelligence/` | CME/volume intelligence |
| `websocket/` | WebSocket interfaces |

For the detailed engine-by-engine catalogue, see `docs/GSIS_INSTITUTIONAL_REVERSE_ENGINEERING_CATALOGUE.md`.

For the functional dependency graph, see `docs/GSIS_FUNCTIONAL_STRUCTURE.md`.

---

# 20. Legacy and duplicate-looking engines

Because GSIS evolved over many iterations, the repository contains backups, versioned engines, compatibility layers and similarly named components. Examples include backup orchestrators, backup adapters, duplicate-looking order-flow/signal/management components and historical copies.

These files should be treated as **evidence and historical implementation material unless explicitly wired into the canonical production runtime**.

The repository contains `LEGACY_ENGINE_CLASSIFICATION.md` specifically to prevent a historical file from accidentally becoming a second production authority.

A future cleanup phase may archive or remove obsolete code, but deletion should follow dependency analysis and certification rather than filename matching alone.

---

# 21. Databases and memory

GSIS contains multiple SQLite databases and JSON state stores for different historical/runtime purposes, including market history, intelligence, learning, memory, patterns, trades, execution state and performance.

Production design should progressively converge toward clearly defined ownership for each data class so that two databases do not silently become competing sources of truth.

---

# 22. Testing and certification

The repository includes tests for:

- canonical trading path;
- canonical notification bus;
- end-to-end wiring;
- broker-symbol resolution boundary;
- market structure;
- liquidity;
- order flow;
- volume profile;
- execution control;
- position sizing;
- risk management;
- realtime pipeline;
- state and connection behavior;
- trade planning/orchestration;
- model validation.

`gsis_certification.py` provides a certification harness that distinguishes static/deterministic validation from live environment validation.

### Certification levels

**Level 1 — Static architecture**

Source and dependency structure is inspected.

**Level 2 — Deterministic functional tests**

Pure engines and canonical wiring are tested without requiring a broker.

**Level 3 — Connector certification**

The actual MT5 Universal Connector is connected to an MT5 terminal and broker environment.

**Level 4 — Live broker certification**

Market data, symbol resolution, account metadata, risk, execution, fill/result handling and recovery are tested with the actual broker.

**Level 5 — Multi-broker neutrality certification**

The same GSIS build is tested against multiple MT5 brokers without broker-specific source modifications.

**Level 6 — Historical/research certification**

The canonical decision path is replayed against historical data with strict time-causality and validated performance accounting.

**Level 7 — Learning-loop certification**

Historical and live outcomes are shown to flow into validated memory/statistics/model updates and then back into future intelligence without bypassing governance.

**Level 8 — Long-duration autonomy**

The system runs continuously while monitoring data loss, reconnects, state recovery, duplicate prevention, execution failures and resource stability.

---

# 23. Installation and deployment concept

GSIS is intended to run on a suitable PC/server environment with Python and the required dependencies.

For live MT5 operation:

```text
PC / Server
│
├── Python
├── GSIS INSTITUTIONAL
├── MT5 Universal Connector
└── MetaTrader 5 terminal
        │
        └── connected broker account
```

The external connector remains responsible for the actual MT5/broker integration.

Optional external providers require their own credentials and dependencies.

Never commit real API keys, tokens or broker credentials to the repository.

---

# 24. Current implementation status

The repository currently demonstrates a substantial canonical architecture including:

- unified production runtime;
- canonical trade signal contract;
- Decision Governor boundary;
- canonical risk/execution interfaces;
- MT5 Universal Connector boundary;
- broker-symbol resolution boundary;
- CME/volume intelligence infrastructure;
- canonical notification boundaries;
- historical/backtesting infrastructure;
- research and learning infrastructure;
- audit/telemetry/monitoring infrastructure;
- extensive deterministic tests.

However, **architecture implemented is not the same as every subsystem being live-certified**.

The highest remaining certification targets are:

1. actual MT5 Universal Connector integration;
2. broker-neutral multi-broker certification;
3. full historical replay of the canonical path;
4. research-to-production knowledge flow validation;
5. machine-learning/adaptive-learning closed-loop validation;
6. long-duration autonomous operation;
7. live communication provider transport certification when credentials are configured.

---

# 25. Development discipline

When extending GSIS:

1. inspect the existing architecture first;
2. reuse an existing authoritative engine where possible;
3. do not create a duplicate engine merely because a feature needs improvement;
4. preserve the canonical signal contract;
5. preserve the Decision Governor as final decision authority;
6. preserve the MT5 Universal Connector as the broker boundary;
7. use runtime data rather than hardcoded market/broker values;
8. add deterministic tests before live certification;
9. document new engine ownership and data flow;
10. certify the changed path before declaring the system stable.

---

# 26. Final mental model

GSIS should be understood as a **hierarchical evidence-and-governance machine**:

```text
                    DATA
                     ↓
                  CONTEXT
                     ↓
               MARKET STATE
                     ↓
             INTELLIGENCE ENGINES
                     ↓
             HISTORICAL KNOWLEDGE
                     ↓
             PATTERN / STATISTICS
                     ↓
              STRATEGY / SETUP
                     ↓
              INTELLIGENCE FUSION
                     ↓
             DECISION GOVERNOR
                     ↓
            CanonicalTradeSignal
                     ↓
                    RISK
                     ↓
                 EXECUTION
                     ↓
            MT5 UNIVERSAL CONNECTOR
                     ↓
                   BROKER
                     ↓
                  OUTCOME
                     ↓
              AUDIT + LEARNING
                     ↓
              VALIDATED KNOWLEDGE
                     ↓
                NEXT DECISION
```

The central objective is not to make every engine independently intelligent. The objective is to make **many specialized engines contribute evidence to one governed, auditable and continuously improving decision process**.

---

## Related documentation

- `docs/GSIS_INSTITUTIONAL_REVERSE_ENGINEERING_CATALOGUE.md` — detailed reverse-engineering catalogue.
- `docs/GSIS_FUNCTIONAL_STRUCTURE.md` — functional architecture and data-flow structure.
- `LEGACY_ENGINE_CLASSIFICATION.md` — classification of historical/non-authoritative engines.
- `BROKER_SYMBOL_RESOLUTION.md` — broker-neutral symbol-resolution architecture.
- `GSIS_END_TO_END_AUDIT.md` — end-to-end audit record.
- `GSIS_IMPORT_AUDIT.txt` — import/dependency audit snapshot.
- `GSIS_DEPENDENCY_AUDIT.txt` — dependency audit snapshot.

## Repository

`Classicman-ai/GSIS_INSTITUTIONAL`

**Status:** canonical architecture under continued certification; live broker, multi-broker, historical-learning and long-duration autonomy certification remain environment-dependent.
