from datetime import datetime, timezone


class JournalEngine:

    def execute(self, context):

        signal = context.signal or {}
        risk = context.risk or {}
        quality = context.quality or {}
        fusion = context.fusion or {}

        return {

            "engine": "GSIS JOURNAL ENGINE",

            "version": "1.1",

            "symbol": getattr(context, "symbol", "UNKNOWN"),

            "timestamp": datetime.now(timezone.utc).isoformat(),

            "direction": signal.get("direction", "NO_TRADE"),

            "entry": risk.get("entry"),

            "stop_loss": risk.get("stop_loss"),

            "targets": risk.get("targets", {}),

            "risk_percent": risk.get("risk_percent", 0),

            "quality_grade": quality.get("quality_grade", "N/A"),

            "fusion_score": fusion.get("fusion_score", 0),

            "status": "JOURNALED"

        }


if __name__ == "__main__":

    class Dummy:
        symbol = "BTCUSDT"
        signal = None
        risk = None
        quality = None
        fusion = None

    print(JournalEngine().execute(Dummy()))
