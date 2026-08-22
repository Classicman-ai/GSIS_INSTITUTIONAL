# GSIS INSTITUTIONAL

## Canonical runtime

GSIS has one production runtime: `institutional.GSISUnifiedEngine`.

The MT5 execution/intelligence path remains separate from the external CME/COMEX intelligence path.

## Market-data source separation

### MT5 Order Flow

The existing GSIS Order Flow Engine remains **MT5-data driven**. It consumes data from `MT5_UNIVERSAL_CONNECTOR` and must not be confused with CME intelligence.

### CME/COMEX Market Microstructure

CME intelligence is implemented separately as:

`adapters/cme/databento_live.py -> volume_intelligence/cme_market_microstructure.py`

The CME adapter is the only layer responsible for external CME connectivity. The microstructure engine is a pure consumer/calculator: it receives normalized CME trades, MBP-10 levels, and MBO events and contains no market prices, synthetic orders, or feed credentials.

### Volume Profile categories

**Category A — Price-independent**

- POC
- VAH / VAL
- HVN / LVN
- Volume concentration
- Trade volume
- Delta / participation
- Value migration

**Category B — Price-dependent**

- CME POC/VAH/VAL translated into MT5 price space
- CME HVN/LVN translated into MT5 price space
- CME-to-MT5 basis
- Basis mean/std/z-score
- Stability gate

Category B is disabled unless the external CME and MT5 prices demonstrate a valid, stable relationship.

## External CME data

GSIS currently provides a Databento adapter for CME Globex data. Databento documents MBO as L3/full order-book data, MBP-10 as L2 top-ten market depth, and trades as tick-by-tick executions. citeturn1search1turn0search1

Configure the provider through `.env` variables from `.env.example`. No CME market data is hardcoded in the production intelligence engines.

Install the optional provider dependency:

```bash
pip install -r requirements-cme.txt
```

The adapter subscribes to externally configured `mbo`, `mbp-10`, and `trades` schemas and forwards normalized records into GSIS. Databento's live API supports multiple schemas in one session and MBO snapshots for initial book state. citeturn0search0turn0search8

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

A static pass alone is not a claim of live broker connectivity or live CME connectivity.
