"""Canonical notification boundary.

Notification publishers receive CanonicalTradeSignal only. They cannot create,
modify, or infer trading decisions. Provider credentials and provider-specific
implementations stay outside the canonical decision path.
"""

from __future__ import annotations

from typing import Callable, Iterable

from intelligence.canonical_trade_signal import CanonicalTradeSignal


NotificationPublisher = Callable[[CanonicalTradeSignal], None]


class CanonicalNotificationBus:
    """Fan out the already-authorized canonical signal to configured publishers."""

    def __init__(self, publishers: Iterable[NotificationPublisher] = ()) -> None:
        self._publishers = tuple(publishers)

    def publish(self, signal: CanonicalTradeSignal) -> int:
        if not isinstance(signal, CanonicalTradeSignal):
            raise TypeError("NotificationBus accepts CanonicalTradeSignal only")
        delivered = 0
        for publisher in self._publishers:
            publisher(signal)
            delivered += 1
        return delivered
