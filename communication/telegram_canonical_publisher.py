"""Telegram publisher boundary for CanonicalTradeSignal.

Transport credentials and HTTP implementation are deliberately external. The
publisher accepts only the canonical signal and never creates a decision.
"""

from intelligence.canonical_trade_signal import CanonicalTradeSignal


class TelegramCanonicalPublisher:
    def __init__(self, sender):
        self.sender = sender

    def publish(self, signal: CanonicalTradeSignal) -> None:
        if not isinstance(signal, CanonicalTradeSignal):
            raise TypeError("Telegram publisher requires CanonicalTradeSignal")
        self.sender(signal)
