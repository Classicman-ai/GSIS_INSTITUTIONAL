# GSIS INSTITUTIONAL — Reverse-Engineering Catalogue & Architecture Map

**Document type:** Institutional reverse-engineering / repository catalogue  
**System:** GSIS INSTITUTIONAL  
**Repository:** `Classicman-ai/GSIS_INSTITUTIONAL`  
**Purpose:** Preserve an auditable map of the system's engines, subsystems, dependencies, decision flow, and architectural intent.

> **Important scope note:** This document is a reverse-engineering map, not a claim that every class or method has been formally verified. It is based on the repository inventories, import audits, master-orchestrator source, historical architecture listings, configuration checks, and system-governance material available during the audit. Engine purpose is inferred from filenames, module placement, imports, and the stated GSIS constitution where implementation details were not inspected directly.

---

## 1. Executive Summary

GSIS INSTITUTIONAL is best understood as a **modular institutional trading and decision-governance platform** rather than a single trading strategy.

Its architecture is organized around a chain that attempts to move from:

**market data → normalization → market understanding → intelligence/fusion → probability/confidence → risk → decision governance → execution control → broker gate → trade lifecycle → monitoring → audit → memory/learning → recovery/telemetry.**

The central design objective is to make trading decisions:

- data-driven,
- statistically justified,
- explainable,
- auditable,
- repeatable,
- transparent,
- risk-controlled.

The GSIS Constitution explicitly states that only the GSIS Core may issue BUY, SELL, or WAIT; AI may explain, audit and educate but does not override trading decisions. It also defines a complete trade lifecycle and requires institutional explanations for decisions.

This makes the system conceptually closer to an **institutional decision operating system** than a conventional indicator-based Expert Advisor.

---

# 2. Mission and Institutional Philosophy

The documented mission is:

> Make objective, explainable, statistically validated, institutional-grade trading decisions while maintaining transparency and disciplined risk management.

The governing principles are:

1. Data-driven
2. Statistically justified
3. Explainable
4. Auditable
5. Transparent
6. Repeatable
7. Risk-controlled

The constitutional design also establishes:

- one responsibility per engine;
- explicit consumers of engine outputs;
- a single source of truth for decisions, lifecycle and events;
- learning from completed trades;
- institutional-quality reporting;
- modularity for future markets and brokers.

This is important because it explains why the repository contains many specialized engines rather than one monolithic strategy.

---

# 3. High-Level Architecture

```text
                    ┌──────────────────────────┐
                    │       MARKET SOURCES     │
                    │ APIs / Broker / Streams  │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │       DATA SUBSYSTEM     │
                    │ price / candles / history│
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ MARKET INTERPRETATION    │
                    │ structure / regime /     │
                    │ liquidity / order flow   │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ INTELLIGENCE SUBSYSTEM    │
                    │ patterns / Bayesian /     │
                    │ fusion / scoring / memory │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ PROBABILITY & CONFIDENCE │
                    │ evidence / quality /     │
                    │ statistical validation   │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ RISK & GOVERNANCE        │
                    │ position / risk / gates  │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ DECISION GOVERNOR        │
                    │ BUY / SELL / WAIT        │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ EXECUTION CONTROL        │
                    │ lifecycle / monitoring /  │
                    │ broker execution gate    │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ AUDIT / TRANSPARENCY     │
                    │ journal / events / reports│
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ MEMORY / LEARNING        │
                    │ outcomes / adaptation    │
                    └────────────┬─────────────┘
                                 │
                                 └──────► feeds future decisions
```

---

# 4. Master Pipeline — The Most Important Architectural Path

The inspected `intelligence/gsis_master_orchestrator.py` constructs the following major components:

1. `ConfigurationControlEngine`
2. `SystemHealthMonitorEngine`
3. `RecoveryControlEngine`
4. `PipelineTelemetryEngine`
5. `GSISMasterIntelligenceAdapter`
6. `RiskPositionEngine`
7. `DecisionGovernorEngine`
8. `TradeLifecycleEngine`
9. `ExecutionControlEngine`
10. `BrokerExecutionGate`
11. `TradeMonitorEngine`
12. `TradeManagementEngine`
13. `TradeAuditEngine`
14. `SignalMemoryEngine`
15. `AutoLearningLoop`

The orchestrator therefore acts as a **system-level composition layer**. It does not itself represent one trading indicator; it coordinates configuration, health, intelligence, risk, decision, execution, monitoring, audit, memory and learning.

A simplified interpretation is:

```text
CONFIG
  ↓
HEALTH / RECOVERY / TELEMETRY
  ↓
INTELLIGENCE
  ↓
RISK
  ↓
DECISION
  ↓
LIFECYCLE
  ↓
EXECUTION
  ↓
BROKER GATE
  ↓
MONITOR / MANAGEMENT
  ↓
AUDIT
  ↓
MEMORY
  ↓
LEARNING
  ↺
```

---

# 5. Subsystem Catalogue

## A. Core Data and Market Acquisition

### `data_engine.py`
Primary market-data acquisition layer. Historical audit evidence shows a Binance client being used to retrieve current XAU-related pricing and server time.

