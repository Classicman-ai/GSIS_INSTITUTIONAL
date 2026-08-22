"""WhatsApp publisher boundary for CanonicalTradeSignal.

Transport credentials and provider-specific HTTP implementation are external.
The publisher accepts only the canonical signal and never creates a decision.
"""

from intelligence.canonical_trade_signal import CanonicalTradeSignal


class WhatsAppCanonicalPublisher:
    def __init__(self, sender):
        self.sender = sender

    def publish(self, signal: CanonicalTradeSignal) -> None:
        if not isinstance(signal, CanonicalTradeSignal):
            raise TypeError("WhatsApp publisher requires CanonicalTradeSignal")
        self.sender(signal)
