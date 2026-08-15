import os
import sys
import datetime


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

sys.path.insert(
    0,
    PROJECT_ROOT
)


from intelligence.memory.gsis_intelligence_memory_connector import (
    GSISIntelligenceMemoryConnector
)



class GSISAdaptiveIntelligenceBridge:


    def __init__(self):

        print("==============================")
        print("GSIS ADAPTIVE INTELLIGENCE BRIDGE v2.0 ONLINE")
        print("MEMORY + TECHNICAL CONFIDENCE SYNTHESIS ACTIVE")
        print("==============================")


        self.memory = GSISIntelligenceMemoryConnector()



    def analyze(
        self,
        signal
    ):


        structure_score = 0
        liquidity_score = 0
        zone_score = 0
        candle_score = 0
        pattern_score = 0


        structure = signal.get(
            "structure",
            {}
        )


        if structure.get(
            "bos"
        ):

            structure_score += 20


        if structure.get(
            "trend"
        ):

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



        candle = signal.get(
            "candlestick",
            {}
        )


        if candle.get(
            "confirmation"
        ):

            candle_score += 15



        pattern = signal.get(
            "pattern",
            "BULLISH_CANDLE"
        )


        memory_profile = self.memory.build_intelligence_profile(
            pattern
        )


        historical_probability = memory_profile.get(
            "historical_probability",
            0
        )


        memory_samples = memory_profile.get(
            "historical_samples",
            0
        )


        if historical_probability >= 70:

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



        final_confidence = min(
            100,
            technical_confidence
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
            memory_samples,


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



if __name__ == "__main__":


    engine = GSISAdaptiveIntelligenceBridge()


    test_signal = {

        "pattern":
        "BULLISH_CANDLE",


        "structure":
        {
            "bos": True,
            "trend": "BULLISH"
        },


        "liquidity":
        {
            "liquidity_state":
            "ACTIVE"
        },


        "zone":
        {
            "nearest_zone":
            "DEMAND"
        },


        "candlestick":
        {
            "confirmation":
            True
        }

    }


    engine.analyze(
        test_signal
    )
