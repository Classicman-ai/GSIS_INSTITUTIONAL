from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .models import MarketTrade, VolumeProfile, VolumeProfileLevel


class VolumeProfileEngine:
    """Build price-independent volume intelligence from trade-level data."""

    def __init__(self, tick_size: float = 0.10, value_area_fraction: float = 0.70,
                 hvn_percentile: float = 0.80, lvn_percentile: float = 0.20) -> None:
        if tick_size <= 0:
            raise ValueError("tick_size must be > 0")
        if not 0 < value_area_fraction <= 1:
            raise ValueError("value_area_fraction must be in (0, 1]")
        if not 0 <= lvn_percentile < hvn_percentile <= 1:
            raise ValueError("percentiles must satisfy 0 <= LVN < HVN <= 1")
        self.tick_size = tick_size
        self.value_area_fraction = value_area_fraction
        self.hvn_percentile = hvn_percentile
        self.lvn_percentile = lvn_percentile

    def _bucket(self, price: float) -> float:
        return round(round(price / self.tick_size) * self.tick_size, 10)

    def build(self, trades: Iterable[MarketTrade], source: str, symbol: str,
              timeframe: str) -> VolumeProfile:
        buckets: dict[float, dict[str, float]] = defaultdict(
            lambda: {"total": 0.0, "buy": 0.0, "sell": 0.0}
        )
        count = 0
        for trade in trades:
            count += 1
            price = self._bucket(trade.price)
            buckets[price]["total"] += trade.volume
            if trade.side == "buy":
                buckets[price]["buy"] += trade.volume
            elif trade.side == "sell":
                buckets[price]["sell"] += trade.volume

        if not buckets:
            raise ValueError("no trades supplied")

        levels = [
            VolumeProfileLevel(p, v["total"], v["buy"], v["sell"])
            for p, v in sorted(buckets.items())
        ]
        total = sum(level.total_volume for level in levels)
        buy = sum(level.buy_volume for level in levels)
        sell = sum(level.sell_volume for level in levels)
        poc_level = max(levels, key=lambda level: level.total_volume)
        poc_index = levels.index(poc_level)
        vah, val = self._value_area(levels, poc_index, total)
        volumes = [level.total_volume for level in levels]
        hvn_threshold = self._percentile(volumes, self.hvn_percentile)
        lvn_threshold = self._percentile(volumes, self.lvn_percentile)

        return VolumeProfile(
            source=source,
            symbol=symbol,
            timeframe=timeframe,
            levels=levels,
            poc=poc_level.price,
            vah=vah,
            val=val,
            hvn=[level.price for level in levels if level.total_volume >= hvn_threshold],
            lvn=[level.price for level in levels if level.total_volume <= lvn_threshold],
            total_volume=total,
            buy_volume=buy,
            sell_volume=sell,
            cumulative_delta=buy - sell,
            value_area_volume_fraction=self.value_area_fraction,
            quality="good" if count >= 100 else "limited",
        )

    def _value_area(self, levels: list[VolumeProfileLevel], poc_index: int,
                    total_volume: float) -> tuple[float, float]:
        target = total_volume * self.value_area_fraction
        accumulated = levels[poc_index].total_volume
        low = high = poc_index
        while accumulated < target and (low > 0 or high < len(levels) - 1):
            left = levels[low - 1].total_volume if low > 0 else -1.0
            right = levels[high + 1].total_volume if high < len(levels) - 1 else -1.0
            if right >= left and high < len(levels) - 1:
                high += 1
                accumulated += levels[high].total_volume
            elif low > 0:
                low -= 1
                accumulated += levels[low].total_volume
            else:
                break
        return levels[high].price, levels[low].price

    @staticmethod
    def _percentile(values: list[float], q: float) -> float:
        values = sorted(values)
        if not values:
            return 0.0
        if len(values) == 1:
            return values[0]
        position = (len(values) - 1) * q
        lower = int(position)
        upper = min(lower + 1, len(values) - 1)
        fraction = position - lower
        return values[lower] + (values[upper] - values[lower]) * fraction

    @staticmethod
    def detect_value_migration(previous: VolumeProfile, current: VolumeProfile) -> str:
        if previous.poc is None or current.poc is None:
            return "unknown"
        if current.poc > previous.poc:
            return "higher"
        if current.poc < previous.poc:
            return "lower"
        return "stable"

    @staticmethod
    def order_flow_summary(profile: VolumeProfile) -> dict[str, float | str]:
        total = profile.buy_volume + profile.sell_volume
        ratio = profile.net_delta / total if total else 0.0
        direction = "bullish" if ratio > 0.10 else "bearish" if ratio < -0.10 else "neutral"
        return {
            "delta": profile.net_delta,
            "delta_ratio": ratio,
            "buy_volume": profile.buy_volume,
            "sell_volume": profile.sell_volume,
            "direction": direction,
        }
