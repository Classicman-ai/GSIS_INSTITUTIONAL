"""
=========================================================
GSIS INSTITUTIONAL
Data Engine
Version: 2.0
=========================================================
"""

import time
from datetime import datetime
from binance.client import Client

from core.base_engine import BaseEngine


class DataEngine(BaseEngine):

    def __init__(self):

        super().__init__("Data Engine")

        self.client = Client()

        self.symbol = "XAUTUSDT"

    def initialize(self):

        super().initialize()

        print("================================")
        print("GSIS ENGINE 1: DATA CORE ONLINE")
        print("Asset:", self.symbol)
        print("================================")

    def run(self):

        try:

            ticker = self.client.get_symbol_ticker(
                symbol=self.symbol
            )

            price = float(ticker["price"])

            server_time = self.client.get_server_time()

            market_time = datetime.fromtimestamp(
                server_time["serverTime"] / 1000
            )

            print(
                "TIME:",
                market_time,
                "| PRICE:",
                price
            )

        except Exception as e:

            print("DATA ERROR:", e)

    def shutdown(self):

        super().shutdown()
