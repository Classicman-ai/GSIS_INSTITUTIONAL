import json
import os
import datetime


class OutcomeMemoryEngine:

    def __init__(self):

        self.file = "data/gsis_outcome_memory.json"

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.file):

            with open(self.file, "w") as f:
                json.dump([], f)


        print("==============================")
        print("GSIS OUTCOME MEMORY ENGINE v1.0 ONLINE")
        print("TRADE RESULT LEARNING MEMORY ACTIVE")
        print("==============================")


    def store_outcome(self, trade):

        with open(self.file, "r") as f:

            memory = json.load(f)


        record = {

            "trade_id":
            trade.get("trade_id"),

            "symbol":
            trade.get("symbol"),

            "direction":
            trade.get("direction"),

            "pattern":
            trade.get("pattern",
            "UNKNOWN"),

            "result":
            trade.get("result",
            "OPEN"),

            "profit_loss":
            trade.get("profit_loss",
            0),

            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }


        memory.append(record)


        with open(self.file, "w") as f:

            json.dump(
                memory,
                f,
                indent=4
            )


        result = {

            "status":
            "OUTCOME STORED",

            "trade_id":
            record["trade_id"],

            "memory_size":
            len(memory),

            "timestamp":
            record["timestamp"]

        }


        print("==============================")
        print("GSIS OUTCOME RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":

    engine = OutcomeMemoryEngine()


    test_trade = {

        "trade_id":
        "TEST-001",

        "symbol":
        "XAUUSD",

        "direction":
        "SELL",

        "pattern":
        "LIQUIDITY_SWEEP_BEARISH",

        "result":
        "OPEN",

        "profit_loss":
        0

    }


    engine.store_outcome(test_trade)
