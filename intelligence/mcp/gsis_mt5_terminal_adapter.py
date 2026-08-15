from datetime import datetime, timezone


print("==============================")
print("GSIS MT5 TERMINAL ADAPTER v1.0 ONLINE")
print("METATRADER TERMINAL INTERFACE LAYER ACTIVE")
print("==============================")


class GSISMT5TerminalAdapter:

    def __init__(self):
        self.connected = False
        self.package_available = False
        self.terminal = None


    def initialize(self):

        try:
            import MetaTrader5 as mt5

            self.package_available = True
            self.terminal = mt5

            # Real terminal initialization will happen here
            # when running on a supported MT5 Python environment

            return {
                "provider": "MT5_TERMINAL",
                "status": "PACKAGE_AVAILABLE",
                "connected": self.connected,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }


        except ImportError:

            return {
                "provider": "MT5_TERMINAL",
                "status": "MISSING_PACKAGE",
                "message": "MetaTrader5 package unavailable on this platform",
                "connected": False,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }


    def health(self):

        return {
            "provider": "MT5_TERMINAL",
            "connected": self.connected,
            "package_available": self.package_available,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


    def quote(self, symbol="XAUUSD"):

        if not self.connected:

            return {
                "symbol": symbol,
                "status": "NOT_CONNECTED",
                "price": None,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }


        tick = self.terminal.symbol_info_tick(symbol)

        if tick is None:

            return {
                "symbol": symbol,
                "status": "NO_TICK_DATA",
                "price": None,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }


        return {
            "symbol": symbol,
            "bid": tick.bid,
            "ask": tick.ask,
            "price": (tick.bid + tick.ask) / 2,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


    def account(self):

        if not self.connected:

            return {
                "status": "NOT_CONNECTED",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }


        info = self.terminal.account_info()

        return {
            "status": "CONNECTED",
            "account": info._asdict(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }



adapter = GSISMT5TerminalAdapter()


if __name__ == "__main__":

    print("==============================")
    print("GSIS MT5 TERMINAL ADAPTER TEST")
    print("==============================")

    print(adapter.initialize())
    print(adapter.health())
    print(adapter.quote("XAUUSD"))
    print(adapter.account())