**Pipeline relationship:** upstream source for downstream market processing.

### `candle_engine.py`
Multi-asset / multi-timeframe candle acquisition and storage layer.

**Pipeline relationship:** converts raw market feeds into structured OHLC-style market observations.

### `history_engine.py`
Historical data access / loading engine.

**Pipeline relationship:** supplies historical context to statistics, backtesting, replay and learning.

### `market/`
Repository namespace for market-domain components.

### `intelligence/market_feed_manager.py`
Market-feed management and coordination.

### `intelligence/realtime_data_engine.py`
Real-time market-data processing.

### `intelligence/gsis_live_market_engine.py`
Higher-level live market processing.

### `intelligence/market_replay_controller.py`
Controls replay of historical market conditions.

### `intelligence/market_research_engine.py`
Research-oriented market analysis.

---

# 6. Market Structure Subsystem

These engines attempt to transform raw prices/candles into a structural description of the market.

### `market_structure_engine.py`
Base market-structure analysis.

### `intelligence/market_structure_engine.py`
Institutional market-structure analysis.

### `intelligence/market_structure_intelligence_engine.py`
Higher-level structure interpretation.

### `intelligence/structure_engine.py`
Alternative/general structure-processing implementation.

### `intelligence/structure_engine_v2.py`
Second structural implementation/version.

### `intelligence/structure_intelligence_engine.py`
Structure-to-intelligence transformation.

### `intelligence/structure_break_engine.py`
Break-of-structure event detection.

### `intelligence/institutional_zone_engine.py`
Identification/management of institutional price zones.

### `intelligence/order_block_engine.py`
Order-block identification.

### `intelligence/order_block_quality_engine.py`
Quality scoring of order blocks.

### `intelligence/smc_structure_engine.py`
Smart-money-concept structural interpretation.

**Pipeline role:** these engines provide structural evidence to intelligence, confluence, signal and decision layers.

---

# 7. Market Regime Subsystem

The purpose of this family is to determine **what kind of market environment currently exists**.

### `regime_engine.py`
Core regime classification.

### `intelligence/market_regime_engine.py`
Market regime classification.

### `intelligence/market_regime_decision_engine.py`
Uses regime information in decision formation.

### `intelligence/market_regime_intelligence_engine.py`
Higher-level regime interpretation.

### `intelligence/market_regime_prediction_engine.py`
Predictive regime analysis.

### `intelligence/market_regime_evolution_engine.py`
Tracks regime transitions/evolution.

### `intelligence/regime_intelligence_engine.py`
Regime intelligence layer.

### `intelligence/market_condition_governor_engine.py`
Uses market conditions as a governance constraint.

### `engines/regime/hmm_regime_model.py`
Hidden-Markov-style regime modelling.

### `engines/regime/market_regime_engine.py`
Alternative market-regime implementation.

### `engines/regime/regime_intelligence_engine.py`
Regime interpretation layer.

### `engines/scoring/regime_score_engine.py`
Regime quality/scoring.

### `engines/learning/regime_feedback.py`
Learning from regime outcomes.

### `engines/learning/regime_memory.py`
Historical regime memory.

**Pipeline role:** regime classification is an early conditioning layer. A setup may be treated differently depending on whether the market is trending, ranging, volatile, transitional, etc.

---

# 8. Liquidity and Order-Flow Subsystem

### `liquidity_engine.py`
Liquidity analysis.

### `intelligence/liquidity_engine.py`
Liquidity intelligence.

### `intelligence/liquidity_intelligence_engine.py`
Higher-level liquidity interpretation.

### `intelligence/liquidity_mapping_engine.py`
Liquidity-location mapping.

### `intelligence/liquidity_sweep_engine.py`
Liquidity sweep detection.

### `intelligence/order_flow_engine.py`
Order-flow analysis.

### `intelligence/order_flow_microstructure_engine.py`
Microstructure-level order-flow analysis.

### `intelligence/order_router.py`
Order-routing abstraction.

### `intelligence/order_slicing_engine.py`
Order slicing / execution fragmentation.

### `intelligence/microstructure_engine.py`
Market microstructure analysis.

### `intelligence/mtf_intelligence_engine.py`
Multi-timeframe intelligence.

### `intelligence/mtf_intelligence_engine_v2.py`
Second multi-timeframe implementation.

### `engines/live/orderflow_aggregator.py`
Aggregates live order-flow information.

### `engines/live/orderflow_bridge.py`
Bridges live order-flow to intelligence.

### `engines/live/orderflow_intelligence.py`
Interprets live order-flow.

### `engines/live/rolling_orderflow_engine.py`
Rolling order-flow calculations.

### `engines/orderflow/order_flow_engine.py`
Order-flow implementation.

### `engines/orderflow/orderflow_engine.py`
Alternative order-flow implementation.

### `engines/order_flow_engine.py`
Root-level order-flow engine.

**Pipeline role:** these engines provide information about liquidity, participation and execution conditions.

---

# 9. Intelligence and Fusion Subsystem

This is the analytical brain of GSIS.

## Core intelligence

