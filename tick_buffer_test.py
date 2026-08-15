from intelligence.realtime_data_engine import RealtimeDataEngine
from intelligence.tick_buffer_engine import TickBufferEngine

feed = RealtimeDataEngine()
buffer = TickBufferEngine()

prices = [
    2386.50,
    2386.52,
    2386.49,
    2386.57,
    2386.60,
    2386.58,
    2386.63,
]

for price in prices:

    tick = feed.receive_tick(
        "XAUUSD",
        price
    )

    buffer.process(tick)

print("==============================")
print("LATEST TICK")
print("==============================")
print(buffer.latest())

print("==============================")
print("TOTAL TICKS")
print("==============================")
print(len(buffer.history()))
