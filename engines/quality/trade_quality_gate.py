from datetime import datetime, timezone


class TradeQualityGate:

    def run(self, context):

        signal = context.signal or {}
        risk = context.risk or {}

        approved = (
            signal.get("execution_state") == "READY"
            and risk.get("status") == "RISK_APPROVED"
        )

        return {
            "engine": "GSIS TRADE QUALITY GATE",
            "version": "4.0",
            "symbol": context.symbol,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "quality_grade": "A" if approved else "C",
            "quality_score": 1.0 if approved else 0.0,
            "approval": approved,
            "status": "APPROVED" if approved else "REJECTED",
            "reasons": [] if approved else ["Signal or Risk not approved"],
        }


if __name__ == "__main__":

    class Dummy:
        symbol = "BTCUSDT"
        signal = {"execution_state": "READY"}
        risk = {"status": "RISK_APPROVED"}

    print(TradeQualityGate().run(Dummy()))
