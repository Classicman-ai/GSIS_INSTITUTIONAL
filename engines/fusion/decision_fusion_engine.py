from datetime import datetime, timezone


class DecisionFusionEngine:

    def __init__(self):
        self.name = "GSIS DECISION FUSION ENGINE"
        self.version = "7.0"


    def execute(self, context):

        market = getattr(context, "market", {}) or {}
        volume = getattr(context, "volume", {}) or {}
        orderflow = getattr(context, "orderflow", {}) or {}
        regime = getattr(context, "regime", {}) or {}
        adaptive = getattr(context, "adaptive", {}) or {}
        liquidity = getattr(context, "liquidity", {}) or {}


        score = 0
        reasons = []


        # MARKET
        if market:
            score += 1
            reasons.append("MARKET DATA VALID")


        # VOLUME
        if volume.get("volume_bias") == "BUY_ACCEPTANCE":
            score += 1
            reasons.append("BUY VOLUME ACCEPTANCE")


        # ORDER FLOW
        if orderflow.get("flow_bias") == "BUY_PRESSURE":
            score += 1
            reasons.append("ORDER FLOW BUY PRESSURE")


        # REGIME
        if regime.get("market_regime") == "TRENDING_UP":
            score += 1
            reasons.append("BULLISH REGIME")


        # ADAPTIVE
        if adaptive.get("market_condition") == "BULLISH_TREND":
            score += 1
            reasons.append("ADAPTIVE BULLISH ALIGNMENT")


        # LIQUIDITY INTELLIGENCE
        if liquidity:

            if liquidity.get("liquidity_bias") == "BUY_SIDE":
                score += 1
                reasons.append("BUY SIDE LIQUIDITY CONFIRMATION")


            if liquidity.get("liquidity_sweep"):
                score += 1
                reasons.append("LIQUIDITY SWEEP DETECTED")


            if liquidity.get("stop_hunt"):
                reasons.append("STOP HUNT DETECTED")


        confidence = round(score / 7, 2)


        if score >= 5:

            bias = "BULLISH"
            execution = "READY"

        elif score <= 2:

            bias = "BEARISH"
            execution = "BLOCKED"

        else:

            bias = "NEUTRAL"
            execution = "WAIT"


        result = {

            "engine": self.name,
            "version": self.version,
            "symbol": "BTCUSDT",
            "timestamp": datetime.now(timezone.utc).isoformat(),

            "fusion_score": score,
            "bias": bias,
            "confidence": confidence,

            "execution": execution,

            "reasons": reasons,

            "status": "FUSION_COMPLETE"

        }


        context.fusion = result

        return result



if __name__ == "__main__":

    engine = DecisionFusionEngine()

    print("GSIS DECISION FUSION ENGINE v7.0 READY")
