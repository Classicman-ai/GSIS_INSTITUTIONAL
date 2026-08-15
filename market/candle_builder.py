"""
=========================================================

GSIS INSTITUTIONAL

CANDLE BUILDER ENGINE v1.1

Tick -> OHLCV Conversion Layer
Event Bus Integration

=========================================================
"""

from datetime import datetime, UTC

from core.event_bus import event_bus


class CandleBuilder:


    def __init__(self):

        self.symbol = "BTCUSDT"

        self.timeframe = "M1"

        self.current_minute = None

        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.volume = 0.0


    def process_tick(self, tick):

        price = tick["price"]

        quantity = tick["quantity"]

        timestamp = datetime.now(UTC)

        minute = timestamp.strftime(
            "%Y-%m-%d %H:%M"
        )


        # First tick starts candle

        if self.current_minute is None:

            self.start_candle(
                minute,
                price
            )


        # New minute = close previous candle

        elif minute != self.current_minute:

            candle = self.close_candle()


            print(
                "CANDLE COMPLETED:"
            )

            print(candle)


            # Send completed candle
            # to GSIS Event Bus

            event_bus.publish(

                "completed_candle",

                candle

            )


            self.start_candle(
                minute,
                price
            )


        # Update active candle

        self.high = max(
            self.high,
            price
        )

        self.low = min(
            self.low,
            price
        )

        self.close = price

        self.volume += quantity



    def start_candle(
            self,
            minute,
            price):


        self.current_minute = minute

        self.open = price

        self.high = price

        self.low = price

        self.close = price

        self.volume = 0.0



    def close_candle(self):


        return {

            "symbol": self.symbol,

            "timeframe": self.timeframe,

            "open": self.open,

            "high": self.high,

            "low": self.low,

            "close": self.close,

            "volume": self.volume,

            "timestamp":
                datetime.now(UTC).isoformat()

        }
