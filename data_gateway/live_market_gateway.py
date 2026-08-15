"""
=========================================================

GSIS INSTITUTIONAL

LIVE MARKET DATA GATEWAY ENGINE v3.0

Binance + Event Bus

=========================================================
"""

import os
import sys
from datetime import datetime, UTC

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from binance.client import Client
from database.database_engine import DatabaseEngine
from core.event_bus import event_bus


class LiveMarketGateway:

    def __init__(self):

        self.symbol = "BTCUSDT"

        self.client = Client()

        self.database = DatabaseEngine()

    def initialize(self):

        self.database.initialize()

        print("==============================")
        print("GSIS LIVE MARKET GATEWAY v3.0")
        print("==============================")

    def get_latest_candle(self):

        candle = self.client.get_klines(
            symbol=self.symbol,
            interval=Client.KLINE_INTERVAL_1MINUTE,
            limit=1
        )[0]

        return {

            "symbol": self.symbol,

            "timeframe": "M1",

            "open": float(candle[1]),

            "high": float(candle[2]),

            "low": float(candle[3]),

            "close": float(candle[4]),

            "volume": float(candle[5]),

            "timestamp": datetime.now(UTC).isoformat()

        }

    def publish_market_event(self):

        candle = self.get_latest_candle()

        self.database.save_candle(

            symbol=candle["symbol"],

            timeframe=candle["timeframe"],

            open_price=candle["open"],

            high=candle["high"],

            low=candle["low"],

            close=candle["close"],

            volume=candle["volume"]

        )

        event_bus.publish(

            "market_candle",

            candle

        )

        return candle


def candle_listener(data):

    print()

    print("========== MARKET EVENT ==========")

    print(data)

    print()

    print("Stored and distributed.")

    print()


def main():

    gateway = LiveMarketGateway()

    gateway.initialize()

    event_bus.subscribe(

        "market_candle",

        candle_listener

    )

    gateway.publish_market_event()


if __name__ == "__main__":

    main()