### `intelligence/core/gsis_master_intelligence_adapter.py`
Central adapter between GSIS master orchestration and the deeper intelligence engines.

### `intelligence/core/gsis_intelligence_fusion_engine.py`
Combines multiple intelligence signals/evidence streams.

### `intelligence/core/gsis_pattern_probability_engine.py`
Pattern probability analysis.

### `intelligence/core/gsis_confidence_calibration_engine.py`
Calibrates confidence using evidence/statistical history.

### `intelligence/core/gsis_knowledge_engine.py`
Knowledge representation / contextual reasoning.

### `intelligence/core/gsis_historical_statistics_engine.py`
Historical statistical evidence.

### `intelligence/core/gsis_intelligence_pipeline_controller.py`
Coordinates intelligence pipeline stages.

### `intelligence/core/gsis_sqlite_database_engine.py`
SQLite-based persistence for intelligence-related state.

## Other intelligence engines

### `intelligence/intelligence_fusion_core.py`
Core fusion implementation.

### `intelligence/intelligence_fusion_engine.py`
General intelligence fusion.

### `intelligence/multi_agent_intelligence_fusion_engine.py`
Multi-agent intelligence combination.

### `intelligence/confluence_intelligence_engine.py`
Confluence analysis.

### `intelligence/decision_intelligence_engine.py`
Decision-oriented intelligence.

### `intelligence/explainable_ai_engine.py`
Explainability layer.

### `intelligence/autonomous_decision_intelligence_engine.py`
Higher-level autonomous decision intelligence.

### `intelligence/intelligence_manager.py`
General intelligence orchestration.

### `intelligence/intelligence_memory_fusion_engine.py`
Combines current intelligence with historical memory.

### `intelligence/intelligence_memory_writer.py`
Persists intelligence-memory outputs.

### `intelligence/knowledge_graph_engine.py`
Knowledge-graph representation.

### `intelligence/knowledge_memory_engine.py`
Knowledge-memory integration.

### `intelligence/bayesian_engine.py`
Bayesian-style evidence processing.

### `engines/intelligence/bayesian_evidence_engine.py`
Bayesian evidence analysis.

### `engines/intelligence/bayesian_memory_engine.py`
Bayesian memory.

### `engines/intelligence/institutional_score_engine.py`
Institutional scoring.

### `engines/intelligence/trade_brain_engine.py`
Higher-level trade reasoning.

### `engines/intelligence/trade_intelligence_engine.py`
Trade-specific intelligence.

### `engines/intelligence/memory_integration_engine.py`
Memory-to-intelligence integration.

### `engines/intelligence/pattern_learning_engine.py`
Pattern learning.

### `engines/intelligence/perfect_trade_archive_engine.py`
Archive of high-quality/reference outcomes.

### `engines/intelligence/trade_outcome_learning_engine.py`
Learns from completed trades.

**Pipeline role:** transforms raw market facts into structured evidence and confidence.

---

# 10. Pattern and Signal Subsystem

### `intelligence/pattern_engine.py`
General pattern engine.

### `intelligence/pattern_discovery.py`
Pattern discovery.

### `intelligence/pattern_discovery_engine.py`
Pattern discovery implementation.

### `intelligence/pattern_matching_engine.py`
Matches current market states to known patterns.

### `intelligence/pattern_memory_engine.py`
Pattern memory.

### `intelligence/pattern_memory_connector.py`
Connects pattern memory to other subsystems.

### `intelligence/pattern_feedback_engine.py`
Feedback from outcomes to pattern quality.

### `intelligence/pattern_library_engine.py`
Pattern catalogue/library.

### `intelligence/pattern_manager.py`
Pattern lifecycle management.

### `intelligence/pattern_recognition_engine.py`
Pattern recognition.

### `intelligence/pattern_auto_generator.py`
Automated pattern generation.

### `intelligence/signal_generation_engine.py`
Signal generation.

### `intelligence/signal_memory_engine.py`
Signal history/memory.

### `engines/signal/master_signal_engine.py`
Master signal generation.

### `engines/signals/signal_generator.py`
Signal generation implementation.

### `intelligence/supply_demand_engine.py`
Supply/demand signal evidence.

### `intelligence/price_action_intelligence_engine.py`
Price-action intelligence.

**Pipeline role:** creates candidate setups from the market evidence produced upstream.

---

# 11. Statistical and Probability Subsystem

### `statistical_engine.py`
Core statistical processing.

### `intelligence/statistical_engine.py`
Intelligence-level statistical analysis.

### `intelligence/statistical_connector.py`
Connects statistical outputs to intelligence.

### `engines/probability/probability_engine.py`
Probability modelling.

### `intelligence/bayesian_engine.py`
Bayesian evidence.

### `intelligence/gsis_pattern_probability_engine.py`
Pattern probability.

### `intelligence/gsis_confidence_calibration_engine.py`
Confidence calibration.

**Pipeline role:** turns raw scores and observations into probability/confidence evidence rather than relying purely on deterministic indicators.

---

# 12. Risk and Capital Subsystem

This is one of the most important governance layers.

