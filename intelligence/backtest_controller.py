import datetime

from historical_replay_engine import HistoricalReplayEngine
from gsis_master_orchestrator import GSISMasterOrchestrator


class BacktestController:

    def __init__(self):

        print("==============================")
        print("GSIS BACKTEST CONTROLLER v1.0 ONLINE")
        print("FULL PIPELINE HISTORICAL TEST ACTIVE")
        print("==============================")

        self.replay = HistoricalReplayEngine()
        self.orchestrator = GSISMasterOrchestrator()

        self.total_candles = 0
        self.total_signals = 0
        self.pipeline_runs = 0


    def candle_to_signal(self, candle):

        direction = "BUY"

        if candle["close"] < candle["open"]:
            direction = "SELL"

        return {

            "symbol": "XAUUSD",

            "direction": direction,

            "entry": candle["close"],

            "stop_loss": round(
                candle["close"] + 0.30
                if direction == "SELL"
                else candle["close"] - 0.30,
                2
            ),

            "tp1": round(
                candle["close"] - 0.30
                if direction == "SELL"
                else candle["close"] + 0.30,
                2
            ),

            "confidence": 100,

            "reasons": [

                "HISTORICAL REPLAY"

            ]

        }


    def run(self, csv_file):

        result = self.replay.load_csv(csv_file)

        print(result)

        while self.replay.has_next():

            candle = self.replay.next_candle()

            self.total_candles += 1

            signal = self.candle_to_signal(candle)

            self.total_signals += 1

            print("==============================")
            print("REPLAY CANDLE")
            print("==============================")
            print(candle)

            try:

                pipeline = self.orchestrator.run_pipeline(signal)

                self.pipeline_runs += 1

                print("==============================")
                print("PIPELINE RESULT")
                print("==============================")
                print(pipeline)

            except Exception as e:

                print("==============================")
                print("PIPELINE ERROR")
                print("==============================")
                print(str(e))

        print("==============================")
        print("BACKTEST SUMMARY")
        print("==============================")

        summary = {

            "status": "BACKTEST COMPLETE",

            "candles_processed": self.total_candles,

            "signals_generated": self.total_signals,

            "pipeline_runs": self.pipeline_runs,

            "timestamp": datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }

        print(summary)

        return summary


if __name__ == "__main__":

    controller = BacktestController()

    controller.run(
        "market_data/xauusd_sample.csv"
    )
