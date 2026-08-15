from intelligence.realtime_data_engine import RealtimeDataEngine
from intelligence.candle_stream_engine import CandleStreamEngine
from intelligence.market_feed_manager import MarketFeedManager



data_engine = RealtimeDataEngine()

candle_engine = CandleStreamEngine()


feed = MarketFeedManager(
    data_engine,
    candle_engine
)



candle = feed.update(
    "XAUUSD",
    2386.50
)


print("==============================")
print("GSIS REALTIME TEST COMPLETE")
print("==============================")

print(candle)
