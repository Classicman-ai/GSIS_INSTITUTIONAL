import csv
import datetime


class HistoricalReplayEngine:

    def __init__(self):

        print("==============================")
        print("GSIS HISTORICAL REPLAY ENGINE v1.0 ONLINE")
        print("MARKET REPLAY SYSTEM ACTIVE")
        print("==============================")

        self.current_index = 0
        self.market_data = []


    def load_csv(self, filename):

        self.market_data = []

        with open(filename, "r") as f:

            reader = csv.DictReader(f)

            for row in reader:

                self.market_data.append(
                    {
                        "time": row.get("time"),
                        "open": float(row["open"]),
                        "high": float(row["high"]),
                        "low": float(row["low"]),
                        "close": float(row["close"]),
                        "volume": float(
                            row.get("volume", 0)
                        )
                    }
                )

        self.current_index = 0

        return {
            "status": "DATA LOADED",
            "candles": len(self.market_data),
            "timestamp": datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()
        }


    def has_next(self):

        return self.current_index < len(self.market_data)


    def next_candle(self):

        if not self.has_next():

            return None

        candle = self.market_data[self.current_index]

        self.current_index += 1

        return candle


    def replay(self):

        while self.has_next():

            yield self.next_candle()


if __name__ == "__main__":

    engine = HistoricalReplayEngine()

    print(
        engine.load_csv(
            "market_data/xauusd_sample.csv"
        )
    )

    for candle in engine.replay():

        print(candle)
