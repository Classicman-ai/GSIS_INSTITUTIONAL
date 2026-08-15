class TradeValidatorEngine:


    def __init__(self):

        print("==============================")
        print("GSIS INSTITUTIONAL TRADE VALIDATOR v1.0 ONLINE")
        print("==============================")
        print("SMART MONEY SETUP VALIDATION ACTIVE")
        print("==============================")


    def validate(
        self,
        liquidity,
        sweep,
        order_block,
        fvg,
        structure,
        regime
    ):


        reasons = []

        score = 0

        direction = None



        # ==============================
        # LIQUIDITY CONFIRMATION
        # ==============================

        if sweep.get("sweep_detected"):

            score += 20

            reasons.append(
                "LIQUIDITY SWEEP CONFIRMED"
            )



        # ==============================
        # ORDER BLOCK
        # ==============================

        if order_block.get("type"):

            score += 20

            reasons.append(
                f"{order_block['type']} ORDER BLOCK"
            )



        # ==============================
        # FAIR VALUE GAP
        # ==============================

        if fvg.get("fvg_found"):

            score += 20

            reasons.append(
                f"{fvg['type']} FAIR VALUE GAP"
            )



        # ==============================
        # STRUCTURE
        # ==============================

        if structure.get("choch"):

            score += 30

            reasons.append(
                structure.get("confirmation")
            )


        elif structure.get("bos"):

            score += 25

            reasons.append(
                structure.get("confirmation")
            )



        # ==============================
        # MARKET REGIME FILTER
        # ==============================

        if regime.get("regime") not in [
            "HIGH_VOLATILITY",
            "LOW_VOLATILITY"
        ]:

            score += 10

            reasons.append(
                "FAVORABLE MARKET REGIME"
            )



        # ==============================
        # DIRECTION
        # ==============================

        if structure.get("structure") == "BEARISH":

            direction = "SELL"


        elif structure.get("structure") == "BULLISH":

            direction = "BUY"



        # ==============================
        # FINAL DECISION
        # ==============================


        if score >= 70:


            result = {

                "symbol": structure["symbol"],

                "setup": "VALID",

                "direction": direction,

                "confidence": score,

                "reasons": reasons,

                "status": "APPROVED"

            }


        else:


            result = {

                "symbol": structure["symbol"],

                "setup": "REJECTED",

                "direction": None,

                "confidence": score,

                "reasons": reasons,

                "status": "WAIT"

            }



        print("==============================")
        print("GSIS TRADE VALIDATION RESULT")
        print("==============================")
        print(result)


        return result