### `intelligence/risk_engine.py`
General risk analysis.

### `intelligence/risk_management_engine.py`
Risk-management policy.

### `intelligence/risk_intelligence_engine.py`
Risk intelligence.

### `intelligence/risk_position_engine.py`
Position-level risk calculation.

### `intelligence/position_sizing_engine.py`
Position sizing.

### `intelligence/capital_management_engine.py`
Capital allocation.

### `intelligence/capital_protection_engine.py`
Capital protection.

### `intelligence/portfolio_engine.py`
Portfolio management.

### `intelligence/portfolio_management_engine.py`
Portfolio-level management.

### `intelligence/portfolio_intelligence_engine.py`
Portfolio intelligence.

### `intelligence/portfolio_risk_governor_engine.py`
Portfolio-level risk governance.

### `intelligence/position_management_engine.py`
Position management.

### `intelligence/position_intelligence_engine.py`
Position intelligence.

### `engines/risk/risk_engine.py`
Risk engine.

### `engines/risk/risk_guard_engine.py`
Risk guard / blocking layer.

### `engines/risk/risk_guard_engine_v1.1_backup.py`
Backup risk guard.

### `engines/risk/risk_guard_engine_v2_backup.py`
Backup risk guard.

### `engines/risk/risk_guard_engine_v2.0_backup.py`
Versioned risk guard backup.

**Pipeline role:** risk is a gate, not merely a score. The constitutional model places risk approval before order submission.

---

# 13. Decision and Governance Subsystem

### `intelligence/decision_engine.py`
General decision logic.

### `intelligence/decision_governor_engine.py`
Central decision governance.

### `intelligence/decision_matrix_engine.py`
Decision matrix logic.

### `intelligence/decision_memory_engine.py`
Historical decision memory.

### `intelligence/decision_explanation_engine.py`
Decision explanations.

### `intelligence/governance_engine.py`
Governance rules.

### `intelligence/final_approval_gate_engine.py`
Final approval gating.

### `intelligence/final_execution_governor_engine.py`
Final execution governance.

### `intelligence/execution_governor.py`
Execution governance.

### `intelligence/market_condition_governor_engine.py`
Market-condition governance.

**Pipeline role:** this is where evidence, confidence and risk become an authorized trading decision.

---

# 14. Execution Subsystem

### `intelligence/execution_engine.py`
Execution logic.

### `intelligence/execution_control_engine.py`
Controls execution.

### `intelligence/execution_coordinator.py`
Coordinates execution steps.

### `intelligence/execution_orchestrator.py`
Execution orchestration.

### `intelligence/execution_optimizer.py`
Execution optimization.

### `intelligence/execution_timing_engine.py`
Execution timing.

### `intelligence/execution_cost_engine.py`
Execution-cost analysis.

### `intelligence/execution_risk_adapter.py`
Risk-to-execution adapter.

### `intelligence/execution_quality_scoring_engine.py`
Execution-quality scoring.

### `intelligence/execution_performance_engine.py`
Execution performance.

### `intelligence/execution_analytics_engine.py`
Execution analytics.

### `intelligence/execution_compliance_engine.py`
Execution compliance.

### `intelligence/execution_context.py`
Execution context.

### `intelligence/execution_intelligence_engine.py`
Execution intelligence.

### `intelligence/execution_learning_engine.py`
Execution learning.

### `intelligence/execution_memory_engine.py`
Execution memory.

### `intelligence/execution_monitoring_engine.py`
Execution monitoring.

### `intelligence/execution_pattern_engine.py`
Execution pattern analysis.

### `intelligence/execution_queue_engine.py`
Execution queue handling.

### `intelligence/execution_recovery_engine.py`
Execution recovery.

### `intelligence/execution_simulation_engine.py`
Execution simulation.

### `intelligence/execution_simulator.py`
Execution simulator.

### `intelligence/execution_strategy_manager.py`
Execution strategy management.

### `intelligence/broker_adapter_engine.py`
Broker abstraction.

### `intelligence/broker_execution_gate.py`
Broker-level final execution gate.

### `engines/execution/execution_bridge_engine.py`
Execution bridge.

### `engines/execution/execution_engine.py`
Execution implementation.

### `engines/execution/execution_safety_engine.py`
Execution safety.

### `engines/execution/mt5_connector.py`
MetaTrader 5 connector.

**Pipeline role:** translates an approved decision into controlled broker interaction.

---

# 15. Trade Lifecycle and Management Subsystem

The constitution defines a lifecycle approximately as:

```text
WAIT
 → SIGNAL_DETECTED
 → QUALIFIED
 → RISK_APPROVED
 → ORDER_SUBMITTED
 → ORDER_FILLED
 → TP1
 → BREAK EVEN
 → TP2
 → TP3
 → TP4
 → COMPLETED
```

### `intelligence/trade_lifecycle_engine.py`
Core trade-state lifecycle.

### `intelligence/trade_management_engine.py`
Active trade management.

### `intelligence/trade_monitor_engine.py`
Trade monitoring.

### `intelligence/trade_orchestrator.py`
Trade orchestration.

