from datetime import datetime


class PerformanceEngine:


    def __init__(self):
        self.version = "1.1"



    def execute(self, context):

        quality = context.quality if isinstance(context.quality, dict) else {}

        signal = context.signal if isinstance(context.signal, dict) else {}

        direction = signal.get("direction", "NO_TRADE")

        approved = quality.get(
            "approval",
            False
        )


        if direction == "NO_TRADE":

            return {

                "engine": "GSIS PERFORMANCE ENGINE",
                "version": self.version,
                "symbol": context.symbol,
                "timestamp": datetime.utcnow().isoformat() + "+00:00",
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0,
                "profit_factor": 0,
                "expectancy": 0,
                "max_drawdown": 0,
                "status": "NO_TRADE_RECORDED"

            }



        return {

            "engine": "GSIS PERFORMANCE ENGINE",
            "version": self.version,
            "symbol": context.symbol,
            "timestamp": datetime.utcnow().isoformat() + "+00:00",
            "total_trades": 1,
            "winning_trades": 1 if approved else 0,
            "losing_trades": 0 if approved else 1,
            "win_rate": 100.0 if approved else 0.0,
            "profit_factor": 1.0 if approved else 0,
            "expectancy": 1.0 if approved else -1.0,
            "max_drawdown": 0.0 if approved else 1.0,
            "status": "PERFORMANCE_READY"

        }



if __name__ == "__main__":

    from core.context_runner import GSISContext

    ctx = GSISContext("BTCUSDT")

    print(
        PerformanceEngine().execute(ctx)
    )
