from communication.canonical_notification_bus import CanonicalNotificationBus
from communication.telegram_canonical_publisher import TelegramCanonicalPublisher
from communication.whatsapp_canonical_publisher import WhatsAppCanonicalPublisher
from intelligence.canonical_trade_signal import CanonicalTradeSignal


def test_notification_bus_accepts_only_canonical_signal():
    received = []

    def publisher(signal):
        received.append(signal)

    signal = CanonicalTradeSignal(
        signal_id="TEST:NOTIFY:1", symbol="XAUUSD", timeframe="M5", decision="BUY",
        confidence=1.0, entry=100.0, stop_loss=99.0, take_profits=[103.0],
    )
    delivered = CanonicalNotificationBus([publisher]).publish(signal)
    assert delivered == 1
    assert received == [signal]


def test_telegram_and_whatsapp_accept_only_canonical_signal():
    received = []
    signal = CanonicalTradeSignal(
        signal_id="TEST:NOTIFY:2", symbol="XAUUSD", timeframe="M5", decision="SELL",
        confidence=1.0, entry=100.0, stop_loss=101.0, take_profits=[97.0],
    )
    TelegramCanonicalPublisher(received.append).publish(signal)
    WhatsAppCanonicalPublisher(received.append).publish(signal)
    assert received == [signal, signal]


def test_notification_bus_rejects_non_canonical_objects():
    bus = CanonicalNotificationBus()
    try:
        bus.publish({"decision": "BUY"})
    except TypeError:
        return
    raise AssertionError("notification bus accepted a non-canonical decision object")