### `intelligence/trade_planner_engine.py`
Trade planning.

### `intelligence/trade_setup_engine.py`
Trade setup formation.

### `intelligence/trade_validator_engine.py`
Trade validation.

### `intelligence/trade_quality_scoring_engine.py`
Trade quality scoring.

### `intelligence/trade_safety_governor_engine.py`
Trade safety governance.

### `engines/trade/trade_lifecycle_engine.py`
Alternative lifecycle implementation.

### `engines/trade/trade_management_engine.py`
Alternative trade-management implementation.

### `engines/trade/trade_management_engine_v1_backup.py`
Backup trade-management implementation.

### `engines/trade_manager/trade_lifecycle_manager.py`
Lifecycle manager.

### `engines/trade_manager/trade_manager.py`
Trade manager.

**Pipeline role:** converts an order into a stateful institutional trade object and maintains its state until completion.

---

# 16. Audit, Transparency and Reporting Subsystem

### `intelligence/trade_audit_engine.py`
Trade audit.

### `intelligence/audit_compliance_engine.py`
Compliance-oriented auditing.

### `intelligence/trade_journal_engine.py`
Trade journal.

### `engines/journal/journal_engine.py`
Journal implementation.

### `engines/transparency/event_validator.py`
Validates transparency events.

### `engines/transparency/execution_event_bridge.py`
Bridges execution events into transparency.

### `engines/transparency/telegram_delivery_engine.py`
Delivers transparency/reporting events through Telegram.

### `engines/transparency/trade_transparency_engine.py`
Trade transparency.

### `engines/report/report_engine.py`
Report generation.

### `engines/reporting/report_engine.py`
Reporting implementation.

### `engines/reporting/monthly_report_engine.py`
Monthly reporting.

### `engines/reporting/report_integration_engine.py`
Report integration.

**Pipeline role:** creates the institutional evidence trail required to reconstruct why a decision happened, what was executed, and what happened afterward.

---

# 17. Memory and Learning Subsystem

### `intelligence/memory_bridge.py`
Connects current pipeline components with memory.

### `intelligence/outcome_memory.py`
Outcome storage.

### `intelligence/outcome_memory_engine.py`
Outcome memory processing.

### `intelligence/context_memory_engine.py`
Context memory.

### `intelligence/feature_memory.py`
Feature memory.

### `intelligence/feature_memory_engine.py`
Feature memory engine.

### `intelligence/decision_memory_engine.py`
Decision memory.

### `intelligence/execution_memory_engine.py`
Execution memory.

### `intelligence/intelligence_memory_fusion_engine.py`
Intelligence-memory fusion.

### `intelligence/intelligence_memory_writer.py`
Memory persistence.

### `intelligence/knowledge_memory_engine.py`
Knowledge memory.

### `intelligence/pattern_memory_engine.py`
Pattern memory.

### `intelligence/signal_memory_engine.py`
Signal memory.

### `intelligence/adaptive_learning_engine.py`
Adaptive learning.

### `intelligence/learning_engine.py`
Learning engine.

### `intelligence/ai_learning_engine.py`
AI-oriented learning.

### `intelligence/execution_learning_engine.py`
Execution learning.

### `intelligence/strategy_evolution_engine.py`
Strategy evolution.

### `intelligence/strategy_adaptation_engine.py`
Strategy adaptation.

### `intelligence/strategy_optimization_engine.py`
Strategy optimization.

### `intelligence/optimization_intelligence_engine.py`
Optimization intelligence.

### `intelligence/auto_learning_loop.py`
Continuous learning loop.

### `engines/learning/outcome_tracker.py`
Tracks outcomes.

### `engines/learning/pattern_memory.py`
Pattern memory.

### `engines/learning/regime_feedback.py`
Regime feedback.

### `engines/learning/regime_memory.py`
Regime memory.

**Pipeline role:** closes the loop. Completed trades become evidence for future confidence, pattern quality, regime interpretation and strategy adaptation.

---

# 18. Recovery, Health and Resilience Subsystem

### `intelligence/system_health_monitor_engine.py`
System health.

### `intelligence/recovery_control_engine.py`
Recovery control.

### `intelligence/failsafe_recovery_engine.py`
Fail-safe recovery.

### `intelligence/execution_recovery_engine.py`
Execution recovery.

### `intelligence/disaster_recovery_engine.py`
System-level disaster recovery.

### `intelligence/health_recovery_engine.py`
Health-driven recovery.

### `engines/recovery/trade_recovery_engine.py`
Trade recovery.

### `engines/system/auto_recovery_engine.py`
Automatic recovery.

### `engines/system/background_guard.py`
Background protection.

### `engines/system/process_lock.py`
Process locking.

### `engines/system/service_supervisor.py`
Service supervision.

### `engines/system/watchdog_engine.py`
Watchdog.

### `engines/supervisor/watchdog.py`
Supervisor watchdog.

### `engines/supervisor/health_monitor.py`
Supervisor health monitoring.

**Pipeline role:** prevents a strategy decision from being treated as valid when the surrounding system is unhealthy.

---

# 19. Configuration and Control Subsystem

