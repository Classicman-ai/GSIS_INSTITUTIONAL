from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Iterable, Optional

from volume_intelligence.cme_market_microstructure import (
    CMEBookLevel,
    CMEBookEvent,
    CMETrade,
)


@dataclass(frozen=True)
class CMEDataSourceConfig:
    """Runtime-only CME feed configuration. No market data is embedded here."""

    api_key: str
    dataset: str
    symbols: str
    stype_in: str = "continuous"
    schemas: tuple[str, ...] = ("mbo", "mbp-10", "trades")

    @classmethod
    def from_environment(cls) -> "CMEDataSourceConfig":
        api_key = os.getenv("DATABENTO_API_KEY", "").strip()
        dataset = os.getenv("GSIS_CME_DATASET", "").strip()
        symbols = os.getenv("GSIS_CME_SYMBOLS", "").strip()
        stype_in = os.getenv("GSIS_CME_STYPE_IN", "continuous").strip()
        schemas_raw = os.getenv("GSIS_CME_SCHEMAS", "mbo,mbp-10,trades")
        schemas = tuple(x.strip() for x in schemas_raw.split(",") if x.strip())

        missing = [name for name, value in (
            ("DATABENTO_API_KEY", api_key),
            ("GSIS_CME_DATASET", dataset),
            ("GSIS_CME_SYMBOLS", symbols),
        ) if not value]
        if missing:
            raise RuntimeError(
                "CME data source is not configured. Missing environment variables: "
                + ", ".join(missing)
            )
        return cls(api_key, dataset, symbols, stype_in, schemas)


class DatabentoCMEDataSource:
    """
    External CME/COMEX source adapter.

    This class owns connectivity only. It does not calculate signals, create
    prices, generate order-book events, or make trading decisions.
    """

    SOURCE = "CME_COMEX_DATABENTO"

    def __init__(
        self,
        config: CMEDataSourceConfig,
        on_trade: Optional[Callable[[CMETrade], None]] = None,
        on_book_level: Optional[Callable[[CMEBookLevel], None]] = None,
        on_book_event: Optional[Callable[[CMEBookEvent], None]] = None,
    ) -> None:
        self.config = config
        self.on_trade = on_trade
        self.on_book_level = on_book_level
        self.on_book_event = on_book_event
        self._client = None

    @staticmethod
    def _timestamp(record) -> datetime:
        value = int(record.ts_event)
        return datetime.fromtimestamp(value / 1_000_000_000, tz=timezone.utc)

    @staticmethod
    def _side(value) -> str:
        value = str(value)
        if value in ("B", "Bid", "bid"):
            return "buy"
        if value in ("A", "Ask", "ask"):
            return "sell"
        return "unknown"

    @staticmethod
    def _price(record) -> float:
        if hasattr(record, "pretty_price"):
            price = float(record.pretty_price)
            if price == price:
                return price
        return float(record.price)

    def _handle_mbo(self, record) -> None:
        action_map = {
            "A": "add",
            "M": "modify",
            "C": "cancel",
            "T": "execute",
            "F": "execute",
        }
        action = action_map.get(str(record.action))
        if action is None:
            return
        event = CMEBookEvent(
            timestamp=self._timestamp(record),
            order_id=str(record.order_id),
            price=self._price(record),
            quantity=float(record.size),
            side=self._side(record.side),
            action=action,
            instrument_id=int(record.instrument_id),
            source=self.SOURCE,
        )
        if self.on_book_event:
            self.on_book_event(event)

    def _handle_mbp10(self, record) -> None:
        timestamp = self._timestamp(record)
        instrument_id = int(record.instrument_id)
        for index in range(10):
            suffix = f"{index:02d}"
            for side_name, prefix in (("bid", "bid"), ("ask", "ask")):
                price_attr = f"{prefix}_px_{suffix}"
                size_attr = f"{prefix}_sz_{suffix}"
                if not hasattr(record, price_attr) or not hasattr(record, size_attr):
                    continue
                price = float(getattr(record, f"pretty_{prefix}_px_{suffix}", float("nan")))
                if price != price:
                    raw_price = int(getattr(record, price_attr))
                    if raw_price <= 0:
                        continue
                    price = raw_price / 1_000_000_000
                quantity = float(getattr(record, size_attr))
                if price <= 0 or quantity < 0:
                    continue
                level = CMEBookLevel(
                    timestamp=timestamp,
                    price=price,
                    quantity=quantity,
                    side=side_name,
                    depth=index,
                    instrument_id=instrument_id,
                    source=self.SOURCE,
                )
                if self.on_book_level:
                    self.on_book_level(level)

    def _handle_trade(self, record) -> None:
        trade = CMETrade(
            timestamp=self._timestamp(record),
            price=self._price(record),
            quantity=float(record.size),
            aggressor_side=self._side(record.side),
            instrument_id=int(record.instrument_id),
            source=self.SOURCE,
        )
        if self.on_trade:
            self.on_trade(trade)

    def _dispatch(self, record) -> None:
        name = type(record).__name__.lower()
        if "mbo" in name:
            self._handle_mbo(record)
        elif "mbp10" in name or "mbp_10" in name:
            self._handle_mbp10(record)
        elif "trade" in name:
            self._handle_trade(record)

    def stream(self, *, start: str | None = None, snapshot: bool = False) -> None:
        """Block and stream external CME records into registered callbacks."""
        try:
            import databento as db
        except ImportError as exc:
            raise RuntimeError(
                "Databento SDK is required for the CME external data source. "
                "Install the provider dependency with: pip install databento"
            ) from exc

        client = db.Live(key=self.config.api_key, reconnect_policy="reconnect")
        self._client = client

        for schema in self.config.schemas:
            kwargs = {
                "dataset": self.config.dataset,
                "schema": schema,
                "symbols": self.config.symbols,
                "stype_in": self.config.stype_in,
            }
            if start is not None:
                kwargs["start"] = start
            if schema == "mbo" and snapshot:
                kwargs["snapshot"] = True
            client.subscribe(**kwargs)

        for record in client:
            self._dispatch(record)

    def stop(self) -> None:
        if self._client is not None:
            self._client.stop()
            self._client = None
