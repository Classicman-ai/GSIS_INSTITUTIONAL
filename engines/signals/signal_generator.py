from datetime import datetime, timezone


class SignalGenerator:

    def run(self, context):

        fusion = getattr(context, "fusion", None)

        confidence = 0

        if fusion:
            confidence = fusion.get(
                "confidence",
                0
            )

        if confidence >= 0.75:
            direction = "LONG"
            action = "EXECUTE_LONG"
            grade = "A"

        elif confidence >= 0.50:
            direction = "WAIT"
            action = "MONITOR"
            grade = "B"

        else:
            direction = "NO_TRADE"
            action = "BLOCK"
            grade = "C"


        return {

            "engine":
                "GSIS SIGNAL GENERATOR",

            "version":
                "4.0",

            "symbol":
                context.symbol,

            "timestamp":
                datetime.now(timezone.utc).isoformat(),

            "direction":
                direction,

            "signal_grade":
                grade,

            "confidence":
                confidence,

            "setup":
                "TREND_CONTINUATION",

            "action":
                action,

            "execution_state":
                "READY" if action == "EXECUTE_LONG" else "BLOCKED",

            "status":
                "SIGNAL_COMPLETE"
        }


if __name__ == "__main__":

    print("GSIS SIGNAL GENERATOR v4.0 READY")