### `intelligence/configuration_control_engine.py`
Central runtime configuration control.

### `intelligence/config/gsis_config.py`
Configuration engine. An audit run reported the engine as READY and detected configured market-data/news API keys.

### `config/`
Repository configuration package.

Historical configuration inventories include trading, risk, execution and symbol configuration components.

**Pipeline role:** supplies controlled configuration and environment-dependent values.

---

# 20. Telemetry and System Observability

### `intelligence/pipeline_telemetry_engine.py`
Pipeline telemetry.

### `intelligence/system_supervisor_engine.py`
System supervision.

### `intelligence/system_info.py`
System/environment information.

### `engines/supervisor/engine_registry.py`
Registry of engines.

### `engines/supervisor/gsis_core.py`
Core supervisory layer.

### `engines/supervisor/gsis_launcher.py`
System launcher.

### `engines/supervisor/gsis_supervisor.py`
Supervisory controller.

### `engines/supervisor/orchestrator.py`
Supervisor-level orchestration.

**Pipeline role:** observes and coordinates the system around the trading pipeline.

---

# 21. Validation and Testing Subsystem

### `validation_engine.py`
General validation.

### `intelligence/backtesting_validation_engine.py`
Backtest validation.

### `intelligence/strategy_validation_engine.py`
Strategy validation.

### `engines/validation/market_validation_engine.py`
Market validation.

### `engines/validation/outcome_validator.py`
Outcome validation.

Repository inventories also show tests for:

- broker synchronization,
- execution chain,
- market microstructure,
- multi-broker execution,
- position management,
- trade recovery,
- decision pipeline,
- intelligence pipeline,
- order flow,
- state,
- volume profile,
- symbol configuration,
- XAU live connectivity.

**Pipeline role:** validates assumptions and outcomes rather than allowing every model output to be treated as truth.

---

# 22. Market Data and Exchange/Broker Connectors

Observed external integrations include:

- Binance client / `python_binance`
- MetaTrader 5 connector
- WebSocket clients
- HTTP/API clients
- external market-data/news APIs through configuration.

The repository architecture therefore appears designed to separate:

```text
DATA SOURCE
    ↓
ADAPTER / CONNECTOR
    ↓
NORMALIZED MARKET EVENT
    ↓
INTELLIGENCE
```

This abstraction is important for future multi-broker and multi-market expansion.

---

# 23. Database and Persistence

Observed persistence technologies/components include:

- SQLite,
- database namespaces,
- historical storage,
- memory storage,
- intelligence database engine,
- trade/event memory.

The design implies several classes of persistence:

1. Market history
2. Trade history
3. Decision evidence
4. Signal memory
5. Pattern memory
6. Outcome memory
7. Intelligence state
8. Audit records
9. Telemetry/recovery state

---

# 24. Complete Legacy/Parallel Engine Family

The repository contains a significant number of overlapping implementations, backups and historical versions.

Examples include:

- `gsis_master_orchestrator_backup.py`
- `gsis_master_orchestrator_v3_backup.py`
- `gsis_master_orchestrator_v4_error_backup.py`
- `gsis_master_intelligence_adapter_backup.py`
- `gsis_master_intelligence_adapter_backup_v7.py`
- `gsis_pattern_probability_engine_backup.py`
- `gsis_pattern_probability_engine_backup_v2.py`
- `gsis_confidence_calibration_engine_backup.py`
- `risk_guard_engine_v1.1_backup.py`
- `risk_guard_engine_v2_backup.py`
- `risk_guard_engine_v2.0_backup.py`
- `trade_management_engine_v1_backup.py`
- `execution_gate_v1.2_backup.py`

These files should be treated as **architectural evidence**, not automatically as active production components.

A future audit should distinguish:

```text
ACTIVE
EXPERIMENTAL
LEGACY
BACKUP
TEST
DEAD / ORPHANED
```

rather than deleting them prematurely.

---

# 25. Dependency Architecture

Observed external Python packages include:

- `numpy`
- `requests`
- `python-dotenv`
- `python-binance`
- `websocket-client`
- `websockets`
- `aiohttp`
- `dateparser`
- `pytz`
- `pycryptodome`
- related HTTP/async dependencies.

A repository import audit also identified `MetaTrader5` as an external dependency expected by parts of the codebase.

Important distinction:

### Python standard library
Examples:

- `os`
- `sys`
- `datetime`
- `json`
- `logging`
- `sqlite3`
- `statistics`
- `subprocess`
- `socket`
- `urllib`
- `uuid`
- `hashlib`
- `fcntl`

These do not normally belong in `requirements.txt`.

### External dependencies
These must be installed in a fresh environment when actually imported by active code.

### Local modules
Imports such as:

- `risk_position_engine`
- `trade_lifecycle_engine`
- `configuration_control_engine`
- `pipeline_telemetry_engine`

are not PyPI packages. They are GSIS repository modules.

This distinction prevented a major false diagnosis during the audit: several imports were initially reported as missing because the audit searched only the Python path rather than recursively locating local repository files. The later module-location audit showed the majority of those engines do exist under `intelligence/` or `intelligence/core/`.

