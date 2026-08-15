from core.event_bus import event_bus
from market.candle_builder import CandleBuilder
from market.candle_database_writer import candle_receiver


builder = CandleBuilder()


event_bus.subscribe(
    "market_tick",
    builder.process_tick
)


event_bus.subscribe(
    "completed_candle",
    candle_receiver
)


print("==============================")
print("GSIS CANDLE PIPELINE TEST")
print("==============================")


# First candle tick

event_bus.publish(
    "market_tick",
    {
        "symbol": "BTCUSDT",
        "price": 64580.0,
        "quantity": 0.01
    }
)


# Force candle close

builder.current_minute = "OLD_MINUTE"


# New tick creates completed candle

event_bus.publish(
    "market_tick",
    {
        "symbol": "BTCUSDT",
        "price": 64585.0,
        "quantity": 0.02
    }
)
