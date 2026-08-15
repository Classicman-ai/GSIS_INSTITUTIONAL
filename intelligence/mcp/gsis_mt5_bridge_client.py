import requests
from datetime import datetime, timezone


print("==============================")
print("GSIS MT5 BRIDGE CLIENT v1.0 ONLINE")
print("REMOTE METATRADER BRIDGE LAYER ACTIVE")
print("==============================")


class GSISMT5BridgeClient:

    def __init__(self, bridge_url="http://127.0.0.1:8000"):
        self.provider = "MT5_BRIDGE"
        self.bridge_url = bridge_url


    def health_check(self):

        try:
            response = requests.get(
                f"{self.bridge_url}/health",
                timeout=5
            )

            return {
                "provider": self.provider,
                "status": "CONNECTED",
                "bridge": response.json(),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        except Exception as e:

            return {
                "provider": self.provider,
                "status": "OFFLINE",
                "message": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }


    def get_quote(self, symbol="XAUUSD"):

        try:
            response = requests.get(
                f"{self.bridge_url}/quote/{symbol}",
                timeout=5
            )

            return response.json()

        except Exception as e:

            return {
                "provider": self.provider,
                "symbol": symbol,
                "status": "ERROR",
                "message": str(e)
            }


if __name__ == "__main__":

    print("==============================")
    print("GSIS MT5 BRIDGE CLIENT TEST")
    print("==============================")

    client = GSISMT5BridgeClient()

    print(client.health_check())
    print(client.get_quote("XAUUSD"))