---

# 26. Master-Orchestrator Dependency Map

The inspected master orchestrator directly depends on:

```text
gsis_master_intelligence_adapter
risk_position_engine
decision_governor_engine
trade_lifecycle_engine
execution_control_engine
broker_execution_gate
trade_monitor_engine
trade_management_engine
trade_audit_engine
signal_memory_engine
auto_learning_loop
system_health_monitor_engine
configuration_control_engine
recovery_control_engine
pipeline_telemetry_engine
```

Their conceptual dependency chain is:

```text
GSISMasterIntelligenceAdapter
            │
            ▼
     RiskPositionEngine
            │
            ▼
   DecisionGovernorEngine
            │
            ▼
   TradeLifecycleEngine
            │
            ▼
   ExecutionControlEngine
            │
            ▼
    BrokerExecutionGate
            │
            ├──────────────► TradeMonitorEngine
            │
            ├──────────────► TradeManagementEngine
            │
            └──────────────► TradeAuditEngine
                              │
                              ▼
                      SignalMemoryEngine
                              │
                              ▼
                       AutoLearningLoop
```

Cross-cutting controls:

```text
ConfigurationControlEngine
SystemHealthMonitorEngine
RecoveryControlEngine
PipelineTelemetryEngine
```

These operate across the entire pipeline.

---

# 27. Institutional Decision Lifecycle

The intended decision lifecycle can be reconstructed as:

## Stage 1 — Observe
Collect prices, candles, historical data, order flow and market events.

## Stage 2 — Normalize
Convert raw source data into a common representation.

## Stage 3 — Understand
Determine structure, regime, liquidity, volatility and market condition.

## Stage 4 — Generate evidence
Identify patterns, supply/demand, order blocks, momentum, divergence and other signals.

## Stage 5 — Fuse
Combine independent evidence sources.

## Stage 6 — Score
Calculate quality, probability and confidence.

## Stage 7 — Validate
Compare the setup against historical statistics and rules.

## Stage 8 — Risk approve
Determine whether the trade is acceptable from a capital/position perspective.

## Stage 9 — Govern
Produce the authoritative BUY, SELL or WAIT decision.

## Stage 10 — Execute
Control order creation, timing, routing and broker interaction.

## Stage 11 — Manage
Track position state, stops, targets, break-even and lifecycle.

## Stage 12 — Audit
Record why the trade happened, what happened and whether rules were followed.

## Stage 13 — Learn
Feed outcome information into memory and future confidence.

---

# 28. What GSIS Is Trying to Prevent

The architecture appears designed to prevent several common failure modes:

### 1. Single-indicator decisions
Solved by multi-engine intelligence/fusion.

### 2. Uncontrolled execution
Solved by execution control and broker gates.

### 3. Oversized positions
Solved by position/risk engines.

### 4. Unexplained trades
Solved by decision explanation, audit and transparency engines.

### 5. Forgetting historical outcomes
Solved by memory and learning engines.

### 6. Trading in the wrong market regime
Solved by regime and market-condition engines.

### 7. System failure during trading
Solved by health, recovery and watchdog engines.

### 8. Strategy drift without evidence
Solved by statistical validation and learning controls.

### 9. Lack of institutional accountability
Solved by audit, journal, event and reporting subsystems.

---

# 29. Important Architectural Observation

GSIS is not one algorithm.

It is a **large collection of specialized decision services/engines** organized around a governance pipeline.

The repository contains multiple generations of architecture. Therefore:

```text
Repository size ≠ active runtime size
```

and:

```text
Number of engines ≠ number of engines executed per trade
```

The master orchestrator is the strongest evidence for the active conceptual pipeline. Other engines may be supporting, experimental, legacy, test, backup or currently orphaned.

---

# 30. Audit Classification Recommended

For future repository governance, every engine should receive one status:

| Status | Meaning |
|---|---|
| ACTIVE | Imported/reached by active production path |
| SUPPORT | Required by an active engine |
| EXPERIMENTAL | Present but not production-critical |
| LEGACY | Historical implementation retained for reference |
| BACKUP | Explicit backup/version |
| TEST | Used by tests only |
| ORPHANED | No current consumer discovered |
| UNKNOWN | Requires runtime tracing |

The catalogue should eventually contain these columns:

```text
Engine
Path
Subsystem
Purpose
Imports
Imported By
Produces
Consumed By
Runtime Status
Version
Backup/Legacy?
Persistence
External Dependencies
Risk Level
Tests
```

---

# 31. Recommended Canonical Repository Structure

The current repository contains many overlapping engine families. A future refactor should not begin by deleting code.

Instead, establish a manifest:

```text
docs/
    GSIS_ARCHITECTURE.md
    GSIS_ENGINE_CATALOGUE.md
    GSIS_DEPENDENCY_MAP.md
    GSIS_DECISION_FLOW.md
    GSIS_AUDIT_MODEL.md

architecture/
    engine_registry.yaml
    pipeline_manifest.yaml

tests/
    architecture/
    integration/
    execution/
    risk/
    data/

engines/
    data/
    market/
    intelligence/
    probability/
    risk/
    decision/
    execution/
    trade/
    audit/
    learning/
    recovery/
```

