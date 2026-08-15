import json
import os
import datetime


class TradeJournalEngine:

    def __init__(self):

        self.file = "data/gsis_trade_journal.json"

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump([], f)

        print("==============================")
        print("GSIS TRADE JOURNAL ENGINE v1.0 ONLINE")
        print("INSTITUTIONAL TRADE RECORDING ACTIVE")
        print("==============================")


    def record_trade(self, trade):

        with open(self.file, "r") as f:
            history = json.load(f)


        trade_record = {

            "trade_id": trade.get("trade_id"),

            "symbol": trade.get("symbol"),

            "direction": trade.get("direction"),

            "entry": trade.get("entry"),

            "stop_loss": trade.get("stop_loss"),

            "take_profit": trade.get("take_profit"),

            "confidence": trade.get("confidence"),

            "status": trade.get("status"),

            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }


        history.append(trade_record)


        with open(self.file, "w") as f:
            json.dump(
                history,
                f,
                indent=4
            )


        result = {

            "status": "TRADE RECORDED",

            "trade_id": trade.get("trade_id"),

            "journal_size": len(history),

            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }


        print("==============================")
        print("GSIS JOURNAL RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":

    engine = TradeJournalEngine()

    engine.record_trade(
        {
            "trade_id":"TEST-001",
            "symbol":"XAUUSD",
            "direction":"SELL",
            "entry":2387.5,
            "stop_loss":2387.8,
            "take_profit":2387.2,
            "confidence":100,
            "status":"OPEN"
        }
    )
