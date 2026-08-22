from adapters.broker_symbol_resolution import ResolvedBrokerSymbol, validate_resolution


def test_resolution_preserves_broker_symbol():
    resolved = ResolvedBrokerSymbol(
        canonical_instrument="GOLD",
        broker_symbol="broker_specific_symbol",
        metadata={"trade_tick_size": 0.01},
    )
    assert validate_resolution(resolved).broker_symbol == "broker_specific_symbol"


def test_resolution_rejects_empty_canonical_instrument():
    try:
        ResolvedBrokerSymbol(canonical_instrument="", broker_symbol="X")
    except ValueError as exc:
        assert str(exc) == "canonical_instrument is required"
    else:
        raise AssertionError("Expected empty canonical instrument to fail")


def test_resolution_rejects_empty_broker_symbol():
    try:
        ResolvedBrokerSymbol(canonical_instrument="GOLD", broker_symbol="")
    except ValueError as exc:
        assert str(exc) == "broker_symbol is required"
    else:
        raise AssertionError("Expected empty broker symbol to fail")