The current modules can then be mapped into this logical architecture without immediately destroying historical evidence.

---

# 32. The True Reverse-Engineering Map

At the highest level:

```text
                           GSIS INSTITUTIONAL
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
           DATA                 GOVERNANCE          RESILIENCE
              │                    │                    │
       market feeds          configuration          health
       candles               decision rules         recovery
       history               risk policy            watchdogs
              │                    │                    │
              └──────────────┬─────┴────────────────────┘
                             │
                         INTELLIGENCE
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
       structure           regime            liquidity
          │                  │                  │
       patterns           order flow         microstructure
          └──────────────────┼──────────────────┘
                             │
                         FUSION / SCORE
                             │
                  probability / confidence
                             │
                           RISK
                             │
                       DECISION GOVERNOR
                             │
                        BUY / SELL / WAIT
                             │
                          EXECUTION
                             │
                     BROKER EXECUTION GATE
                             │
                         TRADE LIFECYCLE
                             │
                  ┌──────────┴──────────┐
                  │                     │
              MANAGEMENT             MONITOR
                  │                     │
                  └──────────┬──────────┘
                             │
                           AUDIT
                             │
                         MEMORY
                             │
                         LEARNING
                             │
                             └──────────────► future decisions
```

This feedback loop is the defining characteristic of the institutional architecture.

---

# 33. Final Assessment

The repository demonstrates an ambitious architecture for an institutional trading decision platform with five major characteristics:

1. **Separation of responsibilities**  
   Market data, intelligence, risk, execution, audit and learning are represented as separate engines.

2. **Decision governance**  
   The architecture attempts to prevent raw signals from directly becoming broker orders.

3. **Risk-first execution**  
   Position and risk controls sit between intelligence and execution.

4. **Full lifecycle accountability**  
   A trade is treated as a stateful object from detection through completion.

5. **Closed-loop learning**  
   Outcomes are intended to feed memory, statistical calibration and future decisions.

The main engineering challenge is therefore no longer simply "add another strategy." The major challenge is **architecture consolidation and runtime verification**:

- identify the canonical production path;
- identify which engines are actually live;
- remove or quarantine duplicate implementations;
- establish a formal engine registry;
- generate deterministic dependency graphs;
- pin dependencies;
- add integration tests;
- verify secrets/configuration;
- document every input/output contract;
- trace one complete trade end-to-end.

Once those steps are complete, GSIS can be represented not merely as a collection of Python files, but as a formally documented **institutional decision system with an auditable execution graph**.

---

# 34. Audit Evidence

The reverse-engineering effort has been supported by:

- the GSIS Constitution;
- repository engine inventories;
- import audits;
- dependency audits;
- master-orchestrator source inspection;
- module-location audits;
- historical architecture listings;
- configuration-engine execution;
- repository Git history and branch state.

The constitution is especially important because it defines the intended institutional behavior: only GSIS Core may issue BUY/SELL/WAIT, decisions must be explainable, trades have a defined lifecycle, and every engine must have a defined responsibility.

---

## Appendix A — Key Files to Protect

At minimum, retain:

```text
intelligence/gsis_master_orchestrator.py
intelligence/core/gsis_master_intelligence_adapter.py
intelligence/core/gsis_intelligence_fusion_engine.py
intelligence/core/gsis_confidence_calibration_engine.py
intelligence/core/gsis_pattern_probability_engine.py

intelligence/risk_position_engine.py
intelligence/decision_governor_engine.py
intelligence/trade_lifecycle_engine.py
intelligence/execution_control_engine.py
intelligence/broker_execution_gate.py
intelligence/trade_monitor_engine.py
intelligence/trade_management_engine.py
intelligence/trade_audit_engine.py
intelligence/signal_memory_engine.py
intelligence/auto_learning_loop.py

intelligence/system_health_monitor_engine.py
intelligence/configuration_control_engine.py
intelligence/recovery_control_engine.py
intelligence/pipeline_telemetry_engine.py

GSIS_IMPORT_AUDIT.txt
GSIS_DEPENDENCY_AUDIT.txt
```

---

## Appendix B — Security Rule

Never commit:

```text
.env
API keys
broker passwords
private keys
tokens
database credentials
Telegram bot tokens
exchange secrets
```

The repository should contain configuration templates and documentation, while real secrets remain outside Git.

---

## Appendix C — Next Audit Milestone

The next authoritative reverse-engineering step is **runtime tracing**:

```text
START
  ↓
identify actual launcher
  ↓
load master controller
  ↓
trace imports
  ↓
trace object construction
  ↓
trace method calls
  ↓
trace data objects
  ↓
trace decision object
  ↓
trace risk approval
  ↓
trace execution
  ↓
trace lifecycle
  ↓
trace audit
  ↓
trace memory
  ↓
trace learning
  ↓
END
```

That will convert this catalogue from a static filename/function inference into a verified runtime architecture map.

---

**End of GSIS INSTITUTIONAL Reverse-Engineering Catalogue**
