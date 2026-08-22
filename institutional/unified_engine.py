from __future__ import annotations

import importlib
import json
import math
import os
import sys
import time
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Optional


@dataclass(frozen=True)
class GSISConfig:
    symbols: tuple[str, ...]
    timeframes: tuple[str, ...]
    loop_interval_seconds: float
    history_count: int
    risk_per_trade: float
    atr_multiplier: float
    reward_multiple: float
    minimum_signal_score: float
    execution_enabled: bool
    database_path: Path
    mt5_connector_path: Path

    @classmethod
    def from_env(cls) -> "GSISConfig":
        def required(name: str) -> str:
            value = os.getenv(name, "").strip()
            if not value:
                raise RuntimeError(f"Missing required environment variable: {name}")
            return value

        def csv(name: str) -> tuple[str, ...]:
            values = tuple(x.strip().upper() for x in required(name).split(",") if x.strip())
            if not values:
                raise RuntimeError(f"Environment variable {name} must contain at least one value")
            return values

        def positive_float(name: str) -> float:
            value = float(required(name))
            if not math.isfinite(value) or value <= 0:
                raise RuntimeError(f"{name} must be a finite positive number")
            return value

        def positive_int(name: str) -> int:
            value = int(required(name))
            if value <= 0:
                raise RuntimeError(f"{name} must be a positive integer")
            return value

        def boolean(name: str) -> bool:
            value = required(name).lower()
            if value not in {"true", "false"}:
                raise RuntimeError(f"{name} must be true or false")
            return value == "true"

        connector_path = Path(required("GSIS_MT5_CONNECTOR_PATH")).expanduser().resolve()
        if not connector_path.exists():
            raise RuntimeError(f"MT5 connector path does not exist: {connector_path}")

        database_path = Path(required("GSIS_DATABASE_PATH")).expanduser().resolve()

        return cls(
            symbols=csv("GSIS_SYMBOLS"),
            timeframes=csv("GSIS_TIMEFRAMES"),
            loop_interval_seconds=positive_float("GSIS_LOOP_INTERVAL_SECONDS"),
            history_count=positive_int("GSIS_HISTORY_COUNT"),
            risk_per_trade=positive_float("GSIS_RISK_PER_TRADE"),
            atr_multiplier=positive_float("GSIS_ATR_MULTIPLIER"),
            reward_multiple=positive_float("GSIS_REWARD_MULTIPLE"),
            minimum_signal_score=float(required("GSIS_MINIMUM_SIGNAL_SCORE")),
            execution_enabled=boolean("GSIS_EXECUTION_ENABLED"),
            database_path=database_path,
            mt5_connector_path=connector_path,
        )


class MT5UniversalConnectorAdapter:
    """Use the existing MT5_UNIVERSAL_CONNECTOR as the sole market-data source."""

    def __init__(self, connector_path: Path) -> None:
        path = str(connector_path)
        if path not in sys.path:
            sys.path.insert(0, path)
        module = importlib.import_module("connector.mt5_connector")
        self.connector = module.MT5Connector()

    def connect(self) -> None:
        if not self.connector.connect():
            raise RuntimeError(f"MT5 connection failed: {self.connector.last_error}")

    def tick(self, symbol: str) -> dict[str, Any]:
        value = self.connector.get_tick(symbol)
        if value is None:
            raise RuntimeError(f"Live tick unavailable for {symbol}: {self.connector.last_error}")
        return value

    def rates(self, symbol: str, timeframe: str, count: int) -> Any:
        value = self.connector.get_rates(symbol, timeframe, count)
        if value is None or len(value) == 0:
            raise RuntimeError(
                f"Live historical data unavailable for {symbol}/{timeframe}: {self.connector.last_error}"
            )
        return value

    def account(self) -> dict[str, Any]:
        value = self.connector.get_account_info()
        if value is None:
            raise RuntimeError(f"Account data unavailable: {self.connector.last_error}")
        return value

    def symbol_info(self, symbol: str) -> dict[str, Any]:
        value = self.connector.get_symbol_info(symbol)
        if value is None:
            raise RuntimeError(f"Symbol metadata unavailable for {symbol}: {self.connector.last_error}")
        return value

    def execute(self, symbol: str, side: str, volume: float, sl: float, tp: float) -> dict[str, Any]:
        if side == "BUY":
            return self.connector.buy(symbol, volume, sl=sl, tp=tp)
        if side == "SELL":
            return self.connector.sell(symbol, volume, sl=sl, tp=tp)
        raise ValueError(f"Unsupported execution side: {side}")

    def status(self) -> dict[str, Any]:
        return self.connector.status()


