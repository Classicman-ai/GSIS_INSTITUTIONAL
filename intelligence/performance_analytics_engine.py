
import json
import os
import datetime


class PerformanceAnalyticsEngine:

    def __init__(self):

        self.file = "data/gsis_trade_journal.json"

        print("==============================")
        print("GSIS PERFORMANCE ANALYTICS ENGINE v1.0 ONLINE")
        print("TRADE PERFORMANCE INTELLIGENCE ACTIVE")
        print("==============================")


    def analyze(self):

        if not os.path.exists(self.file):

            return {
                "status": "NO DATA"
            }


        with open(self.file, "r") as f:

            trades = json.load(f)


        total = len(trades)

        wins = 0
        losses = 0
        open_trades = 0


        for trade in trades:

            status = trade.get("status")


            if status in ["WIN", "CLOSED_PROFIT"]:
                wins += 1


            elif status in ["LOSS", "CLOSED_LOSS"]:
                losses += 1


            else:
                open_trades += 1



        win_rate = 0

        closed = wins + losses

        if closed > 0:

            win_rate = round(
                (wins / closed) * 100,
                2
            )


        result = {

            "status":
            "ANALYSIS COMPLETE",

            "total_trades":
            total,

            "wins":
            wins,

            "losses":
            losses,

            "open_trades":
            open_trades,

            "win_rate":
            win_rate,

            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }


        print("==============================")
        print("GSIS PERFORMANCE RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":

    engine = PerformanceAnalyticsEngine()

    engine.analyze()
