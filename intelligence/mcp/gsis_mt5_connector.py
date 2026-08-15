from datetime import datetime, timezone


print("==============================")
print("GSIS MT5 CONNECTOR v1.0 ONLINE")
print("METATRADER 5 BRIDGE LAYER ACTIVE")
print("==============================")


class GSISMT5Connector:

    def __init__(self):
        self.provider = "MT5"
        self.connected = False

    def check_connection(self):
        try:
            import MetaTrader5 as mt5

            if mt5.initialize():
                self.connected = True

                return {
                    "provider": self.provider,
                    "status": "CONNECTED",
                    "terminal": mt5.version(),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }

            return {
                "provider": self.provider,
                "status": "NOT_CONNECTED",
                "message": "MT5 initialize failed",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        except ImportError:

            return {
                "provider": self.provider,
                "status": "MISSING_PACKAGE",
                "message": "MetaTrader5 Python package not installed",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }


    def get_account(self):

        if not self.connected:
            return {
                "provider": self.provider,
                "status": "NOT_CONNECTED"
            }

        import MetaTrader5 as mt5

        account = mt5.account_info()

        if account:
            return {
                "provider": self.provider,
                "status": "ACCOUNT_CONNECTED",
                "login": account.login,
                "balance": account.balance,
                "equity": account.equity
            }

        return {
            "provider": self.provider,
            "status": "ACCOUNT_UNAVAILABLE"
        }


if __name__ == "__main__":

    print("==============================")
    print("GSIS MT5 CONNECTOR TEST")
    print("==============================")

    connector = GSISMT5Connector()

    print(connector.check_connection())
    print(connector.get_account())
