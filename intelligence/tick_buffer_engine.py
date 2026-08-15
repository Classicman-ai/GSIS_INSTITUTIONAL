from collections import deque
from datetime import datetime, timezone


class TickBufferEngine:

    def __init__(self, max_ticks=10000):

        print("==============================")
        print("GSIS TICK BUFFER ENGINE v1.0 ONLINE")
        print("==============================")
        print("INSTITUTIONAL TICK MEMORY ACTIVE")
        print("==============================")

        self.buffer = deque(maxlen=max_ticks)

    def process(self, tick):

        record = {
            "symbol": tick["symbol"],
            "price": tick["price"],
            "timestamp": tick.get(
                "timestamp",
                datetime.now(timezone.utc).isoformat()
            )
        }

        self.buffer.append(record)

        prices = [t["price"] for t in self.buffer]

        if len(prices) >= 2:
            velocity = prices[-1] - prices[-2]
        else:
            velocity = 0.0

        high = max(prices)
        low = min(prices)
        spread = high - low

        result = {
            "symbol": record["symbol"],
            "latest_price": record["price"],
            "tick_count": len(self.buffer),
            "velocity": round(velocity, 5),
            "micro_volatility": round(spread, 5),
            "buffer_size": self.buffer.maxlen,
            "timestamp": record["timestamp"]
        }

        print("==============================")
        print("GSIS TICK BUFFER")
        print("==============================")
        print(result)

        return result

    def latest(self):

        if len(self.buffer) == 0:
            return None

        return self.buffer[-1]

    def history(self):

        return list(self.buffer)

    def clear(self):

        self.buffer.clear()

        print("==============================")
        print("TICK BUFFER CLEARED")
        print("==============================")