class UnifiedOrderFlowEngine:
    """Canonical order-flow engine. It consumes broker candle data only."""

    name = "GSIS_UNIFIED_ORDER_FLOW"

    def calculate(self, rates: Any) -> dict[str, Any]:
        rows = list(rates)
        if len(rows) < 2:
            raise RuntimeError("Insufficient broker candle data for order-flow calculation")

        buy_volume = 0.0
        sell_volume = 0.0
        bullish = 0
        bearish = 0
        ranges: list[float] = []
        bodies: list[float] = []

        for row in rows:
            opening = float(row["open"])
            closing = float(row["close"])
            high = float(row["high"])
            low = float(row["low"])
            names = getattr(getattr(row, "dtype", None), "names", None) or ()
            volume_field = "tick_volume" if "tick_volume" in names else "volume"
            volume = float(row[volume_field])
            candle_range = max(high - low, 0.0)
            ranges.append(candle_range)
            bodies.append(abs(closing - opening))
            if closing > opening:
                buy_volume += volume
                bullish += 1
            elif closing < opening:
                sell_volume += volume
                bearish += 1
            else:
                buy_volume += volume / 2.0
                sell_volume += volume / 2.0

        total = buy_volume + sell_volume
        if total <= 0:
            raise RuntimeError("Broker supplied candles contain no usable volume")

        delta = (buy_volume - sell_volume) / total
        latest = rows[-1]
        latest_range = max(float(latest["high"]) - float(latest["low"]), 0.0)
        latest_body = abs(float(latest["close"]) - float(latest["open"]))
        average_range = mean(ranges)
        body_strength = latest_body / latest_range if latest_range > 0 else 0.0

        return {
            "buy_volume": buy_volume,
            "sell_volume": sell_volume,
            "delta": delta,
            "bullish_candles": bullish,
            "bearish_candles": bearish,
            "average_range": average_range,
            "body_strength": body_strength,
        }


class UnifiedMarketIntelligenceEngine:
    """Canonical market interpretation from broker candles and live tick data."""

    name = "GSIS_UNIFIED_MARKET_INTELLIGENCE"

    def analyze(self, rates: Any, order_flow: dict[str, Any]) -> dict[str, Any]:
        rows = list(rates)
        closes = [float(row["close"]) for row in rows]
        highs = [float(row["high"]) for row in rows]
        lows = [float(row["low"]) for row in rows]
        if len(closes) < 2:
            raise RuntimeError("Insufficient broker candles for market intelligence")

        first = closes[0]
        last = closes[-1]
        direction = "BUY" if last > first else "SELL" if last < first else "WAIT"
        movement = abs(last - first)
        ranges = [max(h - l, 0.0) for h, l in zip(highs, lows)]
        atr = mean(ranges)
        score = abs(order_flow["delta"])
        if movement > atr:
            score += movement / atr if atr > 0 else 0.0

        return {
            "direction": direction,
            "first_close": first,
            "last_close": last,
            "movement": movement,
            "atr": atr,
            "score": score,
            "order_flow": order_flow,
        }


class UnifiedRiskEngine:
    name = "GSIS_UNIFIED_RISK"

    def size(
        self,
        account: dict[str, Any],
        symbol_info: dict[str, Any],
        entry: float,
        stop: float,
        risk_fraction: float,
    ) -> float:
        equity = float(account.get("equity") or 0.0)
        tick_size = float(symbol_info.get("trade_tick_size") or 0.0)
        tick_value = float(symbol_info.get("trade_tick_value") or 0.0)
        volume_min = float(symbol_info.get("volume_min") or 0.0)
        volume_max = float(symbol_info.get("volume_max") or 0.0)
        volume_step = float(symbol_info.get("volume_step") or 0.0)
        distance = abs(entry - stop)

        if equity <= 0 or tick_size <= 0 or tick_value <= 0 or distance <= 0:
            raise RuntimeError("Broker risk metadata is insufficient for position sizing")
        if volume_min <= 0 or volume_max <= 0 or volume_step <= 0:
            raise RuntimeError("Broker volume constraints are unavailable")

        risk_amount = equity * risk_fraction
        ticks = distance / tick_size
        loss_per_lot = ticks * tick_value
        raw_volume = risk_amount / loss_per_lot
        steps = math.floor(raw_volume / volume_step)
        volume = min(steps * volume_step, volume_max)
        if volume < volume_min:
            raise RuntimeError("Calculated position is below the broker minimum volume")
        return volume


