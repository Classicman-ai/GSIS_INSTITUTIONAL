import datetime


from intelligence.memory.gsis_intelligence_memory_connector import (
    GSISIntelligenceMemoryConnector
)



class GSISAdaptiveIntelligenceBridge:


    def __init__(self):

        print("==============================")
        print("GSIS ADAPTIVE INTELLIGENCE BRIDGE v2.0 ONLINE")
        print("MULTI FACTOR CONFIDENCE SYNTHESIS ACTIVE")
        print("==============================")


        self.memory = GSISIntelligenceMemoryConnector()



    def analyze(self, signal):


        structure_score = 0
        liquidity_score = 0
        pattern_score = 0
        candle_score = 0
        zone_score = 0



        structure = signal.get(
            "structure",
            {}
        )


        if structure.get("bos"):
            structure_score += 20


        if structure.get("trend") in [
            "BULLISH",
            "BEARISH"
        ]:
            structure_score += 10



        liquidity = signal.get(
            "liquidity",
            {}
        )


        if liquidity.get(
            "liquidity_state"
        ) == "ACTIVE":

            liquidity_score += 15



        zone = signal.get(
            "zone",
            {}
        )


        if zone.get(
            "nearest_zone"
        ):

            zone_score += 15



        candlestick = signal.get(
            "candlestick",
            {}
        )


        if candlestick.get(
            "confirmation"
        ):

            candle_score += 15



        pattern_score += 10



        technical_confidence = (

            structure_score
            +
            liquidity_score
            +
            zone_score
            +
            candle_score
            +
            pattern_score

        )



        memory = self.memory.evaluate(
            signal
        )


        historical_probability = memory.get(
            "historical_probability",
            0
        )


        samples = memory.get(
            "historical_samples",
            0
        )


        memory_bonus = 0


        if historical_probability >= 70:

            memory_bonus = 10



        final_confidence = min(
            100,
            technical_confidence + memory_bonus
        )



        if final_confidence >= 80:

            quality = "HIGH"

        elif final_confidence >= 60:

            quality = "MEDIUM"

        else:

            quality = "LOW"



        result = {


            "status":
            "ADAPTIVE INTELLIGENCE COMPLETE",


            "technical_confidence":
            technical_confidence,


            "historical_probability":
            historical_probability,


            "memory_samples":
            samples,


            "memory_bonus":
            memory_bonus,


            "final_confidence":
            final_confidence,


            "quality":
            quality,


            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }


        print("==============================")
        print("GSIS ADAPTIVE INTELLIGENCE RESULT")
        print("==============================")

        print(result)


        return result
