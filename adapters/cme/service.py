from __future__ import annotations

import os
from collections import deque
from dataclasses import dataclass

from volume_intelligence.cme_market_microstructure import (
    CMEBookEvent,
    CMEBookLevel,
    CMETrade,
    CMEMarketMicrostructureEngine,
    CMEMicrostructureSignal,
)

from .databento_live import CMEDataSourceConfig, DatabentoCMEDataSource


@dataclass(frozen=True)
class CMEMicrostructureConfig:
    max_score: float
    depth_imbalance_threshold: float
    delta_ratio_threshold: float
    absorption_threshold: float
    withdrawal_threshold: float
    buffer_size: int = 5000

    @classmethod
    def from_environment(cls) -> "CMEMicrostructureConfig":
        def required_float(name: str) -> float:
            value = os.getenv(name, "").strip()
            if not value:
                raise RuntimeError(f"Missing runtime configuration: {name}")
            return float(value)

        return cls(
            max_score=required_float("GSIS_CME_MICROSTRUCTURE_MAX_SCORE"),
            depth_imbalance_threshold=required_float("GSIS_CME_DEPTH_IMBALANCE_THRESHOLD"),
            delta_ratio_threshold=required_float("GSIS_CME_DELTA_RATIO_THRESHOLD"),
            absorption_threshold=required_float("GSIS_CME_ABSORPTION_THRESHOLD"),
            withdrawal_threshold=required_float("GSIS_CME_WITHDRAWAL_THRESHOLD"),
            buffer_size=int(os.getenv("GSIS_CME_MICROSTRUCTURE_BUFFER_SIZE", "5000")),
        )


class CMEIntelligenceService:
    """
    External-data orchestration boundary for CME intelligence.

    MBP-10 is a current-depth observation, so the service keeps the latest
    externally supplied levels per instrument/depth instead of accumulating
    historical levels as if they were simultaneous liquidity.
    """

    def __init__(
        self,
        source: DatabentoCMEDataSource,
        engine: CMEMarketMicrostructureEngine,
        buffer_size: int,
    ) -> None:
        if buffer_size <= 0:
            raise ValueError("buffer_size must be > 0")
        self.source = source
        self.engine = engine
        self._levels: dict[tuple[int, str, int], CMEBookLevel] = {}
        self.events: deque[CMEBookEvent] = deque(maxlen=buffer_size)
        self.trades: deque[CMETrade] = deque(maxlen=buffer_size)
        self.latest_signal: CMEMicrostructureSignal | None = None

        source.on_book_level = self._on_book_level
        source.on_book_event = self._on_book_event
        source.on_trade = self._on_trade

    @property
    def levels(self) -> tuple[CMEBookLevel, ...]:
        return tuple(self._levels.values())

    def _on_book_level(self, value: CMEBookLevel) -> None:
        key = (value.instrument_id, value.side, value.depth)
        self._levels[key] = value
        self._recalculate()

    def _on_book_event(self, value: CMEBookEvent) -> None:
        self.events.append(value)
        self._recalculate()

    def _on_trade(self, value: CMETrade) -> None:
        self.trades.append(value)
        self._recalculate()

    def _recalculate(self) -> None:
        if not self._levels and not self.events and not self.trades:
            return
        self.latest_signal = self.engine.analyze(
            levels=self.levels,
            events=self.events,
            trades=self.trades,
        )

    def run(self, *, start: str | None = None, snapshot: bool = True) -> None:
        self.source.stream(start=start, snapshot=snapshot)

    def stop(self) -> None:
        self.source.stop()


def build_cme_intelligence_service() -> CMEIntelligenceService:
    source_config = CMEDataSourceConfig.from_environment()
    microstructure_config = CMEMicrostructureConfig.from_environment()
    source = DatabentoCMEDataSource(source_config)
    engine = CMEMarketMicrostructureEngine(
        max_score=microstructure_config.max_score,
        depth_imbalance_threshold=microstructure_config.depth_imbalance_threshold,
        delta_ratio_threshold=microstructure_config.delta_ratio_threshold,
        absorption_threshold=microstructure_config.absorption_threshold,
        withdrawal_threshold=microstructure_config.withdrawal_threshold,
    )
    return CMEIntelligenceService(source, engine, microstructure_config.buffer_size)