class UnifiedPersistence:
    def __init__(self, path: Path) -> None:
        import sqlite3

        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS gsis_cycles (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, symbol TEXT NOT NULL, status TEXT NOT NULL, payload TEXT NOT NULL)"
        )
        self.connection.commit()

    def record(self, symbol: str, status: str, payload: dict[str, Any]) -> None:
        self.connection.execute(
            "INSERT INTO gsis_cycles(timestamp, symbol, status, payload) VALUES(?,?,?,?)",
            (
                datetime.now(timezone.utc).isoformat(),
                symbol,
                status,
                json.dumps(payload, default=str),
            ),
        )
        self.connection.commit()


class GSISUnifiedEngine:
    """Single autonomous GSIS runtime: broker -> analysis -> risk -> execution -> audit -> repeat."""

    name = "GSIS_INSTITUTIONAL_UNIFIED_ENGINE"

    def __init__(self, config: GSISConfig) -> None:
        self.config = config
        self.market = MT5UniversalConnectorAdapter(config.mt5_connector_path)
        self.order_flow = UnifiedOrderFlowEngine()
        self.intelligence = UnifiedMarketIntelligenceEngine()
        self.risk = UnifiedRiskEngine()
        self.persistence = UnifiedPersistence(config.database_path)

    def validate_runtime(self) -> dict[str, Any]:
        self.market.connect()
        account = self.market.account()
        symbols = {}
        for symbol in self.config.symbols:
            tick = self.market.tick(symbol)
            info = self.market.symbol_info(symbol)
            symbols[symbol] = {"tick": tick, "symbol_info": info}
        return {
            "engine": self.name,
            "connector": self.market.status(),
            "account": account,
            "symbols": symbols,
            "execution_enabled": self.config.execution_enabled,
            "status": "READY",
        }

    def cycle(self) -> dict[str, Any]:
        self.market.connect()
        account = self.market.account()
        results: dict[str, Any] = {}

        for symbol in self.config.symbols:
            tick = self.market.tick(symbol)
            symbol_info = self.market.symbol_info(symbol)
            timeframes: dict[str, Any] = {}

            for timeframe in self.config.timeframes:
                rates = self.market.rates(symbol, timeframe, self.config.history_count)
                flow = self.order_flow.calculate(rates)
                intelligence = self.intelligence.analyze(rates, flow)

                decision = "WAIT"
                execution: Optional[dict[str, Any]] = None

                if (
                    intelligence["direction"] != "WAIT"
                    and intelligence["score"] >= self.config.minimum_signal_score
                ):
                    decision = intelligence["direction"]
                    atr = intelligence["atr"]
                    if atr <= 0:
                        raise RuntimeError(f"Cannot derive stop distance for {symbol}/{timeframe}")

                    entry = float(tick["ask"] if decision == "BUY" else tick["bid"])
                    stop_distance = self.config.atr_multiplier * atr
                    target_distance = self.config.reward_multiple * stop_distance
                    stop = entry - stop_distance if decision == "BUY" else entry + stop_distance
                    target = entry + target_distance if decision == "BUY" else entry - target_distance
                    volume = self.risk.size(
                        account,
                        symbol_info,
                        entry,
                        stop,
                        self.config.risk_per_trade,
                    )

                    if self.config.execution_enabled:
                        execution = self.market.execute(
                            symbol,
                            decision,
                            volume,
                            stop,
                            target,
                        )

                snapshot = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "tick": tick,
                    "flow": flow,
                    "intelligence": intelligence,
                    "decision": decision,
                    "execution": execution,
                }
                self.persistence.record(symbol, "COMPLETE", snapshot)
                timeframes[timeframe] = snapshot

            results[symbol] = timeframes

        return {
            "engine": self.name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "CYCLE_COMPLETE",
            "results": results,
        }

    def run_forever(self) -> None:
        self.validate_runtime()
        while True:
            started = time.monotonic()
            try:
                result = self.cycle()
                print(json.dumps(result, default=str))
            except Exception as exc:
                error = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "status": "CYCLE_ERROR",
                    "error": f"{type(exc).__name__}: {exc}",
                    "traceback": traceback.format_exc(),
                }
                self.persistence.record("SYSTEM", "ERROR", error)
                print(json.dumps(error))
            elapsed = time.monotonic() - started
            delay = max(self.config.loop_interval_seconds - elapsed, 0.0)
            time.sleep(delay)
